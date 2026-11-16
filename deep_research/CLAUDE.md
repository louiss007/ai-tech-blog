# CLAUDE.md — Deep Research 技术博客

本文件是后续 Claude Code 会话的工作指南；人类可读的项目交接见 `HANDOFF.md`。开始修改前先读「唯一事实来源」一节。

## 1. 项目是什么

一个中文技术博客项目，主题是 **Deep Research：从信息检索到多步推理的 AI 研究型 Agent**。面向有 AI、大模型或后端基础的工程师，要求技术细节充分、避免营销式表达。

项目现在有三份成稿，分两条发布线：

| 版本 | 文件 | 规模 | 用途 |
|---|---|---|---|
| 技术长文 | `deep-research-technical-deep-dive.md` | 约 1.8 万汉字，1900+ 行 | 原始深度版，结构最完整 |
| 公众号完整版 | `deep-research-wechat.md` | 约 8000 汉字 | 公众号长文源稿，构建脚本的输入 |
| 公众号连载版 | `wechat-series/part1–3.md/html` | 约 4700 / 2000 / 1700 汉字 | 三篇可独立发布的连载 |

公众号版本已经做了：移动端排版、三张配图、三篇各自的参考文献、可直接粘贴的 HTML。

## 2. 当前状态

**内容已完成，处于「待发布 / 待终审」阶段。**

- 上篇：01–03，为什么需要 Deep Research、定义、7 个核心模块；含「七模块总架构图」；12 条参考文献。
- 中篇：04–07，RAG 对比、13 步工作流、6 个工程难点、可落地架构与伪代码；含「13 步工作流图」；12 条参考文献。
- 下篇：08–11，评估、8 个应用场景、7 个趋势、总结与 8 条落地建议；含「评估流程图」；13 条参考文献。
- 完整版 HTML 含 3 张图、28 条去重后的参考文献。
- HTML 已用 430×900 视口检查：图片能加载、表格不竖排、代码块不横向溢出、无外部链接。
- 最近提交：`0830d82 给part3评估部分配图`。已有稿件和三张图都已纳入 git；本次新增的 `CLAUDE.md` 与 `render_diagrams.py` 尚未提交。仓库里还跟踪了 `.DS_Store`，可择机清理。

## 3. 文件地图

```
deep_research/
├── CLAUDE.md                          # 本文件（Claude Code 工作指南）
├── HANDOFF.md                         # 人类可读的项目交接文档
├── deep-research-technical-deep-dive.md  # 原始技术长文（不参与构建）
├── deep-research-wechat.md            # 公众号正文源稿（构建输入）
├── build_wechat_series.py             # 拆分 + Markdown→内联样式 HTML
├── render_diagrams.py                 # SVG→2x PNG（Playwright）
├── deep-research-wechat.html          # 生成：完整版 HTML
└── wechat-series/
    ├── README.md                      # 发布说明（给运营/作者看）
    ├── part1.md / part1.html          # 生成：上篇
    ├── part2.md / part2.html          # 生成：中篇
    ├── part3.md / part3.html          # 生成：下篇
    └── images/
        ├── part1-architecture.svg/png # 上篇：七模块总架构图
        ├── part2-workflow.svg/png     # 中篇：13 步工作流图
        └── part3-evaluation.svg/png   # 下篇：评估流程图
```

**生成文件（不要直接编辑）**：`deep-research-wechat.html`、`wechat-series/part1–3.md`、`wechat-series/part1–3.html`。下次运行构建脚本会被覆盖。

## 4. 唯一事实来源与生成链路

### 4.1 正文

- 公众号正文的唯一源稿是 **`deep-research-wechat.md`**。
- `build_wechat_series.py` 读取它，按两个 H2 标题切成三篇：
  - `## 04 |` 之前 → 上篇
  - `## 04 |` 到 `## 08 |` 之前 → 中篇
  - `## 08 |` 到文末 → 下篇
