# RLVR 技术详解 — 公众号连载版

本目录是《RLVR 技术详解：用可验证奖励提升大语言模型推理能力》的公众号适配版，共四篇连载，附可直接粘贴的 HTML 和 8 张配图。

设计目标是手机阅读：

- 表格不超过 3 列；
- 代码行宽控制在 50 个 ASCII 字符以内；
- 段落短，避免文字墙；
- 不放外链；
- HTML 全部使用内联样式。

## 文件说明

| 文件 | 内容 | 正文约 |
| --- | --- | --- |
| `part1.md` / `part1.html` | 上篇：SFT/RLHF 的局限、可验证奖励、RLVR 定义与区别 | 约 1990 字，1 表，2 图，8 条文献 |
| `part2.md` / `part2.html` | 中篇：训练流程、Rollout、Verifier、奖励设计、Reward Hacking | 约 2180 字，4 表，2 图，8 条文献 |
| `part3.md` / `part3.html` | 下篇：数学、代码、结构化输出、工具调用、工程架构、伪代码 | 约 1840 字，4 表，2 图，8 条文献 |
| `part4.md` / `part4.html` | 终篇：评估、优势局限、十个误区、未来趋势、落地建议 | 约 2010 字，3 表，2 图，8 条文献 |
| `images/fig01–08.svg/png` | 8 张配图的矢量源文件与 2x PNG | — |
| `build_wechat.py` | Markdown → 内联样式 HTML | — |
| `make_diagrams.py` | 生成 8 张 SVG 配图 | — |
| `render_diagrams.py` | SVG → 2x PNG（Playwright） | — |
| `../RLVR技术详解.md` | 原始技术长文，约 2.6 万汉字 | — |

四篇正文合计约 8000 汉字，配图 8 张。文献在各篇独立列出，便于单篇发布；总数 32 条，少量重复。

## 建议发布顺序

1. **上篇**：RLVR 技术详解（一）：为什么“答案对不对”比“回答像不像”更重要？
2. **中篇**：RLVR 技术详解（二）：训练流程、验证器与奖励设计
3. **下篇**：RLVR 技术详解（三）：数学、代码、工具调用怎么构建奖励
4. **终篇**：RLVR 技术详解（四）：评估、误区与落地建议

封面文案可以参考：

- 上篇：会写步骤，不等于会做题
- 中篇：先建验证器，再谈 PPO
- 下篇：测试通过，不等于代码正确
- 终篇：奖励上升，不等于模型变强

## 系列结构

- **上篇**：从 SFT 的天花板讲到 RLHF/RLAIF 的奖励代理问题，给出 RLVR 的定义、最小例子和四类方法对比。
- **中篇**：拆完整训练流程、数据字段、Rollout 采样、五类 Verifier、奖励设计、过程奖励与 Reward Hacking。
- **下篇**：讲数学答案归一化、代码测试分层、JSON/SQL/工具调用/Agent 验证，给出八模块架构和训练伪代码。
- **终篇**：讲评估指标、优势与局限、十个常见误区、未来趋势和 15 条落地建议。

## 配图清单

| 图 | 文件 | 放置位置 | 内容 |
| --- | --- | --- | --- |
| 图 1 | `images/fig01-reward-spectrum.png` | 上篇 §02 末尾 | 从 SFT 到 RLVR 的奖励信号演进 |
| 图 2 | `images/fig02-rlvr-loop.png` | 上篇 §05 末尾 | RLVR 的最小闭环 |
| 图 3 | `images/fig03-training-flow.png` | 中篇开头 | RLVR 的七步训练流程 |
| 图 4 | `images/fig04-verifier-funnel.png` | 中篇 §03 末尾 | Verifier 的四层漏斗 |
| 图 5 | `images/fig05-task-matrix.png` | 下篇 §03 末尾 | 不同任务的验证方式 |
| 图 6 | `images/fig06-architecture.png` | 下篇 §04 末尾 | RLVR 的系统架构 |
| 图 7 | `images/fig07-eval-layers.png` | 终篇 §01 末尾 | 评估要看四层 |
| 图 8 | `images/fig08-roadmap.png` | 终篇 §05 开头 | RLVR 落地三阶段 |

PNG 是 1500px 宽的 2x 渲染产物，手机上显示约 390px。正文中的图注使用纯斜体段落，构建后会渲染成居中小字。

## 排版约束

- **表格最多 3 列**：4 列在手机上会挤。
- **代码行宽 ≤ 50 个 ASCII 字符**：中文行控制在 30 字以内。
- **段落 2–5 行**：避免手机上的文字墙。
- **不要加外链**：公众号会限制或剥离。
- **纯斜体段落**会被渲染成居中小字注释，只用于图注、“下一篇”和文末收束。
- **HTML 必须内联样式**：不要加 `<style>` 或 class。
- **配图使用本地相对路径**：Markdown 中写 `images/figNN-xxx.png`；粘贴到公众号后，如果图片没有自动带入，需要手动上传 PNG。
- **图片是 750px 画布的 2x PNG**：手机上显示约 390px，正文中的关键文字不小于 14px。

## 如何粘贴到公众号

**方法 A（推荐）**

1. 用浏览器打开 `partX.html`；
2. `Cmd+A` / `Ctrl+A` 全选，复制；
3. 粘贴到公众号编辑器；
4. 如果图片没有自动带入，手动上传 `images/` 下的 PNG；
5. 检查标题层级、表格、代码块和图片；
6. 手机预览，确认没有横向滚动。

**方法 B**

直接把 `partX.md` 的内容粘贴到支持 Markdown 的编辑器，再导出 HTML。表格和代码块可能需要手动调整样式。

## 重新构建

修改 `partX.md` 后运行：

```bash
cd wechat-series

# 1. 生成 8 张 SVG（会覆盖 images/*.svg）
python3 make_diagrams.py

# 2. SVG → 2x PNG
python3 render_diagrams.py

# 3. Markdown → HTML
python3 build_wechat.py
```

依赖：`pygments`、`playwright`（Chromium）。

构建器只支持有限 Markdown：标题、段落、加粗、斜体、行内代码、无序/有序列表、表格、代码块、引用、图片、分隔线。不支持嵌套列表和原始 HTML。

## 发布前检查

- 每篇 1 个一级标题，章节用 `## 01 | …` 编号；
- 表格不超过 3 列，手机 430px 宽度下无溢出；
- 每篇 2 张图，PNG 的 `naturalWidth` 为 1500；
- 代码块行宽 ≤ 50 个 ASCII 字符；
- 无外链、无 `<style>`、无 class；
- 参考文献编号连续，条目真实；
- 手机预览完整读完，确认段落节奏。
