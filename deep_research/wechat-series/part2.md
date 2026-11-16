<!--
公众号发布备注（转换后不会显示）：
本文是「Deep Research 技术详解」连载中篇，覆盖 04–07。
建议封面文案：Deep Research（中）/ 一次研究怎么跑起来
正文含 1 处配图建议。
-->

# Deep Research 技术详解（中）：RAG 之后，一次研究任务怎么跑起来

> 与 RAG 的区别、13 步工作流、6 个工程难点和可落地架构

上一篇我们拆了 Deep Research 的七个核心模块，回答了“它由什么组成”。

这一篇回答另一个问题：这些模块串起来，一次研究任务到底怎么跑？钱和时间花在哪？工程上最容易翻车的地方是什么？

---

## 04 | Deep Research 与 RAG 的区别

| 维度 | RAG | Deep Research |
|---|---|---|
| 目标 | 回答具体问题 | 产出研究结论 |
| 查询复杂度 | 单跳为主 | 多跳、复合 |
| 检索方式 | 向量为主 | 多源混合 |
| 推理深度 | 浅层 | 深层 |
| 多轮迭代 | 通常单轮 | 多轮动态 |
| 任务规划 | 一般没有 | 核心组件 |
| 输出形式 | 答案或短总结 | 结构化报告 |
| 典型场景 | 客服、文档助手 | 投研、选型、调研 |

补充四点：

1. **RAG 是 Deep Research 的子能力**。Deep Research 查私有库时，内部仍是一个 RAG 流程。
2. **RAG 的评估重点是“答对”**，Deep Research 的重点是“研究质量”。
3. **RAG 的失败多是召回问题**，Deep Research 的失败更多是规划、验证和综合问题。
4. **Deep Research 不一定需要 RAG**，但企业场景通常会结合公开网络、私有库和结构化数据库。

---

## 05 | 完整工作流：13 步

把上面的模块串起来，一次研究通常这样走：

**1. 提出问题。**
接收自然语言问题，可能带附件、链接、历史对话。先把多轮指代消解成独立问题。

**2. 识别研究目标。**
判断意图，提取约束，识别歧义，定义成功标准。意图错了，后面全偏。

**3. 拆解子问题。**
按框架或对象拆成 5–12 个可检索、可验证的子问题，形成 DAG。拆太粗会发散，拆太细会爆炸。

**4. 制定研究计划。**
为每个子问题分配检索策略、来源类型、预算和成功标准。计划要考虑工具能力，比如解析器能不能读 PDF 表格。

**5. 执行多轮检索。**
多查询并行，混合召回，去重融合。维护查询历史，避免重复；保留原问题作为锚点，防止漂移。

**6. 阅读和抽取。**
抓取、解析、切片、抽取证据。抓取要分级：HTTP → 无头浏览器 → 人工兜底。抽取必须带原文 quote。

**7. 聚类和去重。**
把讲同一件事的证据归并，识别共识和分歧。按 claim 聚类，而不是按文档聚类；标记来源独立性，防止“伪多源”。

**8. 交叉验证关键事实。**
只对 P0/P1 的 claim 做深度验证，用规则 + NLI + LLM 组合判断。冲突要显式记录，不要静默选一个。

**9. 发现信息缺口。**
对比计划和证据，找出没回答的子问题、证据不足的结论、存在冲突的事实。缺口要分优先级。

**10. 追加检索。**
换角度、换来源、换语言、换时间范围。要求新查询和旧查询有显著差异；连续无新增证据就停。

**11. 形成中间结论。**
每个子问题给出阶段性结论，带置信度和证据。中间结论要带版本号，保留被推翻的可能。

**12. 综合推理。**
跨子问题建立联系，形成整体判断、趋势、风险和建议。按主题组织，不要按来源堆砌。

**13. 生成最终报告。**
大纲先行，逐章生成，引用绑定 evidence_id，最后做引用校验和一致性检查。

整条链路里，最容易出问题的是第 3、6、8、13 步：**拆解决定上限，抽取决定证据质量，验证决定可信度，引用决定可审计性。**

<!-- 配图建议 3：13 步流程图，可压缩成 4 个阶段 -->

---

## 06 | 六个工程难点

### 难点一：问题拆解质量不稳定

同一个问题多次运行，计划差异很大；有时漏维度，有时拆出一堆低价值子问题。

**解法**：领域分析框架库、少样本示例、结构化校验（数量、粒度、依赖、可检索性）、计划评审，以及相似问题的计划复用。

### 难点二：搜索结果噪声高

SEO 内容、转载、营销稿、过时信息占满前排，真正的一手来源反而靠后。

**解法**：多查询多角度召回、站点白名单、一手来源优先、内容质量特征过滤、结果聚类去重。

### 难点三：可信度难判断

模型容易相信“看起来专业”的页面，识别不了软文、利益相关方内容和 AI 生成内容。

**解法**：多维特征 + 规则 + 模型打分；来源分级；追溯引用链；对利益相关内容降权；高风险结论人工审核。

### 难点四：长上下文成本高

