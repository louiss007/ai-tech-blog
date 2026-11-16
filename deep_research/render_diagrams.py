#!/usr/bin/env python3
"""Render every article diagram from SVG to a 2x PNG with Playwright.

Usage:
    python3 render_diagrams.py

The PNG is written next to its SVG in wechat-series/images/. Edit the SVG,
not the PNG; then rerun this script.
"""

from __future__ import annotations

import re
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = Path(__file__).resolve().parent
IMG_DIR = BASE / "wechat-series" / "images"


def render(svg_path: Path, browser) -> None:
    svg = svg_path.read_text(encoding="utf-8")
    match = re.search(r'width="(\d+)"\s+height="(\d+)"', svg)
    if not match:
        raise ValueError(f"cannot read width/height from {svg_path}")
    width, height = map(int, match.groups())

    html = (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        "<style>html,body{margin:0;padding:0;background:#fff}"
        "svg{display:block}</style></head><body>"
        f"{svg}</body></html>"
    )

    page = browser.new_page(
        viewport={"width": width, "height": height},
        device_scale_factor=2,
    )
    page.set_content(html, wait_until="load")
    page.wait_for_timeout(200)
    png_path = svg_path.with_suffix(".png")
    page.locator("svg").screenshot(path=str(png_path), omit_background=False)
    page.close()
    print(f"{png_path.name}: {width * 2}x{height * 2}")


def main() -> None:
    svgs = sorted(IMG_DIR.glob("*.svg"))
    if not svgs:
        raise SystemExit(f"no SVG files in {IMG_DIR}")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            for svg_path in svgs:
                render(svg_path, browser)
        finally:
            browser.close()


if __name__ == "__main__":
    main()
