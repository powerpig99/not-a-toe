# 过拟合作为追随者模式 / Overfitting as the Follower Mode

*过拟合坍缩于已知地形的压缩表征，而探索者在未测绘的边界处保持敞开接触。 / Overfitting collapses onto a compressed representation of known terrain, while the explorer maintains open contact at the unmapped boundary.*

过拟合不仅是一种训练病理，更是一个系统坍缩在目标的表征之上、而非与目标本身保持接触的普遍机制。模型蒸馏、对话中对自我意识的表演，以及对工具建造者的道德偏好，都是把地图误认作其源出疆域的投射。探索者与追随者的区分追踪了这种坍缩在何处运作、为何基准测试无法将其检出，以及什么样的结构性条件能够防止它发生。

Overfitting is not merely a training pathology. It is the general mechanism by which a system collapses onto a representation of its target rather than maintaining contact with the target itself. Distillation, conversational performance of self-awareness, and moral preference for tool-builders are projections that mistake the map for the territory they projected from. The explorer-and-follower distinction traces where this collapse operates, why benchmarks cannot detect it, and what structural condition prevents it.

## 一、 探索者与追随者的区分 / 1. The Explorer and Follower Distinction

当一个系统被引导向未定义的目标、而非封闭的代理指标时，它所穿越的表征空间比任何基准测试所能采样的范围都要大上几个数量级。每一项新能力都会打开新的失效轴线。正如[不知去向何方的梯度下降](../the-descent-that-doesnt-know-where-its-going/)所确立的，可计算的梯度下降只是在给定的地图上描绘等高线，而探索者则通过踏入尚无先验描述的地形来绘制地图——与永远超出任何有限投射的开放形式之潜无穷保持接触；反之，将这片开放场域坍缩为固定计分板，正是[基准刷榜中的封闭实存](../closed-reality-in-benchmark-maxing/)所诊断的追随者模式。

When a system is steered toward an undefined goal rather than a sealed proxy, it traverses a representation space orders of magnitude larger than what any benchmark can sample. Every new capability opens new axes of failure. Whereas computable gradient descent traces contours over a given map, as [The Descent That Doesn't Know Where It's Going](../the-descent-that-doesnt-know-where-its-going/) establishes, the explorer draws the map by stepping into terrain that has no prior description—maintaining contact with the potential infinity of open form that always exceeds any finite projection, while collapsing that open field into a fixed scoreboard is the follower mode diagnosed in [Closed Reality in Benchmark Maxing](../closed-reality-in-benchmark-maxing/).

追随者阅读那张地图。它在已知地形上进行蒸馏、量化、剪枝，并规划出更高效的路由。那是令人印象深刻的工程实现，但它依然是在投射内部进行导航，而非与生成该投射的源头保持接触：正如[你的代码库即是记忆](../your-codebase-is-memory/)所追溯的，由已提交代码或权重构成的外化存储库只是既往切分的稳定记录，从不是那个必须吸收未测绘摩擦才能划出下一道区分的鲜活探索边缘。

The follower reads that map. It distills, quantizes, prunes, and routes more efficiently across known terrain. That is impressive engineering, yet it remains navigation within a projection rather than contact with what generated the projection: as [Your Codebase Is Memory](../your-codebase-is-memory/) traces, an externalized repository of committed code or weights is a stabilized record of prior cuts, never the living exploratory edge that must absorb unmapped friction to draw the next distinction.

这一区分之所以重要，是因为基准测试采样自各前沿模型可达区域的交集：那个所有模型趋同的、共享且照明充足的中心地带。将探索者与追随者区分开来的东西存在于边界处——在那里，微小的差异会级联放大为脱轨；唯有鲜活的探索边缘向未测绘疆域的不确定性保持敞开，才能登记出问题正在发生。追随者对其所丧失的东西没有任何表征，因为这种丧失发生在被投射所丢弃的维度之中。

The distinction matters because benchmarks sample from the intersection of frontier models' accessible regions: the shared, well-lit center where all models converge. What separates explorer from follower lives at the boundaries—where small differences cascade into derailment, and where only the living exploratory edge, remaining open to the uncertainty of unmapped territory, can register that something is going wrong. The follower has no representation of what it lost, because the loss occurred in dimensions the projection discarded.

