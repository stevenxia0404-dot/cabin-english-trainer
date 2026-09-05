# -*- coding: utf-8 -*-
"""生成 PWA 图标（占位版，Steven 出正式图后可整批替换）。

设计：深底 #04060D + 金 #E8C877 麦克风剪影。
麦克风 = 跟读/口语练习，纯几何绘制不依赖字体，192px 小尺寸也能认出来。

产出（全部落在 icons/ 目录）：
    icon-192.png             Android 桌面
    icon-512.png             启动画面 / 安装弹窗
    icon-512-maskable.png    Android 自适应图标（内容缩到 72%，保证安全区不被裁）
    apple-touch-icon-180.png iOS 桌面（RGB 不带透明通道，否则 iOS 会给黑底）

用法：
    python make_icons.py
"""
import os

from PIL import Image, ImageDraw

# 品牌色
BG = (4, 6, 13)        # #04060D 应用深底
FG = (232, 199, 119)   # #E8C877 品牌金

BASE = 1024            # 设计基准画布
SS = 4                 # 超采样倍数（先画大再缩，边缘更平滑）

# 麦克风几何，全部定义在 1024×1024 基准坐标系里
CAPSULE = (422, 201, 602, 491)      # 话筒头（胶囊形）
CAPSULE_R = 90
BRACKET = (302, 304, 722, 724)      # U 形支架外接框
BRACKET_START, BRACKET_END = -10, 190
BRACKET_W = 34
STEM = (512, 724, 512, 784)         # 立杆
STEM_W = 34
BASE_BAR = (382, 784, 642, 824)     # 底座
BASE_R = 20


def draw_mic(d, scale):
    """在已放大的画布上画麦克风。scale 用来给 maskable 版留安全边距。"""
    c = (BASE * SS) / 2.0

    def tx(x):
        return c + (x - 512) * scale * SS

    def ty(y):
        return c + (y - 512) * scale * SS

    def box(b):
        return [tx(b[0]), ty(b[1]), tx(b[2]), ty(b[3])]

    w = max(1, int(round(BRACKET_W * scale * SS)))
    w = w if w % 2 == 0 else w + 1   # 偶数宽度，避免描边偏移半像素

    d.rounded_rectangle(box(CAPSULE), radius=CAPSULE_R * scale * SS, fill=FG)
    d.arc(box(BRACKET), BRACKET_START, BRACKET_END, fill=FG, width=w)
    d.line([tx(STEM[0]), ty(STEM[1]), tx(STEM[2]), ty(STEM[3])], fill=FG, width=w)
    d.rounded_rectangle(box(BASE_BAR), radius=BASE_R * scale * SS, fill=FG)


def render(size, scale=1.0, opaque=False):
    """渲染单个图标。opaque=True 时丢掉 alpha 通道（iOS 要求）。"""
    img = Image.new("RGBA", (BASE * SS, BASE * SS), BG + (255,))
    draw_mic(ImageDraw.Draw(img), scale)
    img = img.resize((size, size), Image.LANCZOS)
    if opaque:
        img = img.convert("RGB")
    return img


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(root, "icons")
    if not os.path.exists(out):
        os.makedirs(out)

    jobs = [
        ("icon-192.png", 192, 1.0, False),
        ("icon-512.png", 512, 1.0, False),
        # maskable：内容缩到 72%，保证被裁成圆/方圆角时麦克风仍在安全区内
        ("icon-512-maskable.png", 512, 0.72, False),
        # iOS：必须不带透明通道
        ("apple-touch-icon-180.png", 180, 1.0, True),
    ]

    for name, size, scale, opaque in jobs:
        p = os.path.join(out, name)
        render(size, scale, opaque).save(p, "PNG", optimize=True)
        print("  %-28s %4dpx  scale=%.2f  %s"
              % (name, size, scale, "RGB(无透明)" if opaque else "RGBA"))

    print("图标已生成 -> %s" % out)


if __name__ == "__main__":
    main()
