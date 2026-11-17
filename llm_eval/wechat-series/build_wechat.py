#!/usr/bin/env python3
"""Render the four WeChat Markdown sources into inline-styled HTML.

The Markdown files are the source of truth. This script only reads them
and writes the matching .html files. It deliberately supports a small
Markdown subset so every output element can carry inline styles that the
WeChat editor keeps.

Usage:
    python3 build_wechat.py
"""

from __future__ import annotations

import html as htmlmod
import re
import unicodedata
from pathlib import Path

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import TextLexer, get_lexer_by_name

BASE = Path(__file__).resolve().parent
PARTS = ["part1", "part2", "part3", "part4"]

# ---------------------------------------------------------------- styles
S_WRAP = (
    "max-width:677px;margin:0 auto;padding:24px 20px 48px;background:#ffffff;"
    "font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC',"
    "'Hiragino Sans GB','Microsoft YaHei',sans-serif;font-size:16px;"
    "line-height:1.8;color:#374151;letter-spacing:0.4px;"
)
S_H1 = (
    "margin:0 0 18px;font-size:24px;line-height:1.45;font-weight:700;"
    "color:#111827;letter-spacing:0.5px;"
)
S_H2 = (
    "margin:40px 0 16px;padding-left:12px;border-left:5px solid #2563eb;"
    "font-size:20px;line-height:1.5;font-weight:700;color:#0f172a;"
)
S_H3 = (
    "margin:28px 0 12px;font-size:17px;line-height:1.6;font-weight:600;"
    "color:#1e3a8a;"
)
S_P = (
    "margin:0 0 18px;font-size:16px;line-height:1.85;color:#374151;"
    "text-align:justify;"
)
S_NOTE = (
    "margin:22px 0;font-size:14px;line-height:1.8;color:#64748b;"
    "text-align:center;"
)
S_BQ = (
    "margin:18px 0;padding:14px 18px;background:#f0f7ff;"
    "border-left:4px solid #2563eb;border-radius:0 6px 6px 0;"
    "color:#1e3a5f;font-size:15px;line-height:1.8;"
)
S_UL = "margin:0 0 18px;padding-left:24px;color:#374151;"
S_LI = "margin:0 0 9px;line-height:1.8;font-size:16px;"
S_HR = "border:none;border-top:1px solid #e5e7eb;margin:34px 0;"
S_STRONG = "color:#111827;font-weight:600;"
S_EM = "color:#6b7280;font-style:normal;"
S_CODE = (
    "padding:2px 6px;border-radius:4px;background:#f1f5f9;color:#be123c;"
    "font-size:14px;font-family:'SFMono-Regular',Consolas,'Liberation Mono',"
    "Menlo,monospace;"
)
S_TABLE_WRAP = "margin:22px 0;overflow-x:auto;"
S_TABLE = (
    "width:100%;border-collapse:collapse;table-layout:fixed;"
    "font-size:13px;line-height:1.65;color:#374151;"
)
S_TH = (
    "padding:8px 10px;border:1px solid #e5e7eb;background:#f1f5f9;"
    "color:#111827;font-weight:600;text-align:left;word-break:break-word;"
)
S_TD = (
    "padding:8px 10px;border:1px solid #e5e7eb;vertical-align:top;"
    "word-break:break-word;"
)
S_PRE_WRAP = (
    "margin:22px 0;border-radius:8px;overflow-x:auto;background:#272822;"
)
S_PRE = (
    "margin:0;padding:16px 18px;font-size:12px;line-height:1.7;"
    "font-family:'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace;"
    "color:#f8f8f2;white-space:pre-wrap;word-break:break-word;"
)