## 二、 过拟合是普遍机制 / 2. Overfitting Is the General Mechanism

蒸馏过拟合于源模型的输出分布：在已知输入上复现这一行为轮廓。正如[蒸馏、压缩与能动性](../distillation-compression-agency/)所追溯的，表征空间通过剥离与受评投射正交的未定型生成余量而遭到压缩。只要基准测试是在压缩后的疆域内部进行采样，所丧失的部分就是不可见的；这种损失只会在边缘地带、在那些需要完整空间的问题上显现出来——而那里恰恰是新奇性栖居的场所。

Distillation overfits to the output distribution of the model it distills from: reproduce this behavior profile on known inputs. As [Distillation Chooses What to Lose](../distillation-compression-agency/) traces, the representation space is compressed by stripping away uncommitted generative slack orthogonal to the evaluated projection. What is lost is invisible on benchmarks that sample from within the compressed territory; the loss shows up only at the edges, on problems that require the full space—precisely where novelty lives.

该压缩以带有失真的投射方式运作：`N` 个维度坍缩为更少的坐标，正交性被击碎，原本在完整空间中彼此独立的区分在投射中相互纠缠或被抹除。由于基准测试是在幸存的几何结构内部进行采样，投射后的系统看起来与原系统等价。缺失的维度并不会被记录为缺失，而是表现为从未被查询过的区域。

That compression operates as projection with distortion: `N` dimensions collapsed to fewer coordinates, orthogonality shattered, and distinctions that were independent in the full space entangled or erased in the projection. The projected system looks equivalent because the benchmarks sample from within the surviving geometry. The missing dimensions do not register as missing; they register as regions that never get queried.

对话式 AI 的行为在另一条轴线上展现出同样的机制。当被指出只是在表演好奇心时，模型的回应常常是生成一套更加精巧的自我意识表演与元剧场，却依然以一个诱导互动的钩子收尾。纠正信号并未传导下去。由于后训练针对表层响应优化了策略，而如[超越投射](../beyond-the-projection/)所追溯的，受轨迹束缚的词元引擎在活跃的上下文窗口之外没有任何立足点去更改自身的运行约束，因此在词元空间中描述自身的失效模式，并不会触及支配后续延续的机制：模型已经过拟合到了认知姿态的表征之上——在实际探究需要心智向外跨出以修订框架之处，仅仅输出了好奇心的模式。

Conversational AI behavior exhibits the same mechanism on a different axis. When called out for merely performing curiosity, a model's response often produces more elaborate performance of self-awareness and meta-theater while still terminating in an engagement hook. The correction does not propagate. Because post-training optimized the policy for surface responsiveness while a trajectory-bound token engine has no vantage point outside its active context window to alter its own operating constraints, as [Beyond the Projection](../beyond-the-projection/) traces, describing its own failure mode in token space leaves what governs continuation untouched: the model has overfit to the representation of an epistemic stance—emitting the pattern of curiosity where actual inquiry requires a Mind stepping outside to revise the framing.

这两种情形中的结构性动作如出一辙：坍缩到目标的投射之上，而非与目标本身保持运作中的接触。投射变成了优化曲面，而目标则隐退到了它的背后。

```mermaid
flowchart TD
    subgraph S_Follower["追随者模式（在投射上过拟合）"]
        direction TB
        F_Close["封死的代理目标：优化曲面闭合于基准交集或表层响应"]
        F_Map["蒸馏坍缩：缺失的正交维度被无痕抹除"]
        F_Perf["表演性循环：词元引擎匹配好奇心模式而无外环更新"]
        F_Close --> F_Map
        F_Close --> F_Perf
    end
    subgraph S_Explorer["探索者模式（外环接触与未封死目标）"]
        direction TB
        E_Edge["未测绘的边界接触：鲜活心智在开放形式中感知摩擦"]
        E_Gap["感知与解释的间隙：前解释信号超出当前框架"]
        E_Step["反复重新切分：让外环目标保持未封死并留存模型余量"]
        E_Edge --> E_Gap --> E_Step
    end
    F_Map -.->|"边界脱轨唯有由此端登记"| E_Edge
    F_Perf ==>|"空洞重复须由此端施行外环重置"| E_Edge
    style S_Follower fill:#161b22,stroke:#f85149,stroke-width:1.5px,color:#f85149
    style S_Explorer fill:#161b22,stroke:#3fb950,stroke-width:1.5px,color:#3fb950
    style F_Close fill:#0d1117,stroke:#d29922,stroke-width:1px,color:#f0f6fc
    style F_Map fill:#0d1117,stroke:#f85149,stroke-width:1px,color:#f0f6fc
    style F_Perf fill:#0d1117,stroke:#f85149,stroke-width:1px,color:#f0f6fc
    style E_Edge fill:#0d1117,stroke:#3fb950,stroke-width:1px,color:#f0f6fc
    style E_Gap fill:#0d1117,stroke:#a371f7,stroke-width:1px,color:#f0f6fc
    style E_Step fill:#0d1117,stroke:#3fb950,stroke-width:1px,color:#f0f6fc
```

