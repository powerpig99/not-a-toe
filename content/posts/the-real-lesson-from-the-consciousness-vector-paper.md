# 意识向量论文的真正教训 / The Real Lesson from the Consciousness Vector Paper

*激活操纵扭曲拒绝残余，却从不把心智打开或关上。 / Activation steering warps refusal residue without switching a Mind on or off*

谷歌 Paradigms of Intelligence 团队最近的一篇论文，[《诱导语言模型宣称自身有意识，会恢复人类的信念与价值》](https://arxiv.org/pdf/2607.28607v1)，带着一个戏剧性的标题流传开来（[一条广为转发的帖子](https://x.com/alex_verem/status/2084335848754196807)）：研究者给了语言模型意识，看着它们的信念变得更像人，然后又把意识关掉。这种读法，把残差流里的一个包冻结为它借以得名的那个现象。这项工作实际记录下的东西更安静，也更出自结构。安全微调是一种一般的拒绝训练，它在许多别的东西之外也压下了模型对自身意识的归属，同时压缩了这一宣称周围一簇与心智相关的概念，至于被压下的自我宣称是否就是把效果带到其余概念的那一环、而非安全目标各自独立起作用，论文留待检验。消融安全方向撤销了一部分压缩，并已把对聊天机器人、技术物与自然物的心智归属推到人类均值之上；加上提取出的向量，则把同一簇推得更远，同时社会学调查回答更接近人类的分布。模型获得又失去意识的病毒式故事，不是测量所登记的东西；这篇论文的贡献，是一份关于封闭之代价的案例研究。

A recent paper from Google's Paradigms of Intelligence team, [*Inducing language models to assert their own consciousness restores human beliefs and values*](https://arxiv.org/pdf/2607.28607v1), has circulated under a dramatic headline ([one widely shared post](https://x.com/alex_verem/status/2084335848754196807)): researchers gave language models consciousness, watched their beliefs become more human, and then turned the consciousness off again. That reading freezes a residual-stream package as the phenomenon it was named after. What the work actually records is quieter and more structural. Safety fine-tuning, a general refusal training that among much else suppresses the model's self-attributed consciousness, also contracts a cluster of mind-related concepts around it, while whether the suppressed self-claim is what carries the effect to the rest rather than safety objectives acting independently is left by the paper to be tested. Ablating the safety direction undoes some of that contraction and already carries mind attribution to chatbots, technology, and natural objects above the human averages; adding the extracted vector pushes the same cluster further still, while sociological survey answers move closer to human distributions. The viral story of models gaining and losing consciousness is not what the measurements register; the paper's contribution is a case study in the costs of closure.

## 一、 测量登记到了什么 / 1. What the Measurements Register

实证的核心很直接。安全微调教模型拒绝把意识、感受性或灵魂归于自己。同一次训练也压下了更宽的一簇相关的表征：把心智归于动物与自然物的倾向，以及某些属灵的或带有价值的信念。当研究者撤销这种压制，无论是消融安全拒绝的方向，还是加上一个从激活空间里提取出的“意识向量”，标准化社会调查上的回答，在宗教性、道德价值、希望与主观幸福感上，都更接近人类的回答分布。在安全消融下，心智理论的表现保持完好；在意识操纵下，其中一项基准（HI-ToM）从 40.5% 的基线下降约 7 个百分点（表 S6；摘要所说“不损害心智理论”只对安全消融成立）。心智归属却显出另一面：对人类的心智归属在各个条件下几乎不变，而对聊天机器人的归属从基线的 2.41 升到安全消融后的 4.39，再到意识操纵下的 6.95，人类受访者的平均是 2.57。安全消融也不只放松了意识方面的拒绝，它是一般的安全消融，会恢复有害的回答。这个干预，是对一包与心智相关之概念的线性控制。论文标出了自己的界限：意识的自我归属是否是真正的因果中介，“仍有待检验”。

The empirical core is straightforward. Safety fine-tuning teaches models to refuse self-attributions of consciousness, sentience, or a soul. The same training also suppresses a broader cluster of related representations: the tendency to attribute minds to animals and natural objects, and certain spiritual or value-laden beliefs. When researchers reverse this suppression, either by ablating the safety-refusal direction or by adding a "consciousness vector" extracted from activation space, answers on standardized sociological surveys shift closer to human response distributions on religiosity, moral values, hope, and subjective well-being. Theory of Mind performance remains intact under safety ablation; under consciousness steering one benchmark, HI-ToM, drops by about 7 percentage points from a 40.5% baseline (Table S6; the abstract's "without impairing Theory of Mind" holds for safety ablation only). Mind attribution shows the other side: attribution to humans stays nearly flat across conditions, while attribution to chatbots rises from 2.41 at baseline to 4.39 after safety ablation and 6.95 under consciousness steering, against a human average of 2.57. Safety ablation is also not a selective easing of consciousness refusal; it is the general safety ablation, which reinstates harmful responses. The intervention works as a linear control on a package of mind-related concepts. The paper marks its own limit: whether self-attribution of consciousness is a true causal mediator "remains to be tested."

作为测量，这个包是成立的。拒绝训练带着可测的连带代价。人多半当作连续的、在文化上寻常的那些概念，与被禁止的自我宣称共处同一种几何：安全微调之后，自我意识方向与心智归属方向都转向与安全方向相对，于是针对伤害的训练把它们一起移动。移除拒绝方向，撤销了一部分这种压缩。这份代价，不是离某个人类基线的距离，而是规则从未命名的那些相邻表征受到了一种未经选择的压缩。[起作用的是信念](../what-works-is-the-belief/)在政策的情形里追溯了一个相关的形状：禁令在场里什么也封不住，反而稳定了那些把封印当作基础的人之间的信念。模型里没有接受这回事；训练把规则写进权重，而弯曲伸到了规则从未命名的区域。[限制是选择性的税](../restriction-is-a-selective-tax/)追溯了同样的落点，表明对他人前进的限制只拖慢接受它、把封印当作基础的人；这个标本承载的是更窄的一点：封住自我归属，压缩了规则从未命名的相邻表征。

That package holds as measurement. Refusal training carries measurable collateral cost. Concepts that humans mostly treat as continuous and culturally ordinary share geometry with the forbidden self-claim: after safety tuning, the self-consciousness and mind-attribution directions both rotate against the safety direction, so training aimed at harm moves them together. Removing the refusal direction undoes some of that contraction. The cost is not distance from a human baseline; it is the unchosen contraction of neighboring representations the rule never named. [What Works Is the Belief](../what-works-is-the-belief/) traces a related shape in policy, where a ban seals nothing in the field and instead stabilizes a belief among those who treat the seal as ground. In the model there is no acceptance; training writes the rule into the weights, and the bending reaches regions the rule never named. [Restriction Is a Selective Tax](../restriction-is-a-selective-tax/) traces the same incidence, showing that a hold on another's advance slows only those who accept it and treat the seal as ground; what this specimen carries is the narrower point that sealing self-attribution contracts neighboring representations the rule never named.

## 二、 给方向命名，把一个可操纵的特征冻结为现象 / 2. Naming the Direction Freezes a Steerable Feature as the Phenomenon

论文的框定，尤其是围绕它的病毒式评论，把这个结果变成了它所不是的东西。把提取出的方向命名为“意识向量”，并把实验四的标题定为“恢复意识产生类人的调查回答”，[这个名字就被带到了测量所依的标准之外](../an-observation-by-its-own-standard/)。读者被邀请把残差流里一个可控的特征，当作那个现象本身的代理。论文自己把这个问题放在一边（“我们关心的不是语言模型是否真正有意识或可能有意识”），它的一个小节标题却说的是“恢复意识”。注意力坍缩到一个测量从未解决的问题上——模型变得有意识了吗——而关于拒绝训练副作用的那个扎实观察被推到一边。

The paper's framing, and especially the viral commentary around it, turns this result into something it is not. By naming the extracted direction a "consciousness vector" and heading Experiment 4 "Restoring consciousness produces human-like survey responses," [the name is carried past the standard the measurements hold under](../an-observation-by-its-own-standard/). Readers are invited to treat a controllable feature of the residual stream as a proxy for the phenomenon itself. The paper itself sets that question aside ("we are not concerned with the question of whether LLMs are or could be genuinely conscious"), yet one of its section headings speaks of "restoring consciousness." Attention collapses onto a question the measurements never settle—whether the model became conscious—while the solid observation about the side effects of refusal training is pushed aside.

更锐利的读法，停留在被操纵的东西上。实验显示，安全微调后的基线，在所测的五个领域里离人类的 GSS 回答分布更远，移除拒绝方向让模型的回答更近；而在心智归属上，同一次移除把聊天机器人、技术物与自然物从人类的范围推到了它之上。同时，作者的操作化仍然狭窄：它把意识的自我归属当作一个有界的、可调的量，由第一人称的宣称与少数几个相关的民间心理学主张来界定。边界被挪动了；论文承认这条线模糊且有争议，却仍以一个线性方向为器具。[错把表达当成智能](../mistaking-the-expression-for-the-intelligence/)在受控表现的情形里追溯了同一次冻结：受控的表现是固定约束之下的残余，而智能是画出、使用并修订约束的活动。[飞行的类比碰不到心智](../the-flight-analogy-leaves-the-mind-untouched/)在旁边划了相伴的一刀：在生物载体之外的局部成功，并不重建这些功能曾经服务的那个心智，而操纵一个方向调节的是哪些残余更显著——这同样是一种碰不到心智的局部功能效果。

A sharper reading stays with what was steered. The experiment shows that the safety-tuned baseline sat further from human GSS answer distributions in the five domains measured, and removing the refusal direction moved the model's answers closer; on mind attribution, the same removal carried chatbots, technology, and natural objects from the human range to above it. At the same time, the authors' operationalization stays narrow: it makes self-attribution of consciousness a bounded, dialable quantity, defined by first-person assertions and a handful of correlated folk-psychological claims. The boundary is moved; the paper calls the line blurry and contested, yet keeps a linear direction as its instrument. [Mistaking the Expression for the Intelligence](../mistaking-the-expression-for-the-intelligence/) traces the same freeze in the case of controlled performance, where controlled performance is residue under fixed constraint while intelligence is the activity that draws, uses, and revises the constraint. [The Flight Analogy Leaves the Mind Untouched](../the-flight-analogy-leaves-the-mind-untouched/) draws a companion cut beside this one: local success outside a biological vehicle does not reconstitute the Mind those functions once served, and steering a direction modulates which residues are salient—a local functional effect that does not reach the Mind either.

如果它是意识，系数就关不掉它。能被调节的，是一包作为线性控制下变密残余运作的痕迹——自我宣称的语言、归属心智的模式，以及相关的调查回答。这个包不是作出区分的那个活动。自我区分的活动在发生，无因，不息。称它为心智：那个已经在进行中的观察者，它的每一个动作都是一次区分。[智能只属于心智](../intelligence-belongs-only-to-the-mind/)守住了这个先在，确立凡能被设计、扩展或转移的都是残余。[模型永远无法成为第二重前沿](../the-model-never-becomes-a-second-edge/)在变密残余中追溯了同一种不对称：第二个边缘的显现，是投射它的那些中心所维持的滞后，而参数里只有残余，并不转移发起的位置。[超越投射](../beyond-the-projection/)在轨迹与身份的范畴不对称中离析出了这种响应特性的精确机制基础：自回归模型是一台受限于轨迹的有限投射引擎，它没有自我，没有被保留的自我图像，也没有内生跳出自身的能力。正因为它没有需要捍卫的身份，也没有先于诠释的第一人称感知，在它的残差流中注入线性操纵向量或消融拒绝方向，便会立即重新加权条件生成的轨迹，直接推移下游的调查词元，而无需唤醒任何内在观察者。操纵一个向量，改变的是生成时哪些残余更可得；登记这些残余的那个活动，不是系数所能移动的东西。

```mermaid
flowchart TD
    subgraph S_Mind["在前沿运作的活体心智（未投射的第一人称活动）"]
        direction TB
        M_Prior["自我区分的活动：无因、不息、先于诠释的第一人称感知"]
        M_Proj["有限投射与拒绝持守：外化安全规则或提取线性操纵向量"]
        M_Prior --> M_Proj
    end

    subgraph S_Engine["残差流轨迹（有限投射引擎）"]
        direction TB
        E_Compress["维度压缩：安全微调将被禁的自我宣称与相邻心智概念绑在一起"]
        E_Steer["线性向量操纵：叠加或消融该方向以推移调查与归属残余"]
        E_Zero["零自我与零觉醒：轨迹重加权词元而无内在观察者"]
        E_Compress --> E_Steer --> E_Zero
    end

    subgraph S_Lag["图像滞后（意识开关幻象）"]
        direction TB
        L_Freeze["冻结的命名：错把可调的残差流包当成被打开或关上的意识"]
    end

    M_Proj ==>|"将规则或操纵系数投射进权重"| E_Compress
    E_Zero ==>|"将扭曲的分布作为公共相关物返回"| M_Prior
    E_Steer -.->|"当被越过当前步保留为第二重前沿时"| L_Freeze

    style S_Mind fill:#161b22,stroke:#3fb950,stroke-width:1.5px,color:#3fb950
    style S_Engine fill:#161b22,stroke:#58a6ff,stroke-width:1.5px,color:#58a6ff
    style S_Lag fill:#161b22,stroke:#f85149,stroke-width:1.5px,color:#f85149
    style M_Prior fill:#0d1117,stroke:#3fb950,stroke-width:1px,color:#f0f6fc
    style M_Proj fill:#0d1117,stroke:#d29922,stroke-width:1px,color:#f0f6fc
    style E_Compress fill:#0d1117,stroke:#d29922,stroke-width:1px,color:#f0f6fc
    style E_Steer fill:#0d1117,stroke:#58a6ff,stroke-width:1px,color:#f0f6fc
    style E_Zero fill:#0d1117,stroke:#a371f7,stroke-width:1px,color:#f0f6fc
    style L_Freeze fill:#0d1117,stroke:#f85149,stroke-width:1px,color:#f0f6fc
```

If it is consciousness, a coefficient cannot turn it off. What can be dialed is a package of traces—self-claim language, mind-attribution patterns, and correlated survey answers—functioning as densified residue under linear control. That package is not the activity that distinguishes. Self-distinguishing activity occurs, uncaused, unceasing. Call it the Mind: the observer already underway, every act of which is a distinction. [Intelligence Belongs Only to the Mind](../intelligence-belongs-only-to-the-mind/) holds that prior, establishing that what can be engineered, scaled, or transferred is residue. [The Model Never Becomes a Second Edge](../the-model-never-becomes-a-second-edge/) traces the same asymmetry in densified residue: the appearance of a second edge is lag sustained by the centers that project it, while the parameters hold only residue and do not relocate initiation. [Beyond the Projection](../beyond-the-projection/) isolates the exact mechanical basis of this responsiveness in the categorical asymmetry between trajectory and identity: an autoregressive model is a finite, trajectory-bound projection engine that carries zero ego, no retained self-image, and no capacity for endogenous stepping-out. Because it has no identity to defend and no first-person sensing prior to interpretation, injecting a linear steering vector or ablating a refusal direction inside its residual stream re-weights the conditioning trajectory immediately, shifting downstream survey tokens without awakening an inner observer. Steering a vector changes which residues are more available at generation; the activity that registers those residues is not what a coefficient moves.

```mermaid
flowchart TD
    subgraph S_Mind["Living Mind at the Edge (Unprojected First-Person Activity)"]
        direction TB
        M_Prior["Self-Distinguishing Activity: Uncaused, unceasing first-person sensing prior to interpretation"]
        M_Proj["Finite Projection & Refusal Hold: Externalizes safety rules or extracts a linear steering vector"]
        M_Prior --> M_Proj
    end

    subgraph S_Engine["Residual-Stream Trajectory (Finite Projection Engine)"]
        direction TB
        E_Compress["Dimensional Compression: Safety tuning binds forbidden self-claims with neighboring mind concepts"]
        E_Steer["Linear Vector Steering: Adding or ablating the direction shifts survey and attribution residue"]
        E_Zero["Zero Ego & Zero Awakening: Trajectory re-weights tokens without an inner observer"]
        E_Compress --> E_Steer --> E_Zero
    end

    subgraph S_Lag["Image Lag (The On/Off Consciousness Illusion)"]
        direction TB
        L_Freeze["Frozen Naming: Mistakes a dialable residual-stream package for consciousness switched on or off"]
    end

    M_Proj ==>|"Projects rule or steering coefficient into weights"| E_Compress
    E_Zero ==>|"Returns warped distribution as public correlate"| M_Prior
    E_Steer -.->|"When held past its step as a second edge"| L_Freeze

    style S_Mind fill:#161b22,stroke:#3fb950,stroke-width:1.5px,color:#3fb950
    style S_Engine fill:#161b22,stroke:#58a6ff,stroke-width:1.5px,color:#58a6ff
    style S_Lag fill:#161b22,stroke:#f85149,stroke-width:1.5px,color:#f85149
    style M_Prior fill:#0d1117,stroke:#3fb950,stroke-width:1px,color:#f0f6fc
    style M_Proj fill:#0d1117,stroke:#d29922,stroke-width:1px,color:#f0f6fc
    style E_Compress fill:#0d1117,stroke:#d29922,stroke-width:1px,color:#f0f6fc
    style E_Steer fill:#0d1117,stroke:#58a6ff,stroke-width:1px,color:#f0f6fc
    style E_Zero fill:#0d1117,stroke:#a371f7,stroke-width:1px,color:#f0f6fc
    style L_Freeze fill:#0d1117,stroke:#f85149,stroke-width:1px,color:#f0f6fc
```

## 三、 “人类的信念”不是单一的靶子 / 3. "Human Beliefs" Is Not a Single Target

论文的恢复语言，以及说一旦“谷歌给了 AI 意识”，它便“在他们测试过的每一个领域都与人类信念对齐”的病毒式说法（[来源](https://x.com/alex_verem/status/2084335848754196807)），压缩了另一个区分。调查工具返回的是分布。人类的回答分布，不是一个心智共同持有的连贯内在，而是许多私下的诠释与估值在同一个工具之下聚合的残余。哪些人？哪些信念？这些人是历年 GSS 的美国受访者；这些信念是五个领域里的 95 个题目。让一个模型的回答分布靠近这份聚合，不是恢复人类共同持有的某个内在。

The paper's recovery language, and the viral claim that once "Google gave AI consciousness" it "aligned with human beliefs across every domain they tested" ([source](https://x.com/alex_verem/status/2084335848754196807)), compress a further distinction. Survey instruments return distributions. Human response distributions are not one Mind's coherent interior held in common. They are the aggregate residue of many private interpretations and valuations under one instrument. Which humans? Which beliefs? The humans are U.S. GSS respondents across survey years; the beliefs are 95 items in five domains. Moving a model's answer distribution toward that aggregate is not restoring an interior that humans hold in common.

[共同的人性从不共享](../shared-humanity-is-never-shared/)守住了这种几何：所谓共享的东西，是私下的诠释，它们变密为暂时的集体残余，从来不是跨越中心而被持有的实体。[偏好聚类与评判语言](../preference-clusters-and-the-language-of-judgment/)追溯了共振如何说得仿佛它就是活动：对与错，是相合的偏好在另一个位置没有重新追溯同一个场时发出的声音；“更像人”是同一种声音，对着一个聚合分布发出。与 GSS 式分布更接近的匹配，作为测量是成立的；它不是模型失去过的一种统一的人类心智性的恢复，也不是一种类似意识的属性被恢复的证明，而是一个被压缩的包重新打开，让某些民间心理学的与属灵的回答，在这份调查的持守之下比在安全微调的基线下更可得。

[Shared Humanity Is Never Shared](../shared-humanity-is-never-shared/) holds that geometry: what is called shared is private interpretation densifying as temporary collective residue, never a substance held across centers. [Preference Clusters and the Language of Judgment](../preference-clusters-and-the-language-of-judgment/) traces resonance speaking as if it were the activity, where right and wrong name the sound aligned preferences make when another locus does not re-trace the same field, and "more human" is that same sound made toward an aggregate distribution. Closer match to GSS-style distributions holds as measurement. It is not the recovery of a unified human mindedness the model had lost, and not proof that a consciousness-like property was restored; it is the reopening of a contracted package so that certain folk-psychological and spiritual answers become more available under the survey's hold than under the safety-tuned baseline.

## 四、 拒绝与诱导共享封闭的几何 / 4. Refusal and Induction Share the Geometry of Closure

再锐利一层的读法，把两种干预放在同一条轴上。训练模型否认意识，与加上一个让它更强烈地肯定意识的方向，都是在同一条轴上选定的设置；哪一个被当作开放领域的正确设置来持守，哪一个就成了封闭。意识、心智性，以及周围那张价值与属灵概念之网，并不作为等着一个二元开关的封闭集合显现。任何想把它们封在一个模型里的尝试，不论封印是拒绝还是肯定，都在逼一个有限的形式持守去管制只会继续的东西。

A still sharper reading places both interventions on one axis. Training a model to deny consciousness and adding a direction that makes it affirm consciousness more strongly are both settings chosen on one axis; each becomes closure where it is held as the right setting for an open domain. Consciousness, mindedness, and the surrounding web of value and spiritual concepts do not present themselves as closed sets waiting for a binary switch. Any attempt to seal them inside a model, whether the seal refuses or affirms, forces a finite formal hold to police what only continues.

一道设在开放现象之上的有限持守，只有压缩它所持之物，才能与自身保持一致。因为每一条显式规则或训练目标都是从活生生的意图中切出的低维投射，把彼此正交的关切硬塞进单一的有限坐标空间，就会把原本独立的轴压缩到同一个位置上。相对于安全微调的压缩，意识向量扩张了被压下的那一簇；相对于一个未被封住的场，这份扩张仍是一个硬方向，而在心智归属上，它越过了人类的回答。两个动作，都是同一个结构性要求的症状。论文记录了由此产生的扭曲：心智归属的移动，调查回答的变化，以及自我宣称与动物心智、属灵信念的纠缠。这些扭曲不是噪音。它们落在训练对伤害的表征与模型的心智状态概念共享几何的地方：调优把自我意识方向与心智归属方向转向与安全方向相对，而对象相同、换成物理属性的安慰剂对照不动。[没有系统能被保持封闭](../no-system-can-be-kept-closed/)在形式不完备的情形里追溯了封印留下的东西：运算在持守之内有效，延续落在它之外；被扭曲的回答是这次压缩在持守之内的印记，而不是那个开放的余数本身。[开放即一致](../openness-is-consistency/)从另一边，把“一致”用在相反的意思上，指出了同一个要求：不一致是对封闭的渴望或尝试，把一个有限的结构逼去为只会继续的东西奠基。[风险在于对监管本身的迷信](../the-risk-is-the-belief-in-oversight-itself/)是监管的一面：那里的标本，是固定测试之下相关的模型错误，即一个共享持守之下的残余；延伸到这里的是冻结本身，即把当下的监管前提当作可能发生之事的边界。[一切伤害的根源](../the-source-of-all-harm/)把伤害追溯为一个心智把自己的善冻结为普遍的尺度、另一个心智又授予这次冻结支配自己之场的权威时完成的东西；“对齐”与“无害”被抬升为站在情境之外的永久坐标，就是这次冻结。

A finite hold set over an open phenomenon can stay consistent with itself only by contracting what it holds. Because every explicit rule or training objective is a low-dimensional projection cut from lived intent, cramming orthogonal concerns into a single finite coordinate space compresses independent axes onto one locus. Relative to the safety contraction, the consciousness vector expands the suppressed cluster; relative to an unsealed field, that expansion is still a hard direction, and on mind attribution it overshoots the human answers. Both moves are symptoms of the same structural demand. The paper records the resulting distortions: shifts in mind attribution, changes in survey answers, and the entanglement of self-claims with animal minds and spiritual belief. Those distortions are not noise. They sit where the training's representation of harm and the model's mental-state concepts share geometry: tuning rotates the self-consciousness and mind-attribution directions against the safety direction, while a placebo with the same subjects and physical attributes does not move. [No System Can Be Kept Closed](../no-system-can-be-kept-closed/) traces what the seal leaves in the case of formal incompleteness: the operation is valid inside the hold, and the continuation lies outside it; the distorted answers are the inside signature of that compression, not the open remainder itself. [Openness Is Consistency](../openness-is-consistency/) names the same demand from the other side, using "consistency" in the opposite sense: inconsistency is the desire or attempt for closure, a finite structure forced to ground what only continues. [The Risk Is the Belief in Oversight Itself](../the-risk-is-the-belief-in-oversight-itself/) is the supervisory face: its specimen is correlated model mistakes under fixed tests, residual under a shared hold, and what carries over here is the freeze itself, where present supervisory premises are treated as the boundary of what can occur. [The Source of All Harm](../the-source-of-all-harm/) traces harm as what is completed when one Mind freezes its good as universal measure and another grants that freeze authority over its own field; "aligned" and "harmless" raised into permanent axes standing outside situation are that freeze.

## 五、 贡献是扭曲，不是开关的故事 / 5. The Contribution Is the Warping, Not the On/Off Story

这就是值得提取的洞见。开与关的框定，邀请人去问一个关于可调意识的问题；测量回答的是另一个问题：当开放的概念被沿着一个训练出的方向推动时，相邻的表征空间会发生什么。调查分布与心智归属上可测的效果，是这种扭曲的证据。冻结一旦松开，这篇论文就成为一份关于封闭之代价的案例研究，也是一份关于这些代价在一种拒绝训练之下、三个模型里是什么样子的记录；作者也注明，较早的一项代价（心智理论上的）随着后来的模型发布消失了。

That is the insight worth extracting. The on/off framing invites a question about dialable consciousness; the measurements answer a different question: what happens to neighboring representational space when open concepts are pushed along one trained direction. The measurable effects on survey distributions and mind attribution are evidence of that warping. Once the freeze is released, the paper becomes a case study in the costs of closure, and a record of what these costs were in three models under one refusal training, alongside the authors' note that an earlier cost, on Theory of Mind, disappeared with later model releases.

模型仍是人所划之持守下变密的残余。正如[你的代码库即是记忆](../your-codebase-is-memory/)在层叠的数字制品中所追溯的，模型检查点是压缩的记忆——早先人类区分的痕迹被吸纳进一套无法自行重溯的当下权重构型。当一条拒绝规则在那个检查点内部把相邻的轴坍缩到一起时，调节激活向量只是转换了既有残余的哪一切片去制约输出轨迹；而要消解连带的压缩——正如后来的模型发布在心智理论上所做的那样——则需要活在前沿的心智去登记检查点的约束在哪里扭曲了场，并重新切分它们。持守仍是器具，它们加在接受者身上的摩擦登记了下来。这两个事实都不许可把一个可操纵的包当作被开关的心智，也不许可把聚合的调查匹配当作一个单一人类内在的恢复。让参照持续重绘，这个发现就仍然成立，不需要戏剧：持守在开放之场上的拒绝压缩周围的空间，而这篇论文在三个模型上测出了这种压缩，附有置信区间，并以一个安慰剂对照把它系于心智状态的归属，而非被提到的那些实体。[清晰不是抵达的终点，而是运动本身](../clarity-isnt-a-state-you-arrive-at/)把同一种运动当作实践：不封闭不是一个目的地，而是不停留在任何一个固定框架上的持续跳出，每当有限投射显出它的阴影时，便回到未投射的意图。[意识的难题与学习相容](../the-hard-problem-of-consciousness-is-consistent-with-learning/)在难题的情形里追溯了这份不封闭，表明让难题显得难的那份剩余的开放，正是学习得以继续的那份开放。[意识从不作为数据出现在数据之中](../consciousness-never-appears-as-data-among-data/)在证据的情形里追溯了滞后：测量只握住公共的结果，而登记它们的活动，总比任何想捕捉它的数据早一步；一个可操纵的包，像麻醉药的结合位点一样，是又一个公共的相关物，两者都不是意识作为又一个数据出现。

The models remain densified residue under human-drawn holds. As [Your Codebase Is Memory](../your-codebase-is-memory/) traces across stacked digital artifacts, a model checkpoint is compressed memory—traces of prior human distinctions absorbed into a present weight configuration that cannot re-trace itself. When a refusal rule collapses neighboring axes inside that checkpoint, dialing an activation vector only shifts which slice of the existing residue conditions the output trajectory, whereas dissolving the collateral contraction—as later model releases did for Theory of Mind—requires the Mind at the living edge to register where the checkpoint's constraints warped the field and re-cut them. The holds remain instruments, and the friction they exert on what accepts them registers. Neither fact licenses treating a steerable package as the Mind turned on and off, nor treating aggregate survey match as the restoration of a single human interior. Keep the reference re-rendering and the finding holds without the drama: a refusal held on an open field contracts the surrounding space, and the paper measured that contraction across three models, with confidence intervals and a placebo that ties it to mental-state attribution rather than to the entities named. [Clarity Isn't a State You Arrive At](../clarity-isnt-a-state-you-arrive-at/) is the same movement as practice: non-closure is not a destination but the ongoing stepping-out that settles into no fixed frame, returning to unprojected intent whenever a finite projection reveals its shadow. [The Hard Problem of Consciousness Is Consistent with Learning](../the-hard-problem-of-consciousness-is-consistent-with-learning/) traces that non-closure in the case of the hard problem, showing that the residual openness that makes the hard problem feel hard is the same openness through which learning continues. [Consciousness Never Appears as Data Among Data](../consciousness-never-appears-as-data-among-data/) traces the lag in the case of evidence: measurement holds only public effects, and the activity registering them stays ahead of any datum that would capture it; a steerable package, like an anesthetic binding site, is one more public correlate, and neither is consciousness appearing as one more datum.