- 如果你新增或移动章节，必须同步检查这两个切分点；否则三篇内容会错位。
- 每篇的标题、副标题、开场承接、文末预告、参考文献，不在源稿里，而在 `build_wechat_series.py` 的常量中：
  - `P1_TITLE` / `P1_SUB` / `P1_NOTE` / `P1_OUTRO` / `P1_REFS`
  - `P2_*`、`P3_*` 同理

### 4.2 HTML

`build_wechat_series.py` 的小型 Markdown 渲染器支持：

- `#` / `##` / `###` 标题
- 段落、加粗、斜体、行内代码
- 无序/有序列表
- 表格（渲染为固定列宽，2/3/4 列有预设宽度）
- 围栏代码块（Pygments，monokai，内联样式）
- 引用块、分隔线、图片
- 纯斜体段落 → 居中 14px 灰色注释（用于图注和文末 CTA）
- `## 参考文献` 下的有序列表 → 14px 小字号文献样式

所有样式都内联在元素上，没有 `<style>`、没有 class，方便公众号编辑器保留。

### 4.3 图片

- 图片源文件是 `wechat-series/images/*.svg`；PNG 是 2x 渲染产物，不要手改 PNG。
- 修改 SVG 后运行：

```bash
python3 render_diagrams.py
```

- 构建脚本会自动处理图片路径：
  - 分篇 HTML 在 `wechat-series/` 下，`src="images/xxx.png"`；
  - 完整版 HTML 在项目根目录，构建时自动加前缀 `wechat-series/`。

## 5. 常用命令

```bash
# 重新拆分并生成三篇 + 完整版 HTML
python3 build_wechat_series.py

# 修改 SVG 后重新渲染三张 PNG
python3 render_diagrams.py

# 快速本地预览
open wechat-series/part1.html
open wechat-series/part2.html
open wechat-series/part3.html
```

## 6. 修改指南

### 6.1 改正文

1. 改 `deep-research-wechat.md`；
2. 运行 `python3 build_wechat_series.py`；
3. 检查三篇 HTML 的对应位置。

不要改 `wechat-series/partX.md`，它会在下次构建时被覆盖。

### 6.2 改某篇的标题、导语、结尾

改 `build_wechat_series.py` 顶部的 `P1_TITLE`、`P1_SUB`、`P1_OUTRO` 等常量，然后重新构建。上篇的导语来自源稿，中篇/下篇的承接语在 `build_markdown()` 的 `p2_intro`、`p3_intro` 中。

### 6.3 加/改参考文献

改 `P1_REFS`、`P2_REFS`、`P3_REFS` 三个列表，重新构建。注意：

- 文献是「主要来源 + 延伸阅读」，正文没有逐条标引用；开头已有说明。
- 只用真实存在的论文/报告，保留作者、标题、会议或 arXiv 编号。
- 为适配公众号，不写外链；arXiv 编号写成 `arXiv:xxxx.xxxxx`。
- 2025 年之后的论文/基准，加之前先用 WebSearch 或 arXiv 核实标题、作者、编号。

### 6.4 加/改配图

1. 在 `wechat-series/images/` 新建或修改 SVG；
2. 运行 `python3 render_diagrams.py`；
3. 在 `deep-research-wechat.md` 对应位置插入：

```markdown
![图的说明](images/your-image.png)

*图示：一句话图注。*
```

4. 运行 `python3 build_wechat_series.py`。

图注用纯斜体行，渲染器会输出居中 14px 灰色注释。设计图时以 750–780px 宽为基准，正文 ≥18px，2x 导出；这样在 390px 宽的手机上仍有约 9–10px 的可读字号。

### 6.5 改排版样式

样式常量在 `build_wechat_series.py` 顶部（`S_WRAP`、`S_H2`、`S_P`、`S_TABLE`、`S_PRE`、`S_REF_LI` 等）。改完重新构建，并用 430px 视口预览。

## 7. 公众号排版约束

这些是已经踩过的坑，新增内容时继续遵守：