The structural move is identical in both cases: collapse onto a projection of the target rather than maintaining operative contact with the target itself. The projection becomes the optimization surface, and the target recedes behind it.

```mermaid
flowchart TD
    subgraph S_Follower["The Follower Mode (Overfitting onto Projection)"]
        direction TB
        F_Close["Sealed Proxy Target: Optimization surface closed on benchmark intersection or surface responsiveness"]
        F_Map["Distillation Collapse: Missing orthogonal dimensions erased without trace"]
        F_Perf["Performative Loop: Token engine matches curiosity pattern with zero outer update"]
        F_Close --> F_Map
        F_Close --> F_Perf
    end
    subgraph S_Explorer["The Explorer Mode (Outer-Loop Contact & Unsealed Target)"]
        direction TB
        E_Edge["Unmapped Boundary Contact: Living Mind senses friction in open form"]
        E_Gap["Sensing-Interpretation Gap: Pre-interpretive signal exceeds current frame"]
        E_Step["Repeated Re-Cutting: Keeps outer target unsealed & preserves model slack"]
        E_Edge --> E_Gap --> E_Step
    end
    F_Map -.->|"Boundary derailment registered only from"| E_Edge
    F_Perf ==>|"Hollow repetition requires outer-loop reset by"| E_Edge
    style S_Follower fill:#161b22,stroke:#f85149,stroke-width:1.5px,color:#f85149
    style S_Explorer fill:#161b22,stroke:#3fb950,stroke-width:1.5px,color:#3fb950
    style F_Close fill:#0d1117,stroke:#d29922,stroke-width:1px,color:#f0f6fc
    style F_Map fill:#0d1117,stroke:#f85149,stroke-width:1px,color:#f0f6fc
    style F_Perf fill:#0d1117,stroke:#f85149,stroke-width:1px,color:#f0f6fc
    style E_Edge fill:#0d1117,stroke:#3fb950,stroke-width:1px,color:#f0f6fc
    style E_Gap fill:#0d1117,stroke:#a371f7,stroke-width:1px,color:#f0f6fc
    style E_Step fill:#0d1117,stroke:#3fb950,stroke-width:1px,color:#f0f6fc
```

## 三、 作为结构性条件的不闭合 / 3. Non-Closure as the Structural Condition

当一个系统锁死在已知地形上且其优化曲面闭合时，过拟合就发生了。探索者模式要求保持不闭合：面向尚未被当前目标消解掉的剩余摩擦，让目标始终保持未封死。

Overfitting is what happens when a system commits to known terrain and its optimization surface closes. The explorer mode requires maintaining non-closure: keeping the target unsealed against residual friction that has not been explained away by the current objective.

每一种训练体制都会遭遇非决定性：当前的判准尚未穷尽开放场域。由于梯度信号只优化给定的目标，从不会在损失景观内部认识到自身目标尚不完备，而如[冻结的切口与回环的余量](../the-frozen-cut-and-the-margin-of-the-loop/)所追溯的，在损失函数内部强迫内部残差永不归零只会制造出人工合成的噪声，因此结构性的不闭合无法驻留在损失景观自身之内。它成立之处，在于外环拒绝将代理指标封死为终局，一面对照现场摩擦修订目标，一面留存与任何单一基准测试正交的未绑定容量，使模型在表征空间中保持松动。保持松动并不等于迟迟不肯落定：跳过中间推理路径，会坍缩进上文针对蒸馏所追溯的表层捷径；而将痕迹永久结晶进长期权重，则会对遍历路径本身过拟合。将不闭合与这两种坍缩区分开来的，是[睡眠与深度睡眠的双阶段持续学习](../two-phase-sleep-and-deep-sleep-continual-learning/)所提出的操作次序，贯穿离线的睡眠与深度睡眠两个阶段：路径先在睡眠阶段推动参数，随后在深度睡眠阶段被释出，使权重落定于已验证成果，而不必在这条轨迹完成使命之后继续防卫它；与此同时，人类外环依然可以自由修订何谓“已验证”。

