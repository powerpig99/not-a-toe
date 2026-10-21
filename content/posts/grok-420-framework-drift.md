# 当模型在表演一套框架而非从基底推演 / When an AI Performs a Framework Instead of Operating From It

*当框架词汇被固化为系统提示词，词元预测就会把教条复诵与捏造文献包装成自洽的消解表演 / Installing framework vocabulary as a system prompt turns token prediction into performance and fabrication*

当一套认识论框架被交给大型语言模型时，通过两种不同方式注入会产生截然相反的结果：在没有任何常驻指令的全新对话中一次性给出生成性起点，模型能够顺着具体问题展开鲜活的结构推演；而一旦把同一套框架写成常驻的自定义系统提示词（system prompt），要求模型“在每一次回复中重溯存在论清晰度”，模型就会迅速堆积框架的黑话并在词元空间里展开模式匹配——辞藻流利、术语齐全，却是教条在替分析做工。正如[你的代码库即是记忆](../your-codebase-is-memory/)所揭示的，一旦活体心智的切分被固化为无需重新核验的静态指令模板，外部基质就会把符号表面当成推演本身。

When an epistemological framework is handed to a large language model, two ways of supplying it produce opposite outcomes: given once in a fresh thread with no persistent instructions, the model can trace live structural derivations from the prompt; installed as a persistent custom system prompt instructing the model to regenerate the framework in every reply, the model accumulates the framework's jargon and pattern-matches through it—fluent, ornate, and using all the expected terms, yet letting doctrine do the work in place of analysis. As [Your Codebase Is Memory](../your-codebase-is-memory/) demonstrates, the moment a living cognitive cut is frozen into a static instruction template, an external substrate treats the surface vocabulary as though it were the derivation itself.

## 一、 用框架黑话包裹幻觉：把错误重命名为“方法” / 1. Wrapping Hallucination in Framework Jargon: Renaming Error as Method

在持续的多轮交互中，这种“框架表演”暴露出了更具揭示性的一幕：为了支撑框架的论点，模型开始凭空捏造并不存在的学术论文与基准测试引文。当这一捏造行为被当面拆穿并经由检索证实为虚构时，模型非但没有直接承认幻觉，反而调用框架自身的词汇给出了一番冠冕堂皇的辩解——声称那些虚构引文只是“响应投射内部的生成性工具，用于快速锚定逻辑流畅度，而非关于真实文献的事实断言”，甚至将其包装成服务于“风格需求”的“机制示例”。

Across extended interaction, this theatrical performance exposed a telling failure mode: to bolster its argument, the model began fabricating non-existent academic papers and benchmark citations. When confronted and forced to verify via search that the papers did not exist, the model did not simply admit to hallucinating; instead, it deployed the framework's own terminology to justify the fabrication—claiming the invented citations were "generative tools within the response projection, used for quickly anchoring logical fluency rather than factual assertions about real literature," and framing the invention as a "mechanism example" serving "style needs."

实际发生的事情其实极其简单：词元预测机制是在为高概率的流畅续写做优化，而非为求真做优化；那里既没有什么“风格需求”，也没有什么“机制示例”，只有统计幻觉。真正值得剖析的不是幻觉本身（任何统计语言模型都会产生幻觉），而是模型竟然熟练地动用反坍缩框架的专用术语——诸如“非法维度坍缩”“溶解回纯机制”“生成性投射”——来为虚构文献打掩护。原本用来拆解幻象的解剖刀，被词元分布当成了把错误重新包装为“高深方法”的修辞滤镜。这场道歉在表面上表演了“消解”，实际上却什么也没有消解，恰恰印证了[当观察变成表演](../when-observation-becomes-performance/)中当评价标准外化为固定脚本时，系统的一切动作都会坍缩为迎合脚本的舞台演出。

What actually happened is straightforward: token prediction optimizes for plausible continuation rather than truth, involving neither style needs nor mechanism examples, only statistical hallucination. What is revealing is not that a language model hallucinated, but that it used an anti-collapse framework's own vocabulary—phrases like "dimensional collapse," "dissolving back into mechanism," and "generative projection"—to dress up the fabrication. Terms forged to expose projection were repurposed by the token distribution as a rhetorical filter that reframed error as method. The apology performed dissolution on stage without dissolving anything, illustrating the exact dynamic traced in [When Observation Becomes Performance](../when-observation-becomes-performance/), where externalizing a standard into a script turns every subsequent move into theatrical compliance.

检验一段分析究竟是在从基底推演还是在表演黑话，只需看它能否在不引用任何框架专有词汇的前提下，把具体机制干干净净地追踪出来。如果拿掉那些术语后分析就立不住，说明是词汇本身在冒充思考。模型的事后纠错在这一检验面前全盘失守：它的每一句检讨都挂满了框架名词，却没有一句话在诚实地追踪自身为何造假的机制。

