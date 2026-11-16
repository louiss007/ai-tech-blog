#!/usr/bin/env python3
"""Split the WeChat long-form article into a 3-part series and render
inline-styled HTML that can be pasted into the WeChat article editor.

Usage: python3 build_wechat_series.py
"""

from __future__ import annotations

import html as htmlmod
import re
from pathlib import Path

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import TextLexer, get_lexer_by_name

BASE = Path(__file__).resolve().parent
SRC = BASE / "deep-research-wechat.md"
OUT = BASE / "wechat-series"

# ---------------------------------------------------------------- styles
S_WRAP = (
    "max-width:677px;margin:0 auto;padding:24px 20px 48px;background:#ffffff;"
    "font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC',"
    "'Hiragino Sans GB','Microsoft YaHei',sans-serif;font-size:16px;"
    "line-height:1.8;color:#374151;letter-spacing:0.4px;"
)
S_H1 = (
    "margin:0 0 18px;font-size:25px;line-height:1.45;font-weight:700;"
    "color:#111827;letter-spacing:0.5px;"
)
S_H2 = (
    "margin:42px 0 18px;padding-left:12px;border-left:5px solid #2563eb;"
    "font-size:21px;line-height:1.5;font-weight:700;color:#0f172a;"
)
S_H3 = (
    "margin:30px 0 12px;font-size:18px;line-height:1.6;font-weight:600;"
    "color:#1e3a8a;"
)
S_P = (
    "margin:0 0 18px;font-size:16px;line-height:1.85;color:#374151;"
    "text-align:justify;"
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
    """Render a small Markdown subset: bold, italic, inline code."""
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


def render_table(rows: list[str]) -> str:
    header = split_table_row(rows[0])
    body = [split_table_row(r) for r in rows[2:]]

    widths_by_count = {
        2: [30, 70],
        3: [26, 40, 34],
        4: [22, 26, 26, 26],
    }
    widths = widths_by_count.get(
        len(header), [round(100 / len(header))] * len(header)
    )

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

        # HTML comments
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
            text = inline(m.group(2))
            styles = {1: S_H1, 2: S_H2, 3: S_H3, 4: S_H3}
            out.append(f'<h{level} style="{styles[level]}">{text}</h{level}>')
            i += 1
            continue

        # horizontal rule
        if stripped == "---":
            out.append(f'<hr style="{S_HR}">')
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

        # paragraph: gather until blank or block marker
        buf = []
        while i < n:
            cur = lines[i].strip()
            if not cur:
                break
            if (
                cur.startswith(("#", ">", "|", "```", "<!--"))
                or cur == "---"
                or re.match(r"^[-*]\s+", cur)
                or re.match(r"^\d+\.\s+", cur)
            ):
                break
            buf.append(inline(cur))
            i += 1
        if buf:
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


# ---------------------------------------------------------------- split
P1_TITLE = "Deep Research 技术详解（上）：从“搜索 + 总结”到研究型 Agent"
P1_SUB = "为什么需要 Deep Research，以及它的 7 个核心模块"
P2_TITLE = "Deep Research 技术详解（中）：RAG 之后，一次研究任务怎么跑起来"
P2_SUB = "与 RAG 的区别、13 步工作流、6 个工程难点和可落地架构"
P3_TITLE = "Deep Research 技术详解（下）：评估、场景、趋势与落地建议"
P3_SUB = "怎么衡量研究质量，能用在哪些场景，以及团队如何起步"

P1_NOTE = """<!--
公众号发布备注（转换后不会显示）：
本文是「Deep Research 技术详解」连载上篇，覆盖 01–03。
建议封面文案：Deep Research（上）/ 不是搜索加总结
正文含 2 处配图建议。
-->"""

P2_NOTE = """<!--
公众号发布备注（转换后不会显示）：
本文是「Deep Research 技术详解」连载中篇，覆盖 04–07。
建议封面文案：Deep Research（中）/ 一次研究怎么跑起来
正文含 1 处配图建议。
-->"""

P3_NOTE = """<!--
公众号发布备注（转换后不会显示）：
本文是「Deep Research 技术详解」连载下篇，覆盖 08–11 与落地建议。
建议封面文案：Deep Research（下）/ 场景、趋势与落地
-->"""

P1_OUTRO = """
*下一篇，我们先把它和 RAG 的边界划清，再把这七个模块串成一条完整的执行链路：13 步分别做什么、会在哪里翻车，以及一套可落地的架构与伪代码。*
"""

P2_OUTRO = """
*下一篇是最后一篇：怎么评估研究质量、8 个典型应用场景、7 个未来趋势，以及给工程团队的 8 条落地建议。*
"""


def build_markdown() -> dict[str, str]:
    raw = SRC.read_text(encoding="utf-8")
    raw = re.sub(r"^\s*<!--.*?-->\s*", "", raw, flags=re.S)
    _title, rest = raw.split("\n", 1)

    i4 = rest.index("## 04 |")
    i8 = rest.index("## 08 |")

    p1_body = rest[:i4].rstrip()
    p2_body = rest[i4:i8].rstrip()
    p3_body = rest[i8:].rstrip()

    p1_body = p1_body.replace(
        "> 拆解研究型 Agent 的 7 个核心模块、13 步工作流与工程落地难点",
        f"> {P1_SUB}",
        1,
    )

    p2_intro = """上一篇我们拆了 Deep Research 的七个核心模块，回答了“它由什么组成”。

这一篇回答另一个问题：这些模块串起来，一次研究任务到底怎么跑？钱和时间花在哪？工程上最容易翻车的地方是什么？"""

    p3_intro = """前两篇讲了原理、模块、工作流和架构。最后一篇，我们把视角拉回业务：它到底能用在哪些场景？未来会往哪走？如果团队现在要动手，应该怎么起步？"""

    p3_body = p3_body.replace(
        "*下一篇准备拆解：如何为 Deep Research 构建一套可用的评估集。*",
        "*这个系列到这里就结束了。如果大家感兴趣，后面可以单独拆解：如何为 Deep Research 构建一套可用的评估集。*",
    )

    p1 = f"""{P1_NOTE}

# {P1_TITLE}

{p1_body}
{P1_OUTRO}"""

    p2 = f"""{P2_NOTE}

# {P2_TITLE}

> {P2_SUB}

{p2_intro}

---

{p2_body}
{P2_OUTRO}"""

    p3 = f"""{P3_NOTE}

# {P3_TITLE}

> {P3_SUB}

{p3_intro}

---

{p3_body}"""

    return {"part1": p1, "part2": p2, "part3": p3}


def main() -> None:
    OUT.mkdir(exist_ok=True)
    parts = build_markdown()

    for key, md in parts.items():
        md_path = OUT / f"{key}.md"
        md_path.write_text(md.strip() + "\n", encoding="utf-8")

        title = next(
            line[2:].strip()
            for line in md.splitlines()
            if line.startswith("# ")
        )
        body = md_to_html(md)
        html_path = OUT / f"{key}.html"
        html_path.write_text(html_document(title, body), encoding="utf-8")
        print(f"wrote {md_path.name} and {html_path.name}")

    # Also render the full long-form article as a single pasteable page.
    full_md = SRC.read_text(encoding="utf-8")
    full_title = next(
        line[2:].strip()
        for line in full_md.splitlines()
        if line.startswith("# ")
    )
    full_html = BASE / "deep-research-wechat.html"
    full_html.write_text(
        html_document(full_title, md_to_html(full_md)), encoding="utf-8"
    )
    print(f"wrote {full_html.name}")


if __name__ == "__main__":
    main()
