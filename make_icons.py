# -*- coding: utf-8 -*-
"""从 assets/logo.png 生成 PWA 应用图标。

处理流程：
1. 读取 logo 源图（当前为 2048×2048 米白底金色图形）。
2. 用 HSV 饱和度+亮度把米白背景替换为 App 主背景色 #070B16。
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
SAT_THR = 20                 # HSV 饱和度阈值：区分金色前景与米白背景
VAL_THR = 245                # HSV 亮度阈值：金色比背景稍暗

# 前景在最终图标里的占比
FILL_NORMAL = 0.80           # 普通图标内容占画布 80%
FILL_MASKABLE = 0.64         # maskable 安全区要求：内容缩到中心 80% 区域内


def extract_foreground(src_path):
    """把 logo 的米白背景替换为 #070B16，返回 RGB 前景图。"""
    src = Image.open(src_path).convert("RGB")
    w, h = src.size
    bg = Image.new("RGB", (w, h), TARGET_BG)

    h, s, v = src.convert("HSV").split()
    mask_s = s.point(lambda x: 255 if x > SAT_THR else 0, mode="L")
    mask_v = v.point(lambda x: 255 if x < VAL_THR else 0, mode="L")
    mask = ImageChops.multiply(mask_s, mask_v)

    return Image.composite(src, bg, mask)


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
    fg = extract_foreground(src)

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
