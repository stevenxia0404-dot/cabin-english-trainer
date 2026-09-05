# -*- coding: utf-8 -*-
"""从 assets/logo.png 生成 PWA 应用图标。

处理流程：
1. 读取 logo 源图（2048×2048，金色图形，背景可为米白或深色）。
2. 采样四角估计背景色，用颜色距离把背景统一替换为 App 主背景色 #070B16。
3. 按平台规范出 4 个图标文件：
   - icon-192.png             Android 桌面
   - icon-512.png             启动画面 / 安装弹窗
   - icon-512-maskable.png    Android 自适应图标（内容缩到 64%，留足安全区）
   - apple-touch-icon-180.png iOS 桌面（RGB 不带透明通道）

用法：
    python make_icons.py
"""
import os

from PIL import Image, ImageChops

# 品牌/应用色
TARGET_BG = (7, 11, 22)      # #070B16，与应用 --bg 一致
BG_THR = 35                  # 背景判定阈值：像素与参考背景的「最大通道差」小于此值即视为背景

# 前景在最终图标里的占比（已先裁掉黑边留白并按视觉质心居中，故话筒图形本身即填满该比例）
# 注意：fill 不是越大越好。圆角/异形图标需要四周留边距（iOS 圆角会切边），
# 内容占比约 84%，已接近圆角安全区上限，让话筒最大化占满图标。
FILL_NORMAL = 0.84           # 普通图标：话筒占画布 84%，极限饱满
FILL_MASKABLE = 0.78         # maskable：内容占 78%，在安卓 80% 安全区内


def extract_foreground(src_path):
    """把 logo 背景统一替换为 App 主背景色 #070B16，返回 RGB 前景图。

    自适应背景：采样四角估计背景色，再用「各通道最大差值」阈值把背景像素
    替换为目标色。这样无论米白底还是深色底 logo 都能干净统一——避免 HSV
    阈值在深底色下把整张黑底误判为前景、或边缘出现斑驳。
    """
    src = Image.open(src_path).convert("RGB")
    w, h = src.size

    # 采样四角估计背景色（源图四角通常为纯背景）
    corners = [src.getpixel((0, 0)), src.getpixel((w - 1, 0)),
               src.getpixel((0, h - 1)), src.getpixel((w - 1, h - 1))]
    bg_ref = tuple(sum(c[i] for c in corners) // 4 for i in range(3))

    # 每个像素与参考背景的「各通道最大差值」，背景像素差值接近 0
    diff = ImageChops.difference(src, Image.new("RGB", (w, h), bg_ref))
    r, g, b = diff.split()
    # lighter 逐通道取最大值，连用得到三通道最大差；转 L 后做阈值
    mx = ImageChops.lighter(r, ImageChops.lighter(g, b)).convert("L")
    # 差值 < BG_THR 视为背景 -> 替换为 TARGET_BG；否则保留原像素
    mask = mx.point(lambda x: 0 if x < BG_THR else 255)

    bg_canvas = Image.new("RGB", (w, h), TARGET_BG)
    fg = Image.composite(src, bg_canvas, mask)
    return fg, mask


def crop_to_visual_center(fg, mask):
    """按前景金色像素的视觉质心（centroid）裁剪成正方形。

    话筒+云的图形重心通常不在几何 bbox 中心（顶部云弧线重、底部支架轻），
    直接用 bbox 居中会导致图标视觉上偏上。这里以所有金色像素的平均位置
    作为视觉中心，裁剪出以该中心为中心、且能完整包含前景的最小正方形。
    """
    w, h = fg.size
    bbox = mask.getbbox()
    if not bbox:
        return fg
    left, top, right, bottom = bbox
    sub_w = right - left
    sub_h = bottom - top

    # 在 bbox 内计算前景像素的质心（用 tobytes 避免 Pillow 14 移除 getdata）
    sub_mask = mask.crop(bbox)
    data = sub_mask.tobytes()
    total = 0
    sx = sy = 0
    for i in range(len(data)):
        if data[i]:
            sx += i % sub_w
            sy += i // sub_w
            total += 1
    if total == 0:
        return fg.crop(bbox)
    cx = left + sx / total
    cy = top + sy / total

    # 以质心为中心，覆盖整个前景的最小正方形半边长
    half = int(max(cx - left, right - cx, cy - top, bottom - cy))
    new_left = max(0, int(round(cx - half)))
    new_top = max(0, int(round(cy - half)))
    new_right = min(w, int(round(cx + half)))
    new_bottom = min(h, int(round(cy + half)))

    # 若因越界导致中心不对称，尽量保持中心位置（通常不会越界）
    if new_right - new_left != new_bottom - new_top:
        side = max(new_right - new_left, new_bottom - new_top)
        new_right = new_left + side
        new_bottom = new_top + side
    return fg.crop((new_left, new_top, new_right, new_bottom))


def render_icon(fg, size, fill):
    """把前景图按 fill 比例居中放到 size×size 画布上。"""
    canvas = Image.new("RGB", (size, size), TARGET_BG)
    scale = int(size * fill)
    scaled = fg.resize((scale, scale), Image.LANCZOS)
    offset = (size - scale) // 2
    canvas.paste(scaled, (offset, offset))
    return canvas


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(root, "assets", "logo.png")
    if not os.path.exists(src):
        raise FileNotFoundError(f"缺少 logo 源文件：{src}")

    out = os.path.join(root, "icons")
    os.makedirs(out, exist_ok=True)

    print("正在从 assets/logo.png 提取前景并替换背景...")
    fg, mask = extract_foreground(src)
    # 先按视觉质心裁剪，让话筒在云形轮廓里真正居中（避免 bbox 几何居中导致视觉上偏上）
    fg = crop_to_visual_center(fg, mask)
    print("  前景裁切后尺寸:", fg.size)

    jobs = [
        ("icon-192.png", 192, FILL_NORMAL),
        ("icon-512.png", 512, FILL_NORMAL),
        ("icon-512-maskable.png", 512, FILL_MASKABLE),
        ("apple-touch-icon-180.png", 180, FILL_NORMAL),
    ]

    for name, size, fill in jobs:
        p = os.path.join(out, name)
        icon = render_icon(fg, size, fill)
        icon.save(p, "PNG", optimize=True)
        print("  %-28s %4dpx  fill=%.0f%%" % (name, size, fill * 100))

    print("图标已生成 -> %s" % out)


if __name__ == "__main__":
    main()
