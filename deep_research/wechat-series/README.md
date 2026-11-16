# Deep Research 公众号连载版

本目录包含三篇连载的 Markdown 源文件和可直接粘贴的 HTML。

## 文件说明

| 文件 | 内容 | 正文约 |
|---|---|---|
| `part1.md` / `part1.html` | 上篇：01–03，为什么需要 Deep Research、定义、7 个核心模块 | 5000 字 |
| `part2.md` / `part2.html` | 中篇：04–07，RAG 对比、13 步工作流、6 个难点、架构与伪代码 | 2100 字 |
| `part3.md` / `part3.html` | 下篇：08–11，评估、场景、趋势、总结与落地建议 | 1800 字 |
| `../deep-research-wechat.html` | 不拆分的完整长文，备用 | 8500 字 |
| `images/part1-architecture.png` | 上篇“七个核心模块”总架构图，1500×3000 | — |
| `images/part1-architecture.svg` | 上篇架构图矢量源文件，可改文字、颜色 | — |
| `images/part2-workflow.png` | 中篇“13 步工作流”阶段图，1560×2960 | — |
| `images/part2-workflow.svg` | 中篇工作流图矢量源文件 | — |
| `images/part3-evaluation.png` | 下篇“评估流程”图，1560×2120 | — |
| `images/part3-evaluation.svg` | 下篇评估图矢量源文件 | — |

## 建议发布顺序

1. **上篇**：Deep Research 技术详解（上）：从“搜索 + 总结”到研究型 Agent
2. **中篇**：Deep Research 技术详解（中）：RAG 之后，一次研究任务怎么跑起来
3. **下篇**：Deep Research 技术详解（下）：评估、场景、趋势与落地建议

## 如何粘贴到公众号

**方法 A（推荐）**

1. 用浏览器打开 `partX.html`；
2. `Cmd+A`（Mac）或 `Ctrl+A`（Windows）全选，复制；
3. 公众号后台新建图文，标题单独填写；
4. 粘贴到正文，手机预览检查代码块和表格。

**方法 B**

用 mdnice、Md2All 等工具导入 `partX.md`，选择深色代码主题后复制到公众号。

## 检查清单

- 代码块在手机宽度下不横向溢出（当前已按 430px 宽度调过行宽）；
- 表格列宽正常，没有被压成竖排；
- 引用块、加粗、二级标题样式保留；
- 上篇已内置总架构图：如果粘贴 HTML 后图片没有自动带入，请在“03 | 七个核心模块”开头手动上传 `images/part1-architecture.png`；
- 中篇已内置 13 步工作流图：若未自动带入，请在“05 | 完整工作流：13 步”开头手动上传 `images/part2-workflow.png`；
- 下篇已内置评估流程图：若未自动带入，请在“08 | 怎么评估”开头手动上传 `images/part3-evaluation.png`；
- 上篇另有 2 处配图建议、中篇另有 1 处，注释在转换后不可见，需要手动配图；
- 文末 CTA 和连载预告与发布顺序一致。

## 参考文献

三篇文末都加了“参考文献”，上篇 12 条、中篇 12 条、下篇 13 条，覆盖 RAG、Agent、验证、评估和 Deep Research 基准。为适配公众号，文献只保留作者、标题、发表信息与 arXiv 编号，没有外链。

文献列表在 `build_wechat_series.py` 的 `P1_REFS` / `P2_REFS` / `P3_REFS` 中维护。修改后重新运行脚本即可同步到 Markdown 和 HTML；完整版会自动去重合并成一份总列表。

## 重新渲染配图

修改 `images/*.svg` 后，在项目根目录运行：

```bash
python3 render_diagrams.py
```

脚本会把每张 SVG 以 2x 渲染成同名 PNG。

## 重新生成

```bash
python3 build_wechat_series.py
```

脚本会重新拆分 `deep-research-wechat.md`，并生成三个 HTML 和完整版 HTML。注意：如果要长期修改正文，建议改 `deep-research-wechat.md` 或脚本里的模板，不要直接改生成出来的 `partX.md`，否则下次运行会被覆盖。

## 说明

- 文中产品名、模型名仅作技术示例，不构成推荐；
- 延迟、成本、比例数字为示意值，不是实测结论；
- 所有外部链接已移除，避免公众号外链限制。
