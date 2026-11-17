# CLAUDE.md — 大语言模型评估技术博客

本文件是后续 Claude Code 会话的工作指南。人类可读的项目交接见 `HANDOFF.md`。开始修改前，先读第 4 节「唯一事实来源」。

## 1. 项目是什么

一个中文技术博客项目，主题是 **《大语言模型评估体系详解：从基准测试到业务场景落地》**。面向有 LLM、机器学习、后端开发或 AI 应用经验的技术读者，要求技术细节充分、有工程视角、避免营销式表达。

文章的核心论点：

- 大模型评估是一套工程体系，不是单点指标；
- 评估要覆盖模型、任务、系统、业务四层；
- 离线评估、人工评估、LLM Judge、线上评估必须组合使用；
- 评估要接入研发流程和上线门禁，才能持续约束质量。

项目有两条交付线：

| 版本 | 文件 | 规模 | 用途 |
|---|---|---|---|
| 技术长文 | `大语言模型评估体系详解.md` | 1802 行 / 28133 汉字 / 42 表 / 13 代码块 | 原始深度版，结构最完整 |
| 公众号连载 | `wechat-series/part1–4.md/html` | 约 10441 汉字 / 32 表 / 8 图 / 47 文献 | 移动端发布版，可直接粘贴 |

## 2. 当前状态

**内容已完成，处于「待终审 / 待发布」阶段。**

- 长文：14 章，覆盖评估的重要性、评估对象、难点、方法、指标、RAG、Agent、评估集、平台架构、伪代码、Judge、报告、误区、总结。
- 公众号：4 篇连载，每篇 2 张配图，文末有参考文献；已做移动端排版，HTML 为内联样式。
- 配图：8 张 SVG 源文件 + 8 张 1500px 宽 2x PNG，已逐张人工检查。
- 参考文献：47 条（12 / 11 / 13 / 11），只保留作者、标题、会议或 arXiv 编号，无外链。
- 发布：尚未在真实公众号编辑器粘贴测试，未做封面图。
- Git：主体已提交；当前工作区有本次新增的 `HANDOFF.md`、`CLAUDE.md` 和 `README.md` 字数修正。

## 3. 文件地图

```text
llm_eval/
├── 大语言模型评估体系详解.md          # 技术长文（唯一长文源稿）
├── HANDOFF.md                         # 人类可读的项目交接
├── CLAUDE.md                          # 本文件
└── wechat-series/
    ├── README.md                      # 公众号发布说明、配图与文献清单
    ├── part1.md / part1.html          # 上篇：为什么评估、评什么、难在哪
    ├── part2.md / part2.html          # 中篇：六种方法与七类指标
    ├── part3.md / part3.html          # 下篇：RAG、Agent 与企业评估集
    ├── part4.md / part4.html          # 终篇：平台、伪代码、Judge、报告与门禁
    ├── build_wechat.py                # Markdown → 内联样式 HTML
    ├── render_diagrams.py             # SVG → 2x PNG（Playwright）
    └── images/
        ├── fig01-test-layers.svg/.png       # 上篇：三层测试
        ├── fig02-eval-layers.svg/.png       # 上篇：四层对象
        ├── fig03-method-pipeline.svg/.png   # 中篇：六种方法
        ├── fig04-correctness-reference.svg/.png  # 中篇：正确性参照物
        ├── fig05-rag-pipeline.svg/.png      # 下篇：RAG 两段
        ├── fig06-agent-trace.svg/.png       # 下篇：Agent 结果与过程
        ├── fig07-platform-flow.svg/.png     # 终篇：平台数据流
        └── fig08-gate-decision.svg/.png     # 终篇：上线门禁
```

**生成文件（不要直接编辑）**：

- `wechat-series/part1–4.html`
- `wechat-series/images/fig01–08.png`

下次运行构建 / 渲染脚本会被覆盖。

## 4. 唯一事实来源

- **长文**：`大语言模型评估体系详解.md`。所有长文内容修改只发生在这里。
- **公众号正文**：`wechat-series/part1.md`–`part4.md`。公众号版是独立压缩改写，不是从长文自动拆分的。
- **配图源文件**：`wechat-series/images/*.svg`。PNG 由 `render_diagrams.py` 生成。
- **图片引用**：公众号 Markdown 使用相对路径 `images/figNN-xxx.png`；HTML 与 `images/` 同目录，路径不需要加前缀。
- **图注格式**：图片下一行是纯斜体段落，例如 `*图 3：六种方法按成本和真实性组合使用。*`，渲染器会输出居中 14px 灰色注释。
- **参考文献**：每篇文末 `## 参考文献`，编号列表；渲染器会把该节的有序列表切换成 14px 文献样式。
- **公众号标题**：`# 大模型评估（一）…` 到 `# 大模型评估（四）…`，章节用 `## 01 | …` 编号。
- **长文标题**：一级标题为 `# 一、…` 到 `# 十四、…`；子节为 `## x.y`。