读几十篇文档后上下文爆炸，关键信息被淹没，模型注意力下降。

**解法**：分层摘要（片段 → 文档 → 主题）、证据表压缩、按子问题隔离上下文、用检索式记忆替代全文记忆。

### 难点五：多轮调用的延迟和成本

一次任务几十次模型调用、上百次网络请求，P95 延迟高，成本难预测。

**解法**：并行化无依赖任务、模型分层、查询/页面/embedding/摘要缓存、语义缓存、预算和超时、流式输出中间结果。

### 难点六：幻觉与引用追溯

编造数字、引用不存在的来源、引用与内容不符，是多轮生成里最顽固的问题。

**解法**：全链路 ID（document → chunk → evidence → sentence）、生成时绑定引用、原文逐字校验、独立 verifier、低置信标注、人工抽检。

### 还有一个：怎么评估

开放式报告没有标准答案，传统 Accuracy 不适用。

**解法**：多维评估体系 + LLM-as-judge + 人工抽检 + 真实业务 gold set；既评估结果，也评估过程（计划质量、检索多样性、验证覆盖率）。

---

## 07 | 可落地的工程方案

### 整体架构

```text
用户问题
   │
   ▼
┌─────────────────┐
│ 编排器           │
│ 状态 / 预算 / 停止 │
└──┬───┬───┬───┬──┘
   │   │   │   │
   ▼   ▼   ▼   ▼
 规划 检索 阅读 验证
   └───┴───┴───┘
        │
        ▼
     综合 / 报告
```

系统分三层：

- **控制面**：API 网关、编排器、Planner、预算管理、状态存储；
- **数据面**：查询服务、搜索适配器、抓取解析、切片向量化、向量库、证据库、验证器、综合器；
- **支撑面**：任务队列、缓存、可观测性、评测、权限控制。

### 数据流

1. API 接收问题，生成 task_id，异步返回；
2. 问题理解输出研究简报；
3. Planner 输出子问题 DAG 和预算；
4. 编排器取可执行任务，调用查询服务；
5. 查询服务多路召回、融合、重排；
6. 抓取解析、切片、抽取证据，写入证据库；
7. 验证器做来源分级、蕴含验证、交叉验证、冲突检测；
8. 覆盖率评估触发重规划或追加检索；
9. 综合器生成大纲、逐章写作、绑定引用；
10. 引用校验器逐句检查，输出最终报告。

### 技术栈示例

| 能力 | 可选方案（仅示例） |
|---|---|
| LLM | Claude、GPT、Gemini、Qwen、DeepSeek |
| Search API | Brave、Bing、Tavily、Exa、SerpAPI |
| Embedding | BGE-M3、E5、Voyage、OpenAI Embeddings |
| Reranker | BGE Reranker、Cohere Rerank、cross-encoder |
| Vector DB | pgvector、Qdrant、Milvus、Weaviate |
| Task Queue | Celery、Temporal、Ray、Kafka |
| Cache | Redis、Memcached |
| Parser | trafilatura、Readability、Unstructured、Playwright |
| 可观测性 | OpenTelemetry、Langfuse、LangSmith、Grafana |

选型时优先看：长上下文、结构化输出、工具调用稳定性、合规要求、单位成本。产品能力变化很快，落地前以官方文档为准。

### 核心伪代码

```python
def run_research(q, constraints):
    brief = understand(q, constraints)
    plan = plan_research(brief)
    state = State(brief, plan, Budget())

    while not should_stop(state):
        tasks = frontier(state.plan, state)
        results = parallel(
            execute_task, tasks)
        merge(state, results)

        state.coverage = coverage(state)
        state.gaps = find_gaps(state)
        state.conflicts = conflicts(state)

        if needs_replan(state):
            state.plan = replan(state)

    draft = synthesize_report(state)
    return check_cites(draft, state.evidence)


def execute_task(task, state):
    qs = generate_queries(task, state)
    hits = search(qs, top_k=10)
    docs = read_documents(hits)
    ev = extract_evidence(docs, task)
    return verify_evidence(ev, state)


def verify_evidence(items, state):
    ok = []
    for e in items:
        e["sup"] = nli(e["quote"], e["claim"])
        e["cred"] = prior(e["source_url"])
        e["fresh"] = fresh(e["published_at"])
        e["corro"] = sources(
            e["claim"], state.evidence)
        e["conf"] = weighted(
            e["sup"], e["cred"],
            e["fresh"], e["corro"])

        if e["sup"] < 0.5:
            continue
        if e["conf"] < 0.45:
            state.gaps.append(e["claim"])
            continue
        ok.append(e)
    return ok
```

这段代码体现了五个关键设计：

- **状态显式化**：计划、证据、覆盖率、缺口都在 State 里；
- **预算硬约束**：每个动作都检查上限；
- **证据可定位**：quote 必须逐字出现在原文；
- **验证前置**：低置信证据不进入综合；
- **可停止**：有明确的停止条件。

---

*下一篇是最后一篇：怎么评估研究质量、8 个典型应用场景、7 个未来趋势，以及给工程团队的 8 条落地建议。*
