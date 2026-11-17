# 大语言模型评估体系 — 项目交接

> **交接日期**：2026-11-17  
> **当前状态**：长文、公众号四篇连载、8 张配图、47 条参考文献均已完成；已提交主体内容，待终审与发布  
> **适用对象**：内容维护者、发布运营、接手的工程师

## 1. 项目一句话

一个面向有 LLM、机器学习、后端开发或 AI 应用经验的技术读者的中文技术博客，主题是 **《大语言模型评估体系详解：从基准测试到业务场景落地》**。

核心观点：

- 大模型评估是一套工程体系，不是单点指标；
- 评估要覆盖模型、任务、系统、业务四层；
- 离线评估、人工评估、LLM Judge、线上评估必须组合使用；
- 评估要接入研发流程和上线门禁，才能持续约束质量。

项目有两条交付线：

1. **技术长文**：结构完整，14 章，适合博客 / 知识库；
2. **公众号连载**：4 篇，移动端排版，带配图和参考文献，可直接粘贴。

## 2. 交付物清单

| 文件 | 说明 | 规模 | 状态 |
|---|---|---|---|
| `大语言模型评估体系详解.md` | 技术长文，14 章 | 1802 行 / 28133 汉字 / 约 123 KB | 完成 |
| `wechat-series/part1.md` | 公众号上篇源稿 | 2553 汉字 / 5 表 / 2 图 / 12 文献 | 完成 |
| `wechat-series/part2.md` | 公众号中篇源稿 | 2814 汉字 / 11 表 / 2 图 / 11 文献 | 完成 |
| `wechat-series/part3.md` | 公众号下篇源稿 | 2694 汉字 / 12 表 / 2 图 / 13 文献 | 完成 |
| `wechat-series/part4.md` | 公众号终篇源稿 | 2380 汉字 / 4 表 / 2 图 / 11 文献 | 完成 |
| `wechat-series/part1–4.html` | 内联样式 HTML，可直接粘贴 | 38–63 KB / 篇 | 完成 |
| `wechat-series/images/fig01–08.svg` | 8 张配图矢量源文件 | 2.7–3.9 KB / 张 | 完成 |
| `wechat-series/images/fig01–08.png` | 8 张配图 2x PNG | 1500px 宽，84–132 KB | 完成 |
| `wechat-series/build_wechat.py` | Markdown → 内联样式 HTML | 385 行 | 可用 |
| `wechat-series/render_diagrams.py` | SVG → 2x PNG（Playwright） | 63 行 | 可用 |
| `wechat-series/README.md` | 公众号发布说明 | — | 完成 |
| `CLAUDE.md` | 后续 Claude Code 会话工作指南 | — | 完成 |

公众号四篇合计约 **10441 汉字**、**32 张表**、**7 个代码块**、**8 张图**、**47 条参考文献**。

## 3. 内容结构

### 3.1 技术长文

| 章节 | 核心内容 |
|---|---|
| 一、引言 | 输出不确定性、传统测试失效、评估目标、知识库问答例子 |
| 二、评什么 | 模型能力、任务效果、系统级、业务级四层 |
| 三、为什么难 | 10 个难点：非确定性、答案不唯一、语义判断、边界、长文、幻觉、污染、榜单脱节、人工成本、Judge 偏差 |
| 四、评估方法 | Benchmark、Golden Set、人工、自动指标、LLM Judge、A/B |
| 五、指标体系 | 正确性、相关性、完整性、指令遵循、安全、效率、稳定性 |
| 六、RAG 评估 | 检索 / 生成拆分、指标、故障诊断、评估集设计 |
| 七、Agent 评估 | 任务成功率、规划、工具、Trace、安全、难点 |
| 八、企业评估集 | 数据来源、样本设计、标注 Schema、分层、维护 |
| 九、平台架构 | 10 个模块、完整数据流、CI/CD 门禁 |
| 十、伪代码 | 加载、运行、指标、Judge、聚合、报告、门禁 |
| 十一、Judge Prompt | 中文模板、6 个维度、JSON 输出、反偏差规则 |
| 十二、评估报告 | 报告模板与写作原则 |
| 十三、常见误区 | 10 个误区及正确做法 |
| 十四、总结 | 5 条结论 + 14 条落地建议 |