## 5. 常用命令

```bash
cd llm_eval/wechat-series

# Markdown → HTML
python3 build_wechat.py

# SVG → 2x PNG
python3 render_diagrams.py

# 本地预览
open part1.html
open part2.html
open part3.html
open part4.html
```

### 5.1 快速统计

```bash
cd llm_eval
python3 - <<'PY'
import re
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

当前基线：

```text
part1.md: 汉字 2553 / 表 5 / 代码块 0 / 图 2 / 文献 12
part2.md: 汉字 2814 / 表 11 / 代码块 1 / 图 2 / 文献 11
part3.md: 汉字 2694 / 表 12 / 代码块 4 / 图 2 / 文献 13
part4.md: 汉字 2380 / 表 4 / 代码块 2 / 图 2 / 文献 11
```

### 5.2 430px 手机宽度检查

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

期望值：每篇 2 张图、无破图、表格和代码块无溢出、`links` 与 `classes` 均为 0、`bodyScroll` 为 430。

## 6. 修改指南

### 6.1 改长文

1. 只改 `大语言模型评估体系详解.md`；
2. 保持 14 章结构和术语一致；
3. 改完运行第 5.1 节统计，确认表格、代码围栏、章节编号没有坏；
4. 如果改动涉及核心观点，同步检查公众号四篇是否需要更新。

### 6.2 改公众号正文

1. 改 `wechat-series/partX.md`，不要改 `partX.html`；
2. 运行 `python3 build_wechat.py`；
3. 用 430px 视口检查表格、代码块、图片和参考文献；
4. 如果新增图片，先改 SVG 并渲染 PNG，再在 Markdown 中引用；
5. 如果改动字数或文献数量，同步更新 `wechat-series/README.md` 和 `HANDOFF.md` 的基线数字。

### 6.3 改配图

1. 改 `images/*.svg`，不要改 PNG；
2. 运行 `python3 render_diagrams.py`；
3. 逐张查看 PNG，检查文字重叠、文本溢出、箭头压框；
4. 运行 `python3 build_wechat.py` 重新生成 HTML；
5. 同步更新 `README.md` 的配图清单和尺寸。

**命名与顺序坑**：

- `fig01-test-layers` 是上篇第一张（图 1，三层测试）；
- `fig02-eval-layers` 是上篇第二张（图 2，四层对象）。
- 曾因先插入四层图、后插入三层图导致编号颠倒；改图时先确认正文出现顺序，再编号。

### 6.4 改参考文献

1. 改对应 `partX.md` 末尾的 `## 参考文献` 列表；
2. 只写真实文献，保留作者、标题、会议 / 期刊或 arXiv 编号；
3. 公众号版不写外链；
4. 新增后运行 `build_wechat.py`；
5. 更新 `README.md` 和 `HANDOFF.md` 的文献数量；
6. 不确定的条目先用 arXiv、ACL Anthology、DBLP 核对，不要凭记忆补引用。

当前数量：12 / 11 / 13 / 11，共 47。

### 6.5 改样式

样式常量在 `build_wechat.py` 顶部：

- `S_WRAP` / `S_H1` / `S_H2` / `S_H3`
- `S_P` / `S_NOTE` / `S_BQ`
- `S_TABLE` / `S_TH` / `S_TD`
- `S_PRE` / `S_CODE`
- `S_REF_LI`

改完重新构建，并用 430px 视口预览。所有样式必须内联，不要加 `<style>` 或 class。

### 6.6 新增或拆分公众号篇目

- 新增篇目时，复制现有 `partX.md` 的标题、导语、承接语风格；
- 在 `build_wechat.py` 的 `PARTS` 列表中加入新文件名；
- 如果拆分，四篇的承接语、图号、文献编号要同步调整；
- 更新 `README.md` 的发布顺序和 `HANDOFF.md` 的篇章表；
- 不要让单篇超过约 3000 汉字，否则手机完读率会下降。

## 7. 公众号排版约束

这些是已经踩过的坑，新增内容时继续遵守：

- **表格最多 3 列**：4 列在手机上会挤；单元格文字尽量 ≤12 字。
- **代码行宽 ≤50 个 ASCII 字符**：中文行控制在 30 字以内。
- **段落 2–5 行**：避免手机上的文字墙。
- **不要加外链**：公众号会限制或剥离。
- **纯斜体段落**会被渲染成居中小字注释，只用于图注和文末 CTA；不要用它做正文强调。
- **不要加 `<style>` 或 class**：公众号编辑器只稳定保留内联样式。
- **图片是本地相对路径**：粘贴 HTML 后如果没自动带入，需要手动上传 PNG。
- **HTML 注释不会显示**：源稿里的发布备注转换后不可见。
- **参考文献用小字号**：`## 参考文献` 下的有序列表会自动用 14px。
- **构建器只支持有限 Markdown**：标题、段落、加粗、斜体、行内代码、无序 / 有序列表、表格、代码块、引用、图片、分隔线；不支持嵌套列表、复杂表格、原始 HTML。

## 8. 写作规范

### 8.1 风格

- 中文技术博客，先给结论，再讲机制，再给工程做法和失败模式；
- 每个核心概念尽量覆盖：职责、常见实现、工程挑战、与其他模块的关系；
- 允许明确说“这是工程经验”或“这是示意值”，不要伪装成实测结论；
- 不用“赋能、颠覆、革命性、最强”等营销词；
- 长段落拆短，表格用于对比，代码块用于可执行逻辑；
- 公众号版要比长文更短、更直接，保留结论和关键机制，删掉重复铺陈。

### 8.2 术语

保持全文一致：

| 术语 | 用法 |
|---|---|
| LLM / 大模型 | 首次出现可用“大语言模型（LLM）”，后文统一 |
| Benchmark | 不翻译；可括注“基准测试” |
| Golden Set | 不翻译；可括注“黄金测试集” |
| LLM Judge / LLM-as-a-Judge | 首次出现写全，后文可用 LLM Judge |
| Faithfulness | 忠实性，不写“忠实度”混用 |
| Answer Correctness | 答案正确性 |
| Context Relevance | 上下文相关性 |
| Trace | 不翻译 |
| RAG | 不翻译 |
| Agent | 不翻译；“智能体”只在必要处括注 |
| 门禁 | 不写“卡点”“准入门槛”混用 |
| 拒答 | 不写“拒绝回答”混用 |

### 8.3 事实与假设

- 数字一律标“示意”或“量级”，不写成 benchmark；
- 公开 Benchmark 只讲能力维度，不引用具体排名；
- 框架 / 产品 API 不绑定版本；
- 涉及安全能力时，明确边界，不承诺“绝对防护”；
- 引用外部事实时给来源；没有来源的推断要写明是推断；
- 参考文献只写真实存在的论文、标准或报告。

### 8.4 代码

- 长文伪代码保持 Python 风格，突出控制流，不追求可直接运行；
- 公众号伪代码行宽 ≤50 个 ASCII 字符，必要时手动断行；
- 不要把长文的大段代码直接粘到公众号版，先压缩到 40–70 行；
- 代码块使用 `python` / `json` / `text` 标注语言，Pygments 会高亮。

## 9. 配图规范

### 9.1 画布与输出

- 画布宽固定 **750px**，高度按内容定；
- 通过 `render_diagrams.py` 输出 **2x PNG**（1500px 宽）；
- 背景纯白 `#ffffff`；
- 字体统一：`'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif`；
- 可在根节点用一个 `<g font-family="...">` 包住所有文本，减少重复；
- SVG 根元素必须写成 `<svg ... width="750" height="H" viewBox="0 0 750 H">`，渲染脚本靠这个读尺寸。

### 9.2 字号与层级

| 层级 | 字号 | 颜色 |
|---|---|---|
| 主标题 | 26–30，bold | `#0f172a` |
| 副标题 | 15–16 | `#64748b` |
| 模块标题 | 18–22，bold | `#0f172a` / `#1e3a8a` |
| 正文标签 | 14–17 | `#334155` / `#475569` |
| 注释 / 次要说明 | 13–15 | `#64748b` / `#94a3b8` |

注意：750px 画布在手机上会缩到约 390px，20px 文字只剩约 10px。关键信息不要小于 14px，主标签尽量 18px 以上。

### 9.3 配色

| 用途 | 色值 |
|---|---|
| 深色主块 / 标题 | `#0f172a` |
| 主流程蓝 | `#2563eb`，浅底 `#eff6ff`，边框 `#bfdbfe` |
| 能力 / 结果青 | `#0f766e`，浅底 `#f0fdfa`，边框 `#99f6e4` |
| 反馈 / 警示橙 | `#d97706`，浅底 `#fffbeb`，边框 `#fcd34d` |
| 协作紫 | `#7c3aed`，浅底 `#f5f3ff`，边框 `#c4b5fd` |
| 风险红 | `#dc2626`，浅底 `#fef2f2`，边框 `#fca5a5` |
| 中性灰 | 文字 `#64748b`，底 `#f8fafc`，边框 `#e2e8f0` |

一屏内不要超过 3 种强调色，否则层级会乱。

### 9.4 连线与形状

- 主流程：实线，`stroke-width` 2–2.4，灰色箭头；
- 反馈 / 回流：虚线 `stroke-dasharray="5 4"` 或 `"4 4"`，橙色箭头；
- 箭头 marker 尺寸 6–8，`refX` 设为 7–8，避免箭头压住框线；
- 圆角：小卡片 9–10，大卡片 12–16，胶囊 16–17；
- 文本放在框内时，baseline 要比框中心高约 5–7px，避免视觉偏下。

### 9.5 图注与命名

- 文件名 `figNN-slug.svg`，与正文出现顺序一致；
- 图注格式固定为 `*图 N：一句话说明。*`；
- 图注放在图片下一行，前后各空一行；
- 图注不重复正文原句，只补充“这张图在说什么”；
- 图内标题可以保留，但不要和图注完全重复；图内标题用于单独查看，图注用于正文语境。

## 10. 验证清单

每次改完内容或图，至少检查：

1. `python3 build_wechat.py` 无报错，四篇 HTML 都生成；
2. `python3 render_diagrams.py` 无报错，8 张 PNG 均为 1500px 宽；
3. 每篇 2 张图，`naturalWidth` 均为 1500，无破图；
4. 表格最多 3 列，430px 下无横向溢出；
5. 代码块无横向溢出，单行 ≤50 个 ASCII 字符；
6. HTML 中没有 `href`、没有 `class`；
7. 参考文献数量为 12 / 11 / 13 / 11；
8. 四篇承接语与发布顺序一致；
9. 图片引用路径与文件名大小写一致；
10. 改动字数或文献数量后，`README.md` 和 `HANDOFF.md` 的基线数字同步更新；
11. 长文仍为 14 章，章节编号连续；
12. 新增内容没有破坏公众号版的“短段落、少表格列、无外链”约束。

## 11. 待办与下一步

完整清单见 `HANDOFF.md` 第 10 节，摘要：

**P0**

- 终审四篇：承接语、图注、文献格式、数字口径；
- 在真实公众号编辑器粘贴一次，确认表格、代码块、图片和参考文献样式；
- 图片未自动带入时手动上传 8 张 PNG；
- 准备封面图；
- 提交 `HANDOFF.md`、`CLAUDE.md` 和 `README.md` 字数修正。

**P1**

- 给长文补参考文献（目前只有公众号版有）；
- 增加系列目录 / 导航；
- 可选：合并为单篇长版 HTML；
- 可选：补 1–2 张场景图或封面图；
- 可选：给长文补可运行的真实代码示例。

**P2**

- `.gitignore` 忽略 `.DS_Store`；
- 从索引移除已跟踪的 `llm_eval/.DS_Store`；
- 根 `README.md` 增加文章索引；
- 统一三篇技术博客的发布说明格式。

## 12. 已知限制

- **数字是示意值**：准确率、延迟、成本、样本量均为量级示意，不是实测或 benchmark。
- **参考文献不是逐条引用**：正文没有 `[1]` 标注，文献作为来源和延伸阅读。
- **公众号编辑器未实测**：HTML 是本地浏览器验证，公众号可能改写部分样式。
- **图片是本地相对路径**：粘贴到公众号后可能需要手动上传。
- **图片文字偏小**：1500px 图在手机上显示约 390px，关键文字约 9–12px。
- **公众号版是压缩改写**：与长文不完全逐段对应，改内容时注意同步两边。
- **构建器只支持有限 Markdown**：不要用嵌套列表、复杂表格、原始 HTML。
- **表格最多 3 列**：4 列会在手机上挤。
- **代码高亮依赖 Pygments**：公众号可能保留也可能改写颜色，发布前需预览。
- **没有自动发布链路**：本地生成 HTML + 手动粘贴。

## 13. 与其他项目的关系

- `../llm_agent/`：同仓库的 Agent 长文，有 7 张配图和完整交接文档，可作为 SVG→PNG、图注、验证清单的格式参考。
- `../deep_research/`：同仓库的 Deep Research 公众号连载版，有 `build_wechat_series.py`、内联样式 HTML 和三篇连载，可作为公众号构建链路参考。
- 三个项目的写作风格一致：中文、工程视角、先结论后机制、拒绝营销表达。
- **不要复用 `deep_research` 的切分脚本**：它的切分点是为那篇文章硬编码的；本项目四篇是独立源稿，不自动拆分。
- 根 `README.md` 目前只有项目名，未做文章索引；如需统一入口，可在 P2 中补。
