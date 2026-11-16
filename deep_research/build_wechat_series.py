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
S_REF_LI = (
    "margin:0 0 10px;line-height:1.75;font-size:14px;color:#475569;"
    "text-align:left;"
)
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


def md_to_html(md: str, img_prefix: str = "") -> str:
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    n = len(lines)
    in_refs = False

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
            raw_text = m.group(2).strip()
            if level <= 2:
                in_refs = raw_text == "参考文献"
            text = inline(raw_text)
            styles = {1: S_H1, 2: S_H2, 3: S_H3, 4: S_H3}
            out.append(f'<h{level} style="{styles[level]}">{text}</h{level}>')
            i += 1
            continue

        # horizontal rule
        if stripped == "---":
            out.append(f'<hr style="{S_HR}">')
            i += 1
            continue

        # image
        m = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)$", stripped)
        if m:
            alt = htmlmod.escape(m.group(1), quote=True)
            src = htmlmod.escape(img_prefix + m.group(2), quote=True)
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
            li_style = S_REF_LI if in_refs else S_LI
            while i < n and re.match(r"^\d+\.\s+", lines[i].strip()):
                item = re.sub(r"^\d+\.\s+", "", lines[i].strip())
                items.append(f'<li style="{li_style}">{inline(item)}</li>')
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

REF_INTRO = (
    "以下文献是本文方法与观点的主要来源，也可作为延伸阅读；"
    "未在正文中逐条标注引用。为便于公众号阅读，仅保留 arXiv 编号与发表信息，未附外链。"
)

P1_REFS = [
    "Yao, S., et al. ReAct: Synergizing Reasoning and Acting in Language Models. ICLR 2023. arXiv:2210.03629.",
    "Nakano, R., et al. WebGPT: Browser-assisted question-answering with human feedback. arXiv:2112.09332, 2021.",
    "Schick, T., et al. Toolformer: Language Models Can Teach Themselves to Use Tools. NeurIPS 2023. arXiv:2302.04761.",
    "Lewis, P., et al. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. NeurIPS 2020. arXiv:2005.11401.",
    "Gao, Y., et al. Retrieval-Augmented Generation for Large Language Models: A Survey. arXiv:2312.10997, 2023.",
    "Asai, A., et al. Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection. ICLR 2024. arXiv:2310.11511.",
    "Yan, S.-Q., et al. Corrective Retrieval Augmented Generation. arXiv:2401.15884, 2024.",
    "Gao, L., et al. Precise Zero-Shot Dense Retrieval without Relevance Labels. ACL 2023. arXiv:2212.10496.",
    "Cormack, G. V., Clarke, C. L. A., & Büttcher, S. Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods. SIGIR 2009.",
    "Liu, N. F., et al. Lost in the Middle: How Language Models Use Long Contexts. TACL 2024. arXiv:2307.03172.",
    "Huang, Y., et al. Deep Research Agents: A Systematic Examination and Roadmap. arXiv:2506.18096, 2025.",
    "OpenAI. Deep Research System Card. 2025.",
]

P2_REFS = [
    "Yao, S., et al. ReAct: Synergizing Reasoning and Acting in Language Models. ICLR 2023. arXiv:2210.03629.",
    "Wang, L., et al. Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large Language Models. ACL 2023. arXiv:2305.04091.",
    "Yao, S., et al. Tree of Thoughts: Deliberate Problem Solving with Large Language Models. NeurIPS 2023. arXiv:2305.10601.",
    "Shinn, N., et al. Reflexion: Language Agents with Verbal Reinforcement Learning. NeurIPS 2023. arXiv:2303.11366.",
    "Madaan, A., et al. Self-Refine: Iterative Refinement with Self-Feedback. NeurIPS 2023. arXiv:2303.17651.",
    "Dhuliawala, S., et al. Chain-of-Verification Reduces Hallucination in Large Language Models. ACL Findings 2024. arXiv:2309.11495.",
    "Es, S., et al. RAGAS: Automated Evaluation of Retrieval Augmented Generation. EACL 2024 Demo. arXiv:2309.15217.",
    "Zheng, L., et al. Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. NeurIPS 2023. arXiv:2306.05685.",
    "Du, M., et al. DeepResearch Bench: A Comprehensive Benchmark for Deep Research Agents. arXiv:2506.11763, 2025.",
    "Wei, J., et al. BrowseComp: A Simple Yet Challenging Benchmark for Browsing Agents. arXiv:2504.12516, 2025.",
    "Mialon, G., et al. GAIA: A Benchmark for General AI Assistants. ICLR 2024. arXiv:2311.12983.",
    "Zheng, Y., et al. DeepResearcher: Scaling Deep Research via Reinforcement Learning in Real-world Environments. EMNLP 2025. arXiv:2504.03160.",
]

P3_REFS = [
    "Mialon, G., et al. GAIA: A Benchmark for General AI Assistants. ICLR 2024. arXiv:2311.12983.",
    "Wei, J., et al. BrowseComp: A Simple Yet Challenging Benchmark for Browsing Agents. arXiv:2504.12516, 2025.",
    "Du, M., et al. DeepResearch Bench: A Comprehensive Benchmark for Deep Research Agents. arXiv:2506.11763, 2025.",
    "Phan, L., et al. Humanity's Last Exam. arXiv:2501.14249, 2025.",
    "Min, S., et al. FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation. EMNLP 2023. arXiv:2305.14251.",
    "Bohnet, B., et al. Attributed Question Answering: Evaluation and Modeling for Attributed Large Language Models. arXiv:2212.08037, 2022.",
    "Es, S., et al. RAGAS: Automated Evaluation of Retrieval Augmented Generation. EACL 2024 Demo. arXiv:2309.15217.",
    "Zheng, L., et al. Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. NeurIPS 2023. arXiv:2306.05685.",
    "Huang, Y., et al. Deep Research Agents: A Systematic Examination and Roadmap. arXiv:2506.18096, 2025.",
    "Jin, B., et al. Search-R1: Training LLMs to Reason and Leverage Search Engines with Reinforcement Learning. COLM 2025. arXiv:2503.09516.",
    "Li, X., et al. WebThinker: Empowering Large Reasoning Models with Deep Research Capability. NeurIPS 2025. arXiv:2504.21776.",
    "Zheng, Y., et al. DeepResearcher: Scaling Deep Research via Reinforcement Learning in Real-world Environments. EMNLP 2025. arXiv:2504.03160.",
    "OpenAI. Deep Research System Card. 2025.",
]


def refs_section(refs: list[str]) -> str:
    lines = ["---", "", "## 参考文献", "", REF_INTRO, ""]
    lines.extend(f"{i}. {ref}" for i, ref in enumerate(refs, 1))
    return "\n".join(lines)


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

    p1 = p1.rstrip() + "\n\n" + refs_section(P1_REFS)
    p2 = p2.rstrip() + "\n\n" + refs_section(P2_REFS)
    p3 = p3.rstrip() + "\n\n" + refs_section(P3_REFS)

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
    all_refs = list(dict.fromkeys(P1_REFS + P2_REFS + P3_REFS))
    full_with_refs = full_md.rstrip() + "\n\n" + refs_section(all_refs)
    full_html = BASE / "deep-research-wechat.html"
    full_html.write_text(
        html_document(
            full_title,
            md_to_html(full_with_refs, img_prefix="wechat-series/"),
        ),
        encoding="utf-8",
    )
    print(f"wrote {full_html.name}")


if __name__ == "__main__":
    main()