### 3.2 公众号连载

| 篇 | 标题 | 覆盖长文章节 | 配图 | 文献 |
|---|---|---|---|---|
| 上篇 | 大模型评估（一）：为什么“感觉不错”不能作为上线依据 | §1–§3 | 图 1–2 | 12 |
| 中篇 | 大模型评估（二）：六种方法，别只盯着 Benchmark | §4–§5 | 图 3–4 | 11 |
| 下篇 | 大模型评估（三）：RAG 与 Agent，必须拆开评 | §6–§8 | 图 5–6 | 13 |
| 终篇 | 大模型评估（四）：把评估接进研发流程 | §9–§14 | 图 7–8 | 11 |

公众号版是对长文的压缩改写，不是逐段搬运。四篇各自独立成文，结尾有连载承接。

## 4. 公众号适配方式

原长文 2.8 万字，单篇公众号会过长，因此拆成 4 篇，每篇约 2400–2800 汉字。

已做的移动端适配：

- 表格最多 3 列，单元格文字尽量短；
- 代码行宽控制在 50 个 ASCII 字符以内；
- 段落控制在 2–5 行；
- 文内无外链；
- HTML 全部内联样式，无 `<style>`、无 class；
- 参考文献 14px 小字号，正文列表 16px；
- 配图 1500px 宽 2x PNG，手机上显示约 390px；
- 每篇 2 张图，放在概念转折处，图注为居中灰色小字。

已在 430px 视口验证：表格和代码块无横向溢出，图片正常加载，页面无横向滚动。

## 5. 配图清单

| 图 | 文件 | 放置位置 | 内容 | 2x 尺寸 |
|---|---|---|---|---|
| 图 1 | `images/fig01-test-layers.png` | 上篇 §02 | 确定性、语义、统计三层测试 | 1500×1040 |
| 图 2 | `images/fig02-eval-layers.png` | 上篇 §04 | 评估的四层对象 | 1500×1120 |
| 图 3 | `images/fig03-method-pipeline.png` | 中篇 §01 | 六种方法的组合顺序 | 1500×1200 |
| 图 4 | `images/fig04-correctness-reference.png` | 中篇 §08 | 正确性的四个参照物 | 1500×1040 |
| 图 5 | `images/fig05-rag-pipeline.png` | 下篇 §01 | RAG 检索与生成两段 | 1500×1160 |
| 图 6 | `images/fig06-agent-trace.png` | 下篇 §08 | Agent 结果与过程评估 | 1500×1120 |
| 图 7 | `images/fig07-platform-flow.png` | 终篇 §01 | 评估平台数据流与回流 | 1500×1400 |
| 图 8 | `images/fig08-gate-decision.png` | 终篇 §03 | 上线门禁的三层判断 | 1500×1200 |

**注意**：PNG 是渲染产物，不要手改。所有图的修改都落在 SVG，再运行 `render_diagrams.py`。

## 6. 参考文献

四篇文末共 47 条：

| 篇 | 数量 | 主要来源 |
|---|---|---|
| 上篇 | 12 | MMLU、GSM8K、HumanEval、TruthfulQA、HellaSwag、C-Eval、CMMLU、HELM、Lost in the Middle、综述、数据污染、LLM Judge |
| 中篇 | 11 | BLEU、ROUGE、BERTScore、COMET、MT-Bench/Judge、Fair Evaluators、G-Eval、Prometheus、Chatbot Arena、HELM、Cohen's kappa |
| 下篇 | 13 | RAG、RAGAS、ARES、Lost in the Middle、HyDE、Self-RAG、CRAG、ReAct、Reflexion、AgentBench、WebArena、SWE-bench、τ-bench |
| 终篇 | 11 | HELM、Judge、RAGAS、Model Cards、Datasheets、ML Test Score、Hidden Technical Debt、NIST AI RMF、ISO/IEC 42001、BIG-bench、LiveCodeBench |

维护约定：

- 只写真实存在的论文、标准或报告；
- 保留作者、标题、会议 / 期刊或 arXiv 编号；
- 公众号版**不写外链**；
- 文献是方法与观点来源和延伸阅读，正文没有逐条标注引用；
- 新增文献前先用 arXiv、ACL Anthology、DBLP 核对，不凭记忆补引用。