- **不要加外部链接**：公众号会限制/剥离外链。文献只写 arXiv 编号和会议信息。
- **表格最多 3 列**：4 列在手机上会挤。单元格文字尽量 ≤12 字。
- **代码块行宽 ≤ 约 50 个 ASCII 字符**：否则手机端会折行，续行顶格很难看。必要时手动断行或缩写变量名。
- **段落短**：手机端 2–5 行一段，避免大段文字墙。
- **章节编号用 `01 |`、`02 |`**，不要目录锚点。
- **纯斜体段落**会被渲染成居中小字注释，只用于图注和文末 CTA；不要用它做正文强调。
- **不要加 `<style>` 或 class**：公众号编辑器只稳定保留内联样式。
- **图片是本地路径**：粘贴 HTML 到公众号后，如果图片没自动带入，需要手动上传对应的 PNG。
- **HTML 注释不会显示**：源稿里的「配图建议」是给作者的，转换后不可见。

## 8. 验证清单

每次改完内容或样式，至少检查：

1. `python3 build_wechat_series.py` 无报错，三篇 md/html 和完整版 html 都生成；
2. 三篇的图片 `naturalWidth > 0`（浏览器打开或 Playwright）；
3. 表格没有横向溢出，第一列没有把中文压成竖排；
4. 代码块没有超出容器宽度；
5. 三篇的参考文献数量正确（当前 12 / 12 / 13，完整版 28）；
6. HTML 中没有 `class=`、没有 `href=`；
7. 手机 430px 预览：标题、图注、CTA、代码块都正常。

一个快速检查片段：

```python
from pathlib import Path
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 430, "height": 900})
    page.goto(Path("wechat-series/part2.html").resolve().as_uri())
    print(page.evaluate("""() => [...document.querySelectorAll('figure img')]
        .map(i => [i.naturalWidth, i.naturalHeight])"""))
    b.close()
```

## 9. 待办与下一步

**发布前**

- 通读三篇，检查连载之间的指代（「上一篇」「下一篇」）是否与发布顺序一致。
- 准备封面图；正文还有 3 处配图建议（上篇 2、中篇 1），可选择补图或删除注释。
- 发布顺序：上篇 → 中篇 → 下篇；每篇标题已在 README 中列出。
- 如果 HTML 粘贴后图片丢失，手动上传 `part1-architecture.png`、`part2-workflow.png`、`part3-evaluation.png`。

**可选优化**

- 上篇约 4700 汉字，明显重于中篇/下篇；如果担心完读率，可把 03 的模块部分再拆一篇，但要注意切分点和连载承接。
- 文献目前是「延伸阅读」而非逐条引用；若要走更学术的风格，可在正文加 `[1]` 编号并逐条对应。
- 之前预告过「如何为 Deep Research 构建评估集」，可以作为下一篇；评估流程图和 08 节可以直接复用。
- 可补一张系列封面或三张分篇封面，保持蓝/青/橙的配色。
- 仓库跟踪了 `.DS_Store`，建议加 `.gitignore` 并从索引移除，保持仓库干净。

## 10. 已知限制

- **数据是示意值**：文中的延迟、成本、比例不是实测结果；技术长文开头有免责声明，公众号版本没有重复，发布前可考虑补一句。
- **产品/模型名仅作示例**：能力、价格、版本会变化，不要写成推荐或定论。
- **参考文献不是逐条引用**：每篇开头已说明「未在正文中逐条标注引用」，避免读者误解。
- **图片是本地资源**：HTML 预览正常，但公众号需要手动上传；md 用 mdnice 转换时也要先处理图片。
- **切分点依赖标题文本**：`## 04 |` 和 `## 08 |` 是硬编码的字符串；改章节编号会直接报错，这是有意的保护。
- **构建脚本会覆盖生成文件**：不要在 `partX.md` 上做长期修改。

## 11. 写作风格

- 中文，专业但易懂；先给结论，再给实现和坑。
- 技术细节要落地：数据结构、伪代码、失败模式、取舍，而不是只讲概念。
- 不写营销式表达；不确定的地方明确说假设。
- 术语保持一致：研究状态、证据、claim + quote、预算、DAG、覆盖率、重规划。
- 每篇结尾保留「坑 / 解法」或「工程建议」的收束，符合技术博客的阅读习惯。