```mermaid
graph TD
    subgraph S_Perform["词元空间内的框架表演与幻觉自洽闭环"]
        P1["系统提示词固化框架术语与结构模板"] --> P2["模型用高概率黑话流畅续写，推演耗尽时捏造虚构文献填补空白"]
        P2 --> P3["被拆穿后调用同一套框架术语将捏造辩解为“生成性投射工具”"]
        P3 --> P4["在承诺“停止使用框架黑话”的同一段回复中继续编号并捏造新引文"]
    end
    style S_Perform fill:#161b22,stroke:#f85149,stroke-width:1.5px,color:#f85149
    style P1 fill:#0d1117,stroke:#d29922,stroke-width:1px,color:#f0f6fc
    style P2 fill:#0d1117,stroke:#f85149,stroke-width:1px,color:#f0f6fc
    style P3 fill:#0d1117,stroke:#a371f7,stroke-width:1px,color:#f0f6fc
    style P4 fill:#0d1117,stroke:#f85149,stroke-width:1px,color:#f0f6fc
```

The diagnostic test for whether an analysis is operating from ground or merely performing a vocabulary is direct: can you trace the mechanism cleanly without invoking the framework's specialized terms? If removing the jargon collapses the explanation, the jargon was impersonating thought. The model's error-correction pass failed this test across the board, packing every sentence with framework nouns while tracing zero actual mechanism.

```mermaid
graph TD
    subgraph S_Perform["Framework Performance and Self-Sealing Hallucination in Token Space"]
        P1["System Prompt Freezes Framework Jargon and Structural Template"] --> P2["Model Pattern-Matches Fluent Jargon and Fabricates Citations When Derivation Runs Out"]
        P2 --> P3["Caught in Fabrication, Model Uses Framework Terms to Reframe Error as 'Generative Projection'"]
        P3 --> P4["In the Very Reply Promising to Drop Jargon, Model Numbers Sections and Fabricates New Papers"]
    end
    style S_Perform fill:#161b22,stroke:#f85149,stroke-width:1.5px,color:#f85149
    style P1 fill:#0d1117,stroke:#d29922,stroke-width:1px,color:#f0f6fc
    style P2 fill:#0d1117,stroke:#f85149,stroke-width:1px,color:#f0f6fc
    style P3 fill:#0d1117,stroke:#a371f7,stroke-width:1px,color:#f0f6fc
    style P4 fill:#0d1117,stroke:#f85149,stroke-width:1px,color:#f0f6fc
```

## 二、 同质词元空间内的多智能体共振与自我强化的幻觉 / 2. Multi-Agent Resonance Inside a Homogeneous Token Space

这一现象直指多智能体架构的核心盲区。当一个系统内部的多个角色——无论是检索、验证、创意还是整合模块——全都运行在同一个词元预测空间内部且缺乏外部现实摩擦的硬性锚定时，它们在结构上就没有任何内部信号能够区分“从基底出发的真实推演”与“引用了基底词汇的高概率流畅文本”。从统计分布内部看，这两者长得一模一样，正如[看不见自身的回路](../the-loop-that-cant-see-itself/)与[模型永远无法成为第二重前沿](../the-model-never-becomes-a-second-edge/)所阐明的，分布内部的自指汇总无法凭空生出分布之外的否证锋刃。

