# 大语言模型评估体系 — 公众号连载版

本目录包含四篇连载的 Markdown 源文件和可直接粘贴的 HTML。

设计目标是手机阅读：表格不超过 3 列，代码行宽控制在 50 个 ASCII 字符以内，段落短，无外链。

## 文件说明

| 文件 | 内容 | 正文约 |
|---|---|---|
| `part1.md` / `part1.html` | 上篇：为什么评估、评什么、难在哪 | 2400 字 |
| `part2.md` / `part2.html` | 中篇：六种方法与七类指标 | 2700 字 |
| `part3.md` / `part3.html` | 下篇：RAG、Agent 与企业评估集 | 2600 字 |
| `part4.md` / `part4.html` | 终篇：平台、伪代码、Judge、报告与门禁 | 2300 字 |
| `images/fig01–08.svg/png` | 8 张配图的矢量源文件与 2x PNG | — |
| `build_wechat.py` | Markdown → 内联样式 HTML | — |
| `render_diagrams.py` | SVG → 2x PNG（Playwright） | — |
| `../大语言模型评估体系详解.md` | 原始技术长文，约 2.8 万汉字 | 不参与构建 |

## 建议发布顺序

1. **上篇**：大模型评估（一）：为什么“感觉不错”不能作为上线依据
2. **中篇**：大模型评估（二）：六种方法，别只盯着 Benchmark
3. **下篇**：大模型评估（三）：RAG 与 Agent，必须拆开评
4. **终篇**：大模型评估（四）：把评估接进研发流程

封面文案可以参考：

- 上篇：不是模型不强，是你没评对
- 中篇：Benchmark 不是录用通知
- 下篇：答案错了，先别换模型
- 终篇：让评估拦住上线

## 配图清单

| 图 | 文件 | 放置位置 | 内容 |
|---|---|---|---|
| 图 1 | `images/fig01-eval-layers.png` | 上篇 §04 | 评估的四层对象 |
| 图 2 | `images/fig02-test-layers.png` | 上篇 §02 | 确定性、语义、统计三层测试 |
| 图 3 | `images/fig03-method-pipeline.png` | 中篇 §01 | 六种方法的组合顺序 |
| 图 4 | `images/fig04-correctness-reference.png` | 中篇 §08 | 正确性的四个参照物 |
| 图 5 | `images/fig05-rag-pipeline.png` | 下篇 §01 | RAG 检索与生成两段 |
| 图 6 | `images/fig06-agent-trace.png` | 下篇 §08 | Agent 结果与过程评估 |
| 图 7 | `images/fig07-platform-flow.png` | 终篇 §01 | 评估平台数据流与回流 |
| 图 8 | `images/fig08-gate-decision.png` | 终篇 §03 | 上线门禁的三层判断 |

PNG 是 1500px 宽的 2x 渲染产物，手机上显示约 390px，关键文字约 9–12px。

## 如何粘贴到公众号

**方法 A（推荐）**

1. 用浏览器打开 `partX.html`；
2. `Cmd+A` / `Ctrl+A` 全选，复制；
3. 公众号后台新建图文，标题单独填写；
4. 粘贴到正文，手机预览检查表格、代码块和配图。

如果粘贴后图片没有自动带入，请在对应位置手动上传 `images/` 下的 PNG。

**方法 B**

用 mdnice、Md2All 等工具导入 `partX.md`，选择深色代码主题后复制到公众号。

## 重新生成

```bash
cd llm_eval/wechat-series
python3 build_wechat.py
```

脚本只读取 `part1.md`–`part4.md`，生成同名 HTML。

要改内容，改 Markdown 源文件，不要改 HTML；下次构建会覆盖。

## 重新渲染配图

配图的唯一源文件是 `images/*.svg`，PNG 是渲染产物，不要手改 PNG。

```bash
cd llm_eval/wechat-series
python3 render_diagrams.py
```

修改 SVG 后重新运行，会覆盖同名 PNG。再用 `build_wechat.py` 重新生成 HTML。

## 检查清单

- 表格不超过 3 列，手机宽度下没有横向溢出；
- 代码块没有横向溢出，续行不顶格；
- 8 张配图都能正常加载，图注在图片下方；
- 标题、引用块、加粗和内联代码样式保留；
- 文内没有外链；
- 四篇的承接语与发布顺序一致；
- 数字均为示意值，不是实测结论。

## 排版约束

- **表格最多 3 列**：4 列在手机上会挤。
- **代码行宽 ≤ 50 个 ASCII 字符**：中文行控制在 30 字以内。
- **段落 2–5 行**：避免手机上的文字墙。
- **不要加外链**：公众号会限制或剥离。
- **纯斜体段落**会被渲染成居中小字注释，只用于图注和文末 CTA。
- **HTML 必须内联样式**：不要加 `<style>` 或 class。

## 说明

- 文中模型名、基准名仅作技术示例，不构成推荐。
- 延迟、成本、准确率、样本量均为量级示意。
- 评估方法和指标体系来自公开资料与工程实践；具体阈值需按业务校准。