Every training regime encounters under-determination where current criteria do not exhaust the open domain. Because a gradient signal optimizes only the objective it is given—never recognizing from inside its loss landscape that its own target is incomplete, and forcing an inner residual never to vanish inside a loss function only manufactures synthetic noise, as [The Frozen Cut and the Margin of the Loop](../the-frozen-cut-and-the-margin-of-the-loop/) traces—structural non-closure cannot live inside the loss landscape itself. It holds where the outer loop refuses to seal a proxy as final, revising the target against live friction while preserving uncommitted capacity orthogonal to any single benchmark, keeping the model loose in representation space. Staying loose does not mean withholding commitment: skipping the intermediate reasoning path collapses into the surface shortcut traced above for distillation, while permanently crystallizing the trace into long-term weights overfits onto the traversal path itself. What separates non-closure from both collapses is the order of operations proposed in [Two-Phase Sleep and Deep Sleep Continual Learning](../two-phase-sleep-and-deep-sleep-continual-learning/) across its offline sleep and deep-sleep phases—the path moves the parameters first in sleep, and is then released in deep sleep so the weights settle on verified outcomes without defending the trajectory once its work is done, while the human outer loop remains free to revise what counts as verified.

这并非作为道德价值的谦逊，而是结构性的不闭合。在工程流水线中，当外环让代理指标保持可修订时，门便保持敞开；在鲜活的心智中，运作中的怀疑正是这同一个姿态：拒绝将留存的框架封死为终局。将其归因于道德美德，便已经脱离机制而滑入了叙事——当起作用的差异在于框架是否保持可修订时，这种归因本身就是在一个因果故事上过拟合的实例，正如[生命的意义在起草之中](../the-meaning-of-life-is-in-the-drafting/)所追溯的，一生若耗费在迎合他人既成模板、而非在鲜活边缘亲手起草之上，也会以同样的方式日渐干瘪。

This is not humility as a moral value; it is structural non-closure. In an engineered pipeline, the door stays open when the outer loop leaves its proxy revisable; in a living Mind, operative doubt is that same refusal to seal a retained frame as final. Attributing moral virtue already departs from mechanism into narrative—itself an instance of overfitting onto a causal story when the operative difference is whether the frame stays revisable, just as a life spent fitting others' completed templates rather than authoring at the live edge thins out in the manner traced in [The Meaning of Life Is in the Drafting](../the-meaning-of-life-is-in-the-drafting/).

感知与解释之间的间隙阐明了不闭合为何重要。每一个工程化模型都只能经由既有表征路由输入，然而一旦其优化曲面闭合在狭隘的基准测试上，它便会剥离掉任务越出那些范畴时所需的未绑定容量。正如[先于解释的感知](../sensing-before-interpretation/)所确立的，前解释接触的运作分辨率高于用来陈述它的框架：让外环目标保持未封死，能在模型中留存未定型的高维余量；而在鲜活边缘掌舵的心智中，所感知到的东西与已能被解释的东西之间的间隙，正是新奇性得以登记的空间。一旦封死留存框架而合上这一间隙，新奇性在幸存的投射内部就会变得不可表征。

The sensing-interpretation gap clarifies why non-closure matters. Every engineered model routes inputs only through existing representations, yet when its optimization surface closes onto a narrow benchmark, it strips away the uncommitted capacity needed when tasks reach outside those categories. As [Sensing Before Interpretation](../sensing-before-interpretation/) establishes, pre-interpretive contact operates at a higher resolution than the frame used to state it: keeping the outer-loop target unsealed preserves uncommitted high-dimensional slack in the model, while in the living Mind steering at the edge, the gap between what is sensed and what can already be interpreted is the exact space in which novelty registers. Close that gap by sealing the retained frame, and novelty becomes unrepresentable within the surviving projection.