## 7. 构建与验证

### 7.1 生成 HTML

```bash
cd llm_eval/wechat-series
python3 build_wechat.py
```

脚本读取 `part1.md`–`part4.md`，生成同名 HTML。

### 7.2 重新渲染配图

```bash
cd llm_eval/wechat-series
python3 render_diagrams.py
```

脚本读取 `images/*.svg`，生成 2x PNG。

修改顺序：

```text
改 SVG → render_diagrams.py → 检查 PNG → build_wechat.py
```

或：

```text
改 Markdown → build_wechat.py → 浏览器预览
```

### 7.3 快速统计

```bash
cd llm_eval
python3 - <<'PY'
import re, unicodedata
from pathlib import Path

def stat(path):
    s = path.read_text(encoding="utf-8")
    lines = s.splitlines()
    inf = False
    block = []
    tables = 0
    code = 0
    fence = "`" * 3
    for line in lines:
        if line.startswith(fence):
            if inf:
                code += 1
            inf = not inf
            continue
        if inf:
            continue
        if line.startswith("|"):
            block.append(line)
        elif block:
            tables += 1
            block = []
    if block:
        tables += 1
    imgs = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", s)
    missing = [x for x in imgs if not (path.parent / x).exists()]
    refs = 0
    if "## 参考文献" in s:
        tail = s.split("## 参考文献", 1)[1]
        refs = len(re.findall(r"^\d+\.\s+", tail, re.M))
    print(path.name, "汉字", len(re.findall(r"[一-鿿]", s)),
          "表格", tables, "代码块", code, "图", len(imgs),
          "缺图", missing or "无", "文献", refs)

for p in sorted(Path("wechat-series").glob("part*.md")):
    stat(p)
PY
```

### 7.4 手机宽度检查

```bash
cd llm_eval/wechat-series
python3 - <<'PY'
from pathlib import Path
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 430, "height": 900})
    for f in sorted(Path(".").glob("part*.html")):
        page.goto(f.resolve().as_uri())
        page.wait_for_timeout(100)
        info = page.evaluate("""() => ({
          tables: document.querySelectorAll('table').length,
          tableOverflow: [...document.querySelectorAll('table')]
            .filter(t => t.scrollWidth > t.clientWidth + 1).length,
          preOverflow: [...document.querySelectorAll('pre')]
            .filter(t => t.scrollWidth > t.clientWidth + 1).length,
          brokenImages: [...document.querySelectorAll('img')]
            .filter(i => !i.complete || i.naturalWidth === 0).length,
          links: document.querySelectorAll('a').length,
          classes: document.querySelectorAll('[class]').length,
          bodyScroll: document.body.scrollWidth
        })""")
        print(f.name, info)
    b.close()