# ---------------------------------------------------------------- inline
def inline(text: str) -> str:
    """Render bold, italic, and inline code."""
    text = htmlmod.escape(text, quote=False)
    codes: list[str] = []

    def stash_code(m: re.Match[str]) -> str:
        codes.append(m.group(1))
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]+)`", stash_code, text)
    text = re.sub(
        r"\*\*(.+?)\*\*",
        lambda m: f'<strong style="{S_STRONG}">{m.group(1)}</strong>',
        text,
    )
    text = re.sub(
        r"(?<!\*)\*([^*]+)\*(?!\*)",
        lambda m: f'<em style="{S_EM}">{m.group(1)}</em>',
        text,
    )

    def restore_code(m: re.Match[str]) -> str:
        return f'<code style="{S_CODE}">{codes[int(m.group(1))]}</code>'

    return re.sub(r"\x00(\d+)\x00", restore_code, text)


# ---------------------------------------------------------------- blocks
def render_code(code: str, lang: str) -> str:
    try:
        lexer = get_lexer_by_name(lang or "text", stripall=False)
    except Exception:
        lexer = TextLexer()
    formatter = HtmlFormatter(noclasses=True, nowrap=True, style="monokai")
    body = highlight(code, lexer, formatter).rstrip("\n")
    return (
        f'<div style="{S_PRE_WRAP}"><pre style="{S_PRE}">'
        f"<code>{body}</code></pre></div>"
    )


def split_table_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def display_width(text: str) -> int:
    return sum(
        2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in text
    )


def column_widths(header: list[str], body: list[list[str]]) -> list[int]:
    """Allocate column widths from content, clamped for mobile screens."""
    n = len(header)
    if n == 2:
        return [32, 68]
    if n != 3:
        return [round(100 / n)] * n

    values = []
    for j in range(n):
        cells = [header[j]] + [row[j] for row in body if j < len(row)]
        values.append(max(display_width(c) for c in cells))

    weights = [min(26, max(14, v)) for v in values]
    total = sum(weights)
    widths = [round(100 * w / total) for w in weights]

    # Keep every column usable; take the difference from the widest.
    for j in range(n):
        if widths[j] < 20:
            need = 20 - widths[j]
            widths[j] = 20
            widest = max(range(n), key=lambda k: widths[k])
            widths[widest] -= need

    widths[-1] = 100 - sum(widths[:-1])
    return widths


def render_table(rows: list[str]) -> str:
    header = split_table_row(rows[0])
    body = [split_table_row(r) for r in rows[2:]]
    widths = column_widths(header, body)

    out = [f'<div style="{S_TABLE_WRAP}"><table style="{S_TABLE}">', "<thead><tr>"]
    for cell, width in zip(header, widths):
        out.append(f'<th style="{S_TH}width:{width}%;">{inline(cell)}</th>')
    out.append("</tr></thead><tbody>")
    for i, row in enumerate(body):
        bg = "background:#fafafa;" if i % 2 == 1 else ""
        out.append("<tr>")
        for cell in row:
            out.append(f'<td style="{S_TD}{bg}">{inline(cell)}</td>')
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def md_to_html(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("<!--"):
            while i < n and "-->" not in lines[i]:
                i += 1
            i += 1
            continue

        if not stripped:
            i += 1
            continue

        # fenced code
        if stripped.startswith("```"):
            lang = stripped[3:].strip()
            i += 1
            buf: list[str] = []
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            out.append(render_code("\n".join(buf), lang))
            continue

        # headings
        m = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if m:
            level = len(m.group(1))
            text = inline(m.group(2).strip())
            styles = {1: S_H1, 2: S_H2, 3: S_H3, 4: S_H3}
            out.append(f'<h{level} style="{styles[level]}">{text}</h{level}>')
            i += 1
            continue

        if stripped == "---":
            out.append(f'<hr style="{S_HR}">')
            i += 1
            continue

        # image (kept for future use)
        m = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)$", stripped)
        if m:
            alt = htmlmod.escape(m.group(1), quote=True)
            src = htmlmod.escape(m.group(2), quote=True)
            out.append(
                f'<figure style="margin:24px 0;text-align:center;">'
                f'<img src="{src}" alt="{alt}" '
                f'style="width:100%;max-width:100%;border-radius:8px;'
                f'display:block;margin:0 auto;"></figure>'
            )
            i += 1
            continue

        # blockquote
        if stripped.startswith(">"):
            paras: list[str] = []
            buf: list[str] = []
            while i < n and lines[i].strip().startswith(">"):
                q = lines[i].strip()[1:].strip()
                if q:
                    buf.append(inline(q))
                elif buf:
                    paras.append("<br>".join(buf))
                    buf = []
                i += 1
            if buf:
                paras.append("<br>".join(buf))
            inner = "".join(
                f'<p style="margin:{"0" if idx == len(paras) - 1 else "0 0 10px"};">{p}</p>'
                for idx, p in enumerate(paras)
            )
            out.append(f'<blockquote style="{S_BQ}">{inner}</blockquote>')
            continue

        # table
        if stripped.startswith("|") and i + 1 < n:
            if re.match(r"^\|[\s:|-]+\|$", lines[i + 1].strip()):
                rows = []
                while i < n and lines[i].strip().startswith("|"):
                    rows.append(lines[i].strip())
                    i += 1
                out.append(render_table(rows))
                continue

        # unordered list
        if re.match(r"^[-*]\s+", stripped):
            items = []
            while i < n and re.match(r"^[-*]\s+", lines[i].strip()):
                item = re.sub(r"^[-*]\s+", "", lines[i].strip())
                items.append(f'<li style="{S_LI}">{inline(item)}</li>')
                i += 1
            out.append(f'<ul style="{S_UL}">{"".join(items)}</ul>')
            continue

        # ordered list
        if re.match(r"^\d+\.\s+", stripped):
            items = []
            start = int(re.match(r"^(\d+)\.", stripped).group(1))
            while i < n and re.match(r"^\d+\.\s+", lines[i].strip()):
                item = re.sub(r"^\d+\.\s+", "", lines[i].strip())
                items.append(f'<li style="{S_LI}">{inline(item)}</li>')
                i += 1
            out.append(
                f'<ol start="{start}" style="{S_UL}">{"".join(items)}</ol>'
            )
            continue

        # paragraph
        buf = []
        while i < n:
            cur = lines[i].strip()
            if not cur:
                break
            if (
                cur.startswith(("#", ">", "|", "```", "<!--", "!["))
                or cur == "---"
                or re.match(r"^[-*]\s+", cur)
                or re.match(r"^\d+\.\s+", cur)
            ):
                break
            buf.append(inline(cur))
            i += 1
        if buf:
            note = (
                re.match(r'^<em style="[^"]*">(.*)</em>$', buf[0], re.S)
                if len(buf) == 1
                else None
            )
            if note:
                out.append(f'<p style="{S_NOTE}">{note.group(1)}</p>')
            else:
                out.append(f'<p style="{S_P}">{"<br>".join(buf)}</p>')
        else:
            i += 1

    return "\n".join(out)


def html_document(title: str, body: str) -> str:
    safe_title = htmlmod.escape(title)
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{safe_title}</title>
</head>
<body style="margin:0;padding:0;background:#ffffff;">
<section style="{S_WRAP}">
{body}
</section>
</body>
</html>
"""


def main() -> None:
    for part in PARTS:
        md_path = BASE / f"{part}.md"
        if not md_path.exists():
            raise SystemExit(f"missing source: {md_path}")
        md = md_path.read_text(encoding="utf-8")
        title = next(
            line[2:].strip()
            for line in md.splitlines()
            if line.startswith("# ")
        )
        html_path = BASE / f"{part}.html"
        html_path.write_text(
            html_document(title, md_to_html(md)),
            encoding="utf-8",
        )
        print(f"wrote {html_path.name}")


if __name__ == "__main__":
    main()