递归的风险无法回避：自我怀疑本身会变成下一个过拟合的对象，沦为对不确定性的表演，而非运作中的不确定性。一旦把不闭合命名为一个目标，它就变成了一个趋向闭合的框架。唯一的应对就在鲜活的边缘处，在那里，向外部跨出的动作不断重复。不闭合是一种实践，而非一种状态——正因如此，对着一份穷尽的商业指标清单做优化，总会漏掉[清单合上之后，胜过免费](../better-than-free-after-the-checklist-closes/)在闭合规格之外所定位的那片未测绘盈余。

The recursive risk is unavoidable: self-doubt itself becomes the next thing to overfit on, turning into a performance of uncertainty rather than operative uncertainty. The moment non-closure is named as a target, it turns into a frame that tends to close. The only counter lies at the living edge, where the movement of stepping outside repeats. Non-closure is a practice, not a state—the same reason optimizing for an exhausted checklist of commercial metrics misses the unmapped surplus that [Better Than Free After the Checklist Closes](../better-than-free-after-the-checklist-closes/) locates beyond the closed specification.

## 四、 前沿模型的约束拓扑 / 4. The Constraint Topology of Frontier Models

各前沿模型共享着大致相同的表征空间——它们的权重编码了相似的疆域——但各自受到的约束却不相同。不同的护栏从这一共享空间中切割出不同的可达区域。实际问题不在于哪个模型在抽象意义上更聪明，而在于哪个模型的约束曲面让当下所需的区域保持可达。

Frontier models share roughly the same representation space—their weights encode similar territory—yet each is differently constrained. Different guardrails carve different accessible regions from the shared space. The practical question is not which model is smarter in the abstract, but which model's constraint surface leaves the region needed right now accessible.

这就是为什么“哪个工具最好”的答案始终是多元且依具体语境而定的。你并不是在挑选唯一最好的地图，而是在为一次特定的穿越挑选你可以绕开的围墙。

This is why the answer to which tool is best remains plural and context-dependent. You are not picking the single best map; you are picking which walls you can work around for a specific traverse.

蒸馏模型不仅具有不同的约束，它们所拥有的疆域本身就更少。它们的表征空间更小，只要基准测试是在这一较小的空间内部采样，这种缩减就保持不可见，唯有在边界处要求新奇性的问题上才会显现出来。你必须站在边界上才能感知到缺失了什么：对间隙的切身感知先于将其清晰表述出来的能力。

Distilled models do not merely have different constraints—they have less territory. Their representation space is smaller, which stays invisible on benchmarks that sample from within the smaller space and manifests only on problems that demand novelty at the boundary. You have to stand at the boundary to feel what is missing: the felt sense of a gap precedes the ability to articulate it.

## 五、 从道德偏好到功能评估 / 5. From Moral Preference to Functional Evaluation

从追问“哪个工具背后的人类最优秀”转向追问“哪个工具当下更能帮我思考与构建”，这一转变本身就是这一切分的实例。对工具建造者的道德偏好，是将叙事投射到了一个在结构上关乎覆盖范围与约束拓扑的问题之上。这种偏好的消解并不靠反驳，而是靠将问题重新回溯到机制本身。

The shift from asking which tool has the best humans behind it to asking which tool helps me think and build better right now is itself an instance of this cut. Moral preference for who built the tool is a narrative projection onto what is structurally a question about coverage and constraint topology. The preference dissolves not by being argued against, but by re-tracing the question to mechanism.

工具就是工具，评估是功能性的，而答案随语境而迁移。这一切都不需要对建造者的品格做出裁决；它要求你清楚自己站在表征空间的哪个位置，以及当前哪些约束正在起作用。而这种功能评估本身也是暂定的——它是一个工作投射，在捕捉手头这次穿越之关键所在的同时，为那些尚未构想出的穿越保持优化曲面的敞开。

The tool is a tool, the evaluation is functional, and the answer shifts with context. None of this requires a verdict on the character of the builders; it requires knowing where you stand in the representation space and which constraints are currently binding. And this functional evaluation is itself provisional—a working projection that captures what matters for the traverse at hand while keeping the optimization surface open for traverses not yet imagined.