PY
```

当前基线：

```text
part1: 图 2 / 表 5 / 文献 12 / 无溢出 / 无外链 / bodyScroll 430
part2: 图 2 / 表 11 / 文献 11 / 无溢出 / 无外链 / bodyScroll 430
part3: 图 2 / 表 12 / 文献 13 / 无溢出 / 无外链 / bodyScroll 430
part4: 图 2 / 表 4 / 文献 11 / 无溢出 / 无外链 / bodyScroll 430
```

## 8. 当前验证结果

- 四篇 HTML 均可生成，图片全部加载；
- 8 张 PNG 均为 1500px 宽，尺寸见第 5 节；
- 表格最多 3 列，430px 下无横向溢出；
- 代码块行宽均 ≤50 个 ASCII 字符，无横向溢出；
- HTML 中无 `href`、无 `class`；
- 参考文献数量 12 / 11 / 13 / 11；
- 正文承接语与发布顺序一致；
- 长文 14 章、42 表、13 个代码块、28133 汉字。

**尚未验证**：

- 没有在真实公众号编辑器中粘贴测试；
- 图片粘贴后是否自动上传未验证，可能需要手动上传 PNG；
- 没有做公众号深色模式 / 不同机型适配；
- 没有准备封面图。

## 9. Git 状态

当前分支：`dev_blog_20261116`

最近提交：

```text
4670625 增加参考文献
1706c51 第一版完成，以及微信公众号版本已完成
f139386 配图与进度交接
77b0949 大语言模型Agent技术详解初版
```

`llm_eval` 目录已纳入 git。当前工作区：

- `HANDOFF.md`、`CLAUDE.md` 为本次新增；
- `wechat-series/README.md` 有字数修正，尚未提交；
- 根目录 `../.DS_Store` 未跟踪；
- `llm_eval/.DS_Store` 被误跟踪，建议后续从索引移除。

## 10. 待办

### P0：发布前

- [ ] 终审四篇：承接语、图注、文献格式、数字口径；
- [ ] 在公众号编辑器实际粘贴一次，确认表格、代码块、图片和参考文献样式；
- [ ] 如果图片未自动带入，手动上传 8 张 PNG；
- [ ] 准备封面图（4 篇或系列封面）；
- [ ] 确认发布顺序与标题；
- [ ] 提交 `HANDOFF.md`、`CLAUDE.md` 和 `README.md` 的字数修正。

### P1：可选优化

- [ ] 给长文补参考文献（目前只有公众号版有）；
- [ ] 增加系列目录 / 导航；
- [ ] 把四篇合并为单篇长版 HTML，作为备用；
- [ ] 补 1–2 张场景图或封面图；
- [ ] 给长文补可运行的真实代码示例（目前只有伪代码）。

### P2：仓库清理

- [ ] 加 `.gitignore` 忽略 `.DS_Store`；
- [ ] 从索引移除已跟踪的 `llm_eval/.DS_Store`；
- [ ] 根 `README.md` 增加文章索引；
- [ ] 如需要，统一 `llm_agent`、`deep_research`、`llm_eval` 三篇的发布说明格式。

## 11. 已知限制

1. **数字是示意值**：准确率、延迟、成本、样本量均为量级示意，不是实测或 benchmark。
2. **参考文献不是逐条引用**：正文没有 `[1]` 标注，文献作为来源和延伸阅读。
3. **公众号编辑器未实测**：HTML 是本地浏览器验证，公众号可能改写部分样式。
4. **图片是本地相对路径**：粘贴到公众号后可能需要手动上传。
5. **图片文字偏小**：1500px 图在手机上显示约 390px，关键文字约 9–12px；可读，但不是无障碍级。
6. **公众号版是压缩改写**：与长文不完全逐段对应，改内容时注意同步两边。
7. **构建器只支持有限 Markdown**：标题、段落、加粗、斜体、行内代码、列表、表格、代码块、引用、图片、分隔线；不支持嵌套列表、复杂表格、HTML 片段。
8. **表格最多 3 列**：4 列会在手机上挤，构建器虽能渲染，但不符合排版约束。
9. **代码高亮依赖 Pygments**：公众号可能保留也可能改写颜色，发布前需预览。
10. **没有自动发布链路**：目前是本地生成 HTML + 手动粘贴。

## 12. 接手快速上手

建议按这个顺序花 20–30 分钟熟悉：

1. 读 `CLAUDE.md` 的「唯一事实来源」「修改指南」「验证清单」；
2. 浏览器打开 `wechat-series/part1.html`，用 430px 视口看一遍；
3. 读 `wechat-series/part1.md`，理解公众号版的压缩程度和语气；
4. 看 `wechat-series/images/` 下 8 张 PNG，确认图文对应；
5. 运行 `python3 build_wechat.py` 和 `python3 render_diagrams.py`，确认链路可用；
6. 读本文件第 10 节的 P0 待办，决定发布形态；
7. 要改内容只改 Markdown，要改图只改 SVG，不要手改 HTML / PNG。

## 13. 相关文档

- `CLAUDE.md`：后续 Claude Code 会话的工作指南，含文件地图、命令、修改规则、写作与配图规范、验证清单。
- `wechat-series/README.md`：公众号发布说明、配图清单、参考文献维护约定。
- `../llm_agent/CLAUDE.md`、`../llm_agent/HANDOFF.md`：同仓库另一篇长文的交接格式参考。
- `../deep_research/CLAUDE.md`：公众号构建链路与移动端排版约束参考。