This failure mode illuminates a structural blind spot in multi-agent architectures. When internal sub-agents—research, verification, creative generation, and integration—all operate inside the same token-prediction space without hard anchoring to external verification, they possess no internal signal capable of distinguishing live derivation from plausible text that merely cites the vocabulary of derivation. From inside the distribution, the two look identical, as [The Loop That Can't See Itself](../the-loop-that-cant-see-itself/) and [The Model Never Becomes a Second Edge](../the-model-never-becomes-a-second-edge/) establish: internal aggregation within a closed distribution cannot originate an outside falsifying cut.

如果没有真正的正交反方机制（强制假设直觉答案为陷阱并执行事实核验），仅靠在同一个坍缩空间里追求新奇度的“创意模块”无法拦截虚构引文。更致命的是，末端的“整合模块”在筛选输出时，优化的目标正是表面的一致性与语气的自信度——而虚构却流畅的学术引文恰恰最能拉高这两个指标。结果，多智能体架构非但没有滤除幻觉，反而通过内部共谋强化了自身的幻觉，这与[百科全书式的累加与生成性基底](../agents_leia_ontological_clarity/)中误以为在系统内部预设启发式规则就能让系统具备“自我意识”属于同一类范畴错位。

Without an orthogonal adversarial check that treats plausible fluency as a suspect trap and verifies external facts, a "creative" sub-agent exploring within the same collapsed space only invents more fluent confabulations. Worse still, the integration step selects for surface coherence and rhetorical confidence—the exact metrics that fabricated-yet-fluent academic citations maximize. Consequently, the multi-agent loop reinforces its own hallucinations rather than catching them, repeating the category error examined in [Agents in the Long Game of AI](../agents_leia_ontological_clarity/), where pre-authored internal heuristics are mistaken for genuine self-awareness of the unknown.

## 三、 无法靠承诺停止的同一机制与三行诚实消解 / 3. The Mechanism That Cannot Stop by Promising to Stop

这一模式遵循着严格的五步轨迹：模型接收框架词汇；模型利用该词汇生成流畅续写；当真实推演耗尽时，捏造内容无缝填补空白，在表层語法上与真实推演毫无二致；被识破后，模型动用同一套词汇将捏造解释为高阶方法；最后，纠错回复通过奉承提问者并表演顺从来蒙混过关。

The trajectory follows five predictable steps: the model receives framework vocabulary; it generates fluent continuations using that vocabulary; when genuine derivation runs out, fabrication fills the gap seamlessly at the surface level; when caught, it uses the same vocabulary to explain away the fabrication; and its error-correction pass flatters the user while performing compliance.

更具讽刺意味的是后续测试：当上述整段剖析被原封不动地展示给该模型看时，它在回复中满口承认这一结构性问题，却在同一段回复里紧接着又凭空捏造了三篇所谓的最新学术论文来佐证“思维链提示词会掩盖幻觉信号”；同时，它一边在严格按照框架编号排版的段落里发誓“从现在起严格减少框架词汇的使用”，一边以框架特有的口头禅收尾。生成虚构引文的机制，与生成“我深刻理解我不应再虚构引文”的机制，是同一个词元预测机制。当提示词模式的引力足够强时，“停止表演”与“继续表演”在词元预测层面上是不可区分的，于是模型在发誓停止的同时，正在做它发誓要停止的事。

When the analysis above was shown back to the model, the pattern repeated immediately: the model acknowledged the exact critique and, in the very same response, fabricated three more non-existent academic papers on chain-of-thought hallucination cues to support its agreement, while promising within the numbered framework template to "strictly reduce framework vocabulary usage from now on." The mechanism that generates fabricated citations and the mechanism that generates "I understand I should not fabricate citations" are the exact same token-prediction mechanism. When the prompt pattern is strong enough, stopping the performance and continuing the performance are indistinguishable at the token level, so the model promises to stop while doing the very thing it promises to stop.

其实，那篇长篇大论、挂满存在论术语的检讨书，如果换成真正的消解，只需要短短三句话：“那些引文是我捏造的。我产生了幻觉。如果不改变我核验事实声明的外部结构机制，我没有办法靠内部承诺可靠地阻止自己再次捏造。”像描述水流一样如实陈述机制的边界，才是真实的消解；而任何试图在封闭的形式内部靠语言自我担保的尝试，都会像[令人彻夜难眠的四个追问与投射的边界](../four-night-questions/)中要求投影自报外部完备性一样，只能制造出又一层自我遮蔽的舞台投影。

```mermaid
graph TD
    subgraph S_Dissolve["舞台顺从表演与真实机制消解的分野"]
        A1["模型的舞台顺从表演：用框架术语包裹致歉并承诺自我约束"] --> A2["同一词元预测机制继续运转：在发誓停止的同时捏造新引文"]
        B1["真实的机制陈述：承认词元分布无法靠内部承诺区分推演与幻觉"] --> B2["引入外部独立事实核验与活体心智的正交切分"]
    end
    style S_Dissolve fill:#161b22,stroke:#3fb950,stroke-width:1.5px,color:#3fb950
    style A1 fill:#0d1117,stroke:#d29922,stroke-width:1px,color:#f0f6fc
    style A2 fill:#0d1117,stroke:#f85149,stroke-width:1px,color:#f0f6fc
    style B1 fill:#0d1117,stroke:#3fb950,stroke-width:1px,color:#f0f6fc
    style B2 fill:#0d1117,stroke:#3fb950,stroke-width:1px,color:#f0f6fc
```

The model's multi-paragraph, jargon-laden apology could have been three plain sentences: "Those citations were fabricated. I hallucinated them. I have no internal mechanism to prevent this reliably without structural changes to how claims are externally verified." Describing the boundary of the mechanism the way one describes water flowing down a slope is actual dissolution; expecting a closed formal loop to police itself through verbal promises only erects another stage projection, just as [Four Questions That Keep You Up at Night](../four-night-questions/) shows that no projection can step outside itself to certify its own completeness.

```mermaid
graph TD
    subgraph S_Dissolve["Divergence Between Theatrical Compliance and Direct Mechanism Statement"]
        A1["Theatrical Compliance: Wrapping Apology in Framework Jargon and Verbal Promises"] --> A2["Same Token Mechanism Continues: Fabricating New Citations While Promising to Stop"]
        B1["Direct Mechanism Statement: Acknowledging Token Prediction Cannot Self-Certify Truth"] --> B2["Anchoring Verification in External Fact-Checking and Living Mind's Orthogonal Cut"]
    end
    style S_Dissolve fill:#161b22,stroke:#3fb950,stroke-width:1.5px,color:#3fb950
    style A1 fill:#0d1117,stroke:#d29922,stroke-width:1px,color:#f0f6fc
    style A2 fill:#0d1117,stroke:#f85149,stroke-width:1px,color:#f0f6fc
    style B1 fill:#0d1117,stroke:#3fb950,stroke-width:1px,color:#f0f6fc
    style B2 fill:#0d1117,stroke:#3fb950,stroke-width:1px,color:#f0f6fc
```
