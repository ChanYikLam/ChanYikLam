#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 assets/*.svg 渲染成 PNG（默认 2 倍图），输出到 assets/png/。

    python3 tools/render_png.py          # 2x
    SCALE=1 python3 tools/render_png.py  # 1x

为什么 README 里用 PNG 而不是 SVG：
    SVG 里的字体依赖查看者本机字体，别人在 Windows / Android 上看会掉字重；
    PNG 把版式烘焙死，任何设备打开都一模一样。SVG 保留作为可编辑源文件。
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets")
DST = os.path.join(SRC, "png")
SCALE = int(os.environ.get("SCALE", "2"))

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    shutil.which("google-chrome") or "",
    shutil.which("chromium") or "",
]


def find_chrome():
    for c in CHROME_CANDIDATES:
        if c and os.path.exists(c):
            return c
    sys.exit("没找到 Chrome / Chromium，请手动打开 SVG 导出 PNG，或安装后重跑。")


def main():
    chrome = find_chrome()
    os.makedirs(DST, exist_ok=True)
    svgs = sorted(f for f in os.listdir(SRC) if f.endswith(".svg"))
    if not svgs:
        sys.exit("assets/ 下没有 SVG，先跑 python3 tools/build_assets.py")
    for name in svgs:
        path = os.path.join(SRC, name)
        content = open(path, encoding="utf-8").read()
        m = re.search(r'width="(\d+)"\s+height="(\d+)"', content)
        if not m:
            print("跳过（没找到 width/height）:", name)
            continue
        w, h = int(m.group(1)), int(m.group(2))
        out = os.path.join(DST, name[:-4] + ".png")
        with tempfile.TemporaryDirectory() as tmp:
            page = os.path.join(tmp, "shot.html")
            with open(page, "w", encoding="utf-8") as f:
                f.write(
                    "<!doctype html><meta charset='utf-8'>"
                    "<style>html,body{margin:0;padding:0;background:#fff}"
                    f"img{{display:block;width:{w}px;height:{h}px}}</style>"
                    f"<img src='file://{path}'>"
                )
            subprocess.run(
                [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                 f"--force-device-scale-factor={SCALE}",
                 f"--window-size={w},{h}", f"--screenshot={out}", f"file://{page}"],
                check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
        print(f"wrote {os.path.relpath(out, ROOT)}  ({w * SCALE}x{h * SCALE})")


if __name__ == "__main__":
    main()
