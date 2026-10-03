#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
包豪斯风格 CNB 个人主页视觉素材生成器
=====================================
只要改下面 CONFIG，重跑本脚本即可重新生成 assets/ 下所有 SVG：

    python3 tools/build_assets.py

再用 tools/render_png.sh 把 SVG 渲染成 2x PNG（README 里默认用 PNG，
这样字体在别人电脑上也不会跑版；想用 SVG 也可以，改 README 里的后缀即可）。
"""

import os
import html

# --------------------------------------------------------------------------
# CONFIG —— 只改这里
# --------------------------------------------------------------------------
CONFIG = {
    "wordmark": "CHANYIKLAM",                       # banner 主标题（大写拉丁）
    "kicker": "CNB.COOL / PROFILE",
    "major_cn": "数据科学与大数据技术",
    "major_en": "DATA SCIENCE & BIG DATA ENGINEERING · GDMU",
    "school_line": "广东医科大学 · 生物医学工程学院 · 2025 级",
    "role_chip": "GDMU-NA 网络协会 · 会长",
    "email": "ChanYikLamNiko@outlook.com",
    "links": ["CNB · cnb.cool/u/ChanYikLam", "GDMU-NA 网络协会 · im.gdmuna.com",
              "广东医科大学"],
    # 技能卡：两张色块卡，每张最多 3~4 行
    "cards": [
        {
            "index": "01",
            "bg": "BLUE",
            "fg": "WHITE",
            "title": "前端开发",
            "subtitle": "FRONTEND ENGINEERING",
            "rows": [
                ("Vue.js", "熟练", 2),
                ("React", "熟练", 2),
                ("Tailwind CSS", "熟练", 2),
            ],
        },
        {
            "index": "02",
            "bg": "YELLOW",
            "fg": "INK",
            "title": "AI 与大模型应用",
            "subtitle": "AI / LLM APPLICATION",
            "rows": [
                ("RAG 检索增强", "熟练", 2),
                ("Agent 智能体", "熟练", 2),
                ("提示词工程", "熟练", 2),
            ],
        },
    ],
}

# --------------------------------------------------------------------------
# 设计 token
# --------------------------------------------------------------------------
COLORS = {
    "INK": "#111111",
    "PAPER": "#F2EFE6",
    "WHITE": "#FFFFFF",
    "RED": "#E23A2E",
    "BLUE": "#1B3FCB",
    "YELLOW": "#F5C518",
    "GREY": "#7A766C",
}
FONT = ("Futura, 'Avenir Next', 'Century Gothic', 'PingFang SC', "
        "'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif")
W = 1400  # 所有素材统一宽度，方便在 README 里对齐
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")


def esc(t):
    return html.escape(str(t), quote=True)


def text(x, y, s, size, fill="INK", weight=400, ls=0, anchor="start", opacity=None):
    a = [f'x="{x}"', f'y="{y}"', f'font-family="{FONT}"', f'font-size="{size}"',
         f'font-weight="{weight}"', f'fill="{COLORS[fill]}"']
    if ls:
        a.append(f'letter-spacing="{ls}"')
    if anchor != "start":
        a.append(f'text-anchor="{anchor}"')
    if opacity is not None:
        a.append(f'opacity="{opacity}"')
    return f'<text {" ".join(a)}>{esc(s)}</text>'


def rect(x, y, w, h, fill, opacity=None, stroke=None, sw=2, rotate=None):
    a = [f'x="{x}"', f'y="{y}"', f'width="{w}"', f'height="{h}"', f'fill="{COLORS.get(fill, fill)}"']
    if opacity is not None:
        a.append(f'opacity="{opacity}"')
    if stroke:
        a.append(f'stroke="{COLORS.get(stroke, stroke)}" stroke-width="{sw}"')
    if rotate is not None:
        a.append(f'transform="rotate({rotate} {x + w / 2} {y + h / 2})"')
    return f'<rect {" ".join(a)}/>'


def circle(cx, cy, r, fill, opacity=None):
    a = [f'cx="{cx}"', f'cy="{cy}"', f'r="{r}"', f'fill="{COLORS.get(fill, fill)}"']
    if opacity is not None:
        a.append(f'opacity="{opacity}"')
    return f'<circle {" ".join(a)}/>'


def poly(points, fill, opacity=None):
    a = [f'points="{points}"', f'fill="{COLORS.get(fill, fill)}"']
    if opacity is not None:
        a.append(f'opacity="{opacity}"')
    return f'<polygon {" ".join(a)}/>'


def line(x1, y1, x2, y2, stroke="INK", sw=2, opacity=None):
    a = [f'x1="{x1}"', f'y1="{y1}"', f'x2="{x2}"', f'y2="{y2}"',
         f'stroke="{COLORS.get(stroke, stroke)}"', f'stroke-width="{sw}"']
    if opacity is not None:
        a.append(f'opacity="{opacity}"')
    return f'<line {" ".join(a)}/>'


def svg(h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" '
            f'viewBox="0 0 {W} {h}" role="img">\n  ' + "\n  ".join(body) + "\n</svg>\n")


# --------------------------------------------------------------------------
# 1) HERO
# --------------------------------------------------------------------------
def build_hero():
    c = CONFIG
    H = 440
    b = [rect(0, 0, W, H, "PAPER")]
    # 右侧白色版面 + 黑色右边条
    b += [rect(860, 0, 504, H, "WHITE"), rect(1364, 0, 36, H, "INK")]
    # 几何构成
    b += [
        rect(980, 250, 160, 160, "RED"),
        circle(1140, 165, 115, "BLUE"),
        poly("1250,440 1364,440 1364,300", "YELLOW"),
        rect(1275, 45, 52, 52, "INK"),
        line(860, 165, 1015, 165, "INK", 2),
    ]
    # 左侧文字
    b += [
        rect(0, 0, 16, H, "INK"),
        text(72, 96, c["kicker"], 18, "INK", 500, 5),
        rect(72, 112, 84, 7, "YELLOW"),
        text(66, 234, c["wordmark"], 88, "INK", 700, 1),
        text(72, 288, c["major_cn"], 32, "INK", 700, 0),
        text(72, 326, c["school_line"], 20, "GREY", 400, 0),
        text(72, 358, c["major_en"], 15, "GREY", 500, 2.5),
        rect(72, 378, 320, 38, "BLUE"),
        text(90, 404, c["role_chip"], 19, "WHITE", 500, 0.5),
    ]
    return svg(H, b)


# --------------------------------------------------------------------------
# 2) SKILLS
# --------------------------------------------------------------------------
def dots(x, y, filled, fg, size=20, gap=28):
    out = []
    for i in range(3):
        if i < filled:
            out.append(rect(x + i * gap, y, size, size, fg))
        else:
            out.append(rect(x + i * gap, y, size, size, "none", stroke=fg, sw=2))
    return out


def build_skills():
    H = 600
    b = [rect(0, 0, W, H, "PAPER")]
    for n, card in enumerate(CONFIG["cards"]):
        cx = 40 + n * 680
        cw, cy, ch = 640, 40, 460
        bg, fg = card["bg"], card["fg"]
        b.append(rect(cx, cy, cw, ch, bg))
        ix = cx + 48
        b += [
            text(ix, cy + 110, card["index"], 92, fg, 700, 0, opacity=0.28),
            text(ix, cy + 186, card["title"], 48, fg, 700),
            text(ix, cy + 222, card["subtitle"], 16, fg, 500, 4, opacity=0.85),
            line(ix, cy + 252, cx + cw - 48, cy + 252, fg, 2, opacity=0.5),
        ]
        for j, (name, level, filled) in enumerate(card["rows"]):
            ry = cy + 312 + j * 58
            b += [
                text(ix, ry, name, 31, fg, 600),
                text(cx + cw - 146, ry, level, 22, fg, 500, 2, anchor="end", opacity=0.9),
            ]
            b += dots(cx + cw - 124, ry - 20, filled, fg)
    # 图例条
    b += [rect(40, 524, 1320, 52, "INK")]
    b += [text(72, 557, "熟练度 LEVEL", 16, "WHITE", 500, 3, opacity=0.7)]
    legend = [("精通", 3), ("熟练", 2), ("了解", 1)]
    lx = 320
    for label, n in legend:
        b += dots(lx, 540, n, "WHITE", 16, 24)
        b += [text(lx + 96, 556, label, 19, "WHITE", 500, 1)]
        lx += 250
    return svg(H, b)


# --------------------------------------------------------------------------
# 3) FOOTER
# --------------------------------------------------------------------------
def build_footer():
    c = CONFIG
    H = 230
    b = [rect(0, 0, W, H, "INK")]
    b += [
        rect(72, 52, 14, 14, "YELLOW"),
        text(100, 66, "CONTACT / 联系", 16, "WHITE", 500, 5, opacity=0.75),
        text(72, 128, c["email"], 32, "WHITE", 700, 0.5),
        line(72, 164, 1092, 164, "WHITE", 1, opacity=0.22),
    ]
    # 三条链接的 x 由实测宽度定：323.5 / 399.4 / 135.0（22px, ls .5），间距 44
    xs = [72, 440, 884]
    for i, s in enumerate(c["links"]):
        if i < len(xs):
            b.append(text(xs[i], 200, s, 22, "WHITE", 400, 0.5, opacity=0.8))
    b += [
        circle(1190, 100, 54, "BLUE"),
        rect(1265, 45, 56, 56, "YELLOW"),
        poly("1280,230 1400,230 1400,118", "RED"),
    ]
    return svg(H, b)


def main():
    os.makedirs(OUT, exist_ok=True)
    files = {
        "bauhaus-hero.svg": build_hero(),
        "bauhaus-skills.svg": build_skills(),
        "bauhaus-footer.svg": build_footer(),
    }
    for name, content in files.items():
        p = os.path.join(OUT, name)
        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
        print("wrote", os.path.relpath(p))


if __name__ == "__main__":
    main()
