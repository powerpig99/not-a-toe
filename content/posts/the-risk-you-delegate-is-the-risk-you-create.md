# 你委托的风险就是你创造的风险 / The Risk You Delegate Is the Risk You Create

*将风险委托给集中审批关卡，会把分散递减的隐患转化为集中且自我维系的顽疾。 / Delegating risk to a central gate turns a distributed, declining hazard into a concentrated, self-sustaining one.*

美国公路上每年约有四万人丧生。NHTSA将大约94%的撞车事故归因于人为失误——分心、酒驾或药驾、疲劳、误判。这一数字几乎没有波动。它是人类驾驶车辆的基线代价，数十年来一直保持稳定。

Approximately 40,000 people die on American roads every year. NHTSA attributes roughly 94% of crashes to human error—distraction, impairment, fatigue, misjudgment. This number barely fluctuates. It is the baseline cost of humans operating vehicles, and it has been stable for decades.

没有任何机构为此担责。当这一数字维持不变时，没有哪个监管者会面临审查，也不会有头条新闻报道。这是前制度化的风险——分散在数以百万计的个体决策之中，每一次决策都很微小，也没有委托给任何人。你开车，你承担风险，而在汇总层面上它始终隐形，因为没有任何单一实体承接它。

No institution is accountable for this. No regulator faces scrutiny when the number holds steady. No headline runs. It is pre-institutional risk—distributed across millions of individual decisions, each one small, none of them delegated to anyone. You drive, you bear the risk, and it stays invisible in aggregate because no single entity holds it.

如今出现了一套能够可观测地降低这一风险的系统。特斯拉基于超过76亿英里的车队行驶里程报告称，受监督版FSD的碰撞率比全美平均水平低数倍。数据由企业自行报告，统计方法归特斯拉自有，用户群体存在自我筛选，且系统仍有赖人类驾驶员兜底。这些因素都至关重要，理应接受独立核验。然而即便大幅折算——哪怕把报告中七倍的安全性提升砍到两倍——信号依然清晰：一套在大规模部署后每年能挽救数千条生命的系统已经存在。请看接下来会发生什么。

Now a system emerges that measurably reduces this risk. Tesla reports, from over 7.6 billion fleet miles, that FSD (Supervised) produces collision rates multiple times lower than the national average. The data is self-reported, the methodology is Tesla's own, the users self-select, and the system includes a human driver as backstop. All of that matters and deserves independent verification. Yet even discounted heavily—cut the reported sevenfold improvement to twofold—the signal is clear: a system exists that, at scale, would prevent thousands of deaths annually. Watch what happens next.

## 一、 委托的动作 / 1. The Delegation Move

风险没有由每个个体自行选择如何接触这套新系统——亲自试用、评估并调整——而是被委托了出去。“总得有人确保它是安全的。”这个“有人”变成了一座机构：监管部门、标准制定机构、审批框架。个体向后退却，机构顺势介入。正如[主权、信念与规制结构的生成](../sovereignty-belief-and-regulatory-structures/)所揭示的，监管机构正是由“风险可以移交”这一信念构筑而成的。

Rather than each individual choosing their own exposure to the new system—trying it, assessing it, adjusting—the risk gets delegated. "Someone should make sure this is safe." That someone becomes an institution: a regulatory body, a standards agency, an approval framework. The individual steps back. The institution steps in. Regulators are built from the belief that this risk can be handed over, as [Sovereignty, Belief, and the Generation of Regulatory Structures](../sovereignty-belief-and-regulatory-structures/) shows.

这听起来像是负责任，实则是负责任的反面。风险一旦委托给机构，便在性质上发生了蜕变。监管者此刻对新系统的任何故障背负着高度集中的问责。如果他们批准了FSD，随后一起车祸登上了头条，这项批准就会遭到严厉审视。仕途就此断送，调查随之启动。一次错误的“放行”，其代价对机构而言是显眼的、可归咎的，甚至是灭顶的。

This feels like responsibility. It is its opposite. The moment risk delegates to an institution, it transforms in kind. The regulator now holds concentrated accountability for any failure of the new system. If they approve FSD and a crash makes headlines, the approval is scrutinized. Careers end. Investigations launch. The cost of a wrong "yes" is visible, attributable, and catastrophic for the institution.

而一次错误的“否决”——在旧基线下每天照常发生的110起死亡——其代价却是隐形的。没有人为现状担责。哪怕更安全的系统提早一年部署就能避免无数车祸，也没有哪个监管者会因为这些本可避免的伤亡而接受调查。这笔代价由陌生人分摊，四散分布、无从归咎，在做出决策的机构眼中处于结构性的盲区。

The cost of a wrong "no"—the 110 daily deaths that continue under the old baseline—is invisible. No one is accountable for the status quo. No regulator is investigated for the crashes that would not have occurred had the better system been deployed a year earlier. That cost is borne by strangers, distributed, unattributable, and structurally invisible to the institution making the decision.

于是机构做出了理性的优化：将可归咎的新型故障压到最低。这直接将不可归咎的持续伤害推到了最高。这不是出于恶意，也不是出于无能，而是源于责任委托出去之后，问责机制集中收缩的几何结构。

```mermaid
flowchart TD
    subgraph S_Dist["1. 分散选择（递减的风险）"]
        direction TB
        D_Act["数百万个体驾驶员自行评估、转向并承担局部风险"]
        D_Learn["车队级遥测与直接反馈持续压缩基线碰撞率"]
        D_Act --> D_Learn
    end
    subgraph S_Gate["2. 委托陷阱（集中的关卡）"]
        direction TB
        G_Hand["风险向上委托给审批框架（“确保它安全”）"]
        G_Asym["非对称账本：错误的“放行”断送仕途；错误的“否决”（每天110人丧生）无从归咎"]
        G_Loop["自我维系的延误：个体风险评估能力萎缩，关卡的必要性随之膨胀"]
        G_Hand --> G_Asym --> G_Loop
    end
    D_Act -.->|"放弃直接评估"| G_Hand
    G_Loop ==>|"收回不可代理的第一人称评估"| D_Act
    style S_Dist fill:#161b22,stroke:#3fb950,stroke-width:1.5px,color:#3fb950
    style S_Gate fill:#161b22,stroke:#f85149,stroke-width:1.5px,color:#f85149
    style D_Act fill:#0d1117,stroke:#3fb950,stroke-width:1px,color:#f0f6fc
    style D_Learn fill:#0d1117,stroke:#58a6ff,stroke-width:1px,color:#f0f6fc
    style G_Hand fill:#0d1117,stroke:#d29922,stroke-width:1px,color:#f0f6fc
    style G_Asym fill:#0d1117,stroke:#f85149,stroke-width:1px,color:#f0f6fc
    style G_Loop fill:#0d1117,stroke:#a371f7,stroke-width:1px,color:#f0f6fc
```

So the institution optimizes rationally: minimize attributable novel failure. This directly maximizes unattributable ongoing harm. Not through malice, not through incompetence—through the geometry of how accountability concentrates when responsibility delegates.

```mermaid
flowchart TD
    subgraph S_Dist["1. Distributed Choice (Diminishing Risk)"]
        direction TB
        D_Act["Millions of individual drivers assess, steer, and bear local risk"]
        D_Learn["Fleet-scale telemetry & direct feedback shrink baseline collision rate"]
        D_Act --> D_Learn
    end
    subgraph S_Gate["2. The Delegation Trap (Concentrated Gate)"]
        direction TB
        G_Hand["Risk delegated upward to an approval framework ('make sure it is safe')"]
        G_Asym["Asymmetric ledger: wrong 'yes' is career-ending; wrong 'no' (110 daily deaths) is unattributed"]
        G_Loop["Self-sustaining delay: individual risk-assessment atrophies while gate necessity grows"]
        G_Hand --> G_Asym --> G_Loop
    end
    D_Act -.->|"Abdicating direct assessment"| G_Hand
    G_Loop ==>|"Reclaiming unproxyable first-person evaluation"| D_Act
    style S_Dist fill:#161b22,stroke:#3fb950,stroke-width:1.5px,color:#3fb950
    style S_Gate fill:#161b22,stroke:#f85149,stroke-width:1.5px,color:#f85149
    style D_Act fill:#0d1117,stroke:#3fb950,stroke-width:1px,color:#f0f6fc
    style D_Learn fill:#0d1117,stroke:#58a6ff,stroke-width:1px,color:#f0f6fc
    style G_Hand fill:#0d1117,stroke:#d29922,stroke-width:1px,color:#f0f6fc
    style G_Asym fill:#0d1117,stroke:#f85149,stroke-width:1px,color:#f0f6fc
    style G_Loop fill:#0d1117,stroke:#a371f7,stroke-width:1px,color:#f0f6fc
```

## 二、 自我维系的回路 / 2. The Self-Sustaining Loop

此时，机构的存在意义变成了管理这一风险。它的经费、权力和存在价值，都仰赖于该风险持续需要被管理。审批流程越复杂，机构就越显必要；延误拖得越久，流向监管而非部署的资源就越多。机构无需密谋去延续风险——它用不着这么做。它的生存结构会自动完成这一切。

The institution now exists to manage the risk. Its funding, authority, and relevance depend on the risk continuing to require management. The more complex the approval process, the more necessary the institution becomes. The longer the delay, the more resources flow toward oversight rather than deployment. The institution does not conspire to perpetuate risk—it does not need to. Its survival structure does the work automatically.

与此同时，交出责任的个体丧失了判断能力。“这套系统安全吗？”变成了“监管机构批准它了吗？”——这是截然不同的两个问题，后者用机构的裁定取代了直接的评估。因为委托让亲自评估变得多余，个体评估风险的能力便随之萎缩。这加深了对机构的依赖，继而抬高了机构的必要性，助长了机构的保守倾向，进一步拉长了延误。

Meanwhile, the individual who delegated the responsibility loses capacity. "Is this system safe?" becomes "has the regulator approved it?"—a different question altogether, one that substitutes institutional judgment for direct assessment. The individual's ability to evaluate risk atrophies because the delegation made it unnecessary. This increases dependence on the institution, which increases the institution's necessity, which increases its conservatism, which increases the delay.

而个体自身的驾驶行为——那94%撞车事故的实际源头——却从未进入这条回路。这层风险从未被委托出去，因为没有人会把自己的日常驾驶当成一项需要交由他人管理的风险。它游离在问责结构之外，正因为没有任何机构承接它，它才得以保持隐形。

And the individual's own driving—the actual source of 94% of crashes—never enters this loop. That risk was never delegated because no one thinks of their own driving as a risk to be managed by someone else. It sits outside the accountability structure, invisible precisely because no institution holds it.

回路就此闭合：委托风险这一动作，亲手造就了维系风险的条件。机构需要风险来证明自身存在的合理性；个体的弃权则抽走了原本能够消减风险的直接介入。初衷在于减少伤害的委托，反倒成了让伤害长存的机制。

The loop closes: the act of delegating risk generates the conditions that sustain it. The institution requires the risk to justify its existence. The individual's abdication removes the direct engagement that would diminish the risk. The delegation, undertaken to reduce harm, becomes the mechanism that perpetuates it.

## 三、 跨法域的证据 / 3. The Evidence Across Jurisdictions

这一结构在自动驾驶的全球格局中清晰可见。欧洲在部署进度上落后北美数年——不是因为技术能力不足，而是因为碎片化的监管框架让委托层级成倍增加。每个司法管辖区都设立各自的审批关卡，每一道关卡都围绕自身的问责风险做最优化，汇总起来的延误便在国境线之间层层叠加。这种延误所招致的伤亡在道路上持续累积，四散分布，且归咎不到任何人头上。

This structure is visible across the autonomous driving landscape. Europe is years behind North America on deployment—not because the technology is less capable, but because fragmented regulatory frameworks multiply the delegation layers. Each jurisdiction creates its own institutional gate, each gate optimizes for its own accountability, and the aggregate delay compounds across borders. The casualties of that delay accumulate on the road, distributed and attributed to no one.

每一场涉及FSD的碰撞都会触发制度性反应：立案调查、专项质询、潜在的限制措施。机构必须做出反应——当可归咎的故障发生时，它的合法性取决于能否采取看得见的行动。而同一时期发生的数千起人为失误车祸，却不会引发对等的反应。这种非对称并非出于偏见，而是源于结构。机构只能看见其问责结构所能识别的事物，因为它的成文规则手册只是过往切分的外化记录，而非身处驾驶前沿的活态观察者：正如[总在倾听者无法发起](../what-always-listens-cannot-originate/)与[你的代码库即是记忆](../your-codebase-is-memory/)所揭示的，无论是静态的监管核查表还是神经网络权重库，都无法发起当下的区分，也无法承担审批关卡所强加的延误后果。

Every FSD-involved crash triggers institutional response: investigations, probes, potential restrictions. The institution must respond—its legitimacy depends on visible action when attributable failure occurs. No equivalent response exists for the thousands of human-error crashes that occur in the same period. The asymmetry is not bias; it is structural. The institution can only see what its accountability structure makes legible, because its codified rulebook is an externalized record of past cuts rather than a living observer at the steering edge: as [What Always Listens Cannot Originate](../what-always-listens-cannot-originate/) and [Your Codebase Is Memory](../your-codebase-is-memory/) show, neither a static regulatory checklist nor a repository of neural weights can originate a present distinction or bear the consequence of the delay the gate enforces.

特斯拉的数据尽管存在种种局限，却代表着制度框架难以消化的一类事实：在车队规模上对相对风险展开的直接测量。机构手中的工具是个案审查、标准合规与审批关卡——没有一样是为了权衡基线伤害的总体替代量而设计的。这组数据回答的，是一个机构在结构上就无法提出的问题。正如[数字火箭、同行审查与因果闭环的稀释](../the-dilution-of-the-causal-loop-and-the-misallocation-of-agency/)所追溯的，同行审查与安全体制正是通过稀释因果回路来制造风险的。

Tesla's data, for all its limitations, represents something the institutional framework cannot easily process: a direct, fleet-scale measurement of comparative risk. The institution's tools are incident review, standards compliance, and approval gates—none of which are designed to weigh aggregate displacement of baseline harm. The data speaks to a question the institution is not structured to ask. Peer review and safety regimes create risk by diluting the loop, as [Digital Rockets, Peer Review, and the Dilution of the Causal Loop](../the-dilution-of-the-causal-loop-and-the-misallocation-of-agency/) traces.

## 四、 机制揭示了什么 / 4. What the Mechanism Reveals

常规叙事将机构定位为挡在危险技术与脆弱公众之间的保护屏障。但在这一叙事之下运转的结构却截然不同：机构的存续需要风险持续存在，个体的委托抽走了直接消减风险的能力，而由此产生的延误，恰恰制造了双方原本试图避免的伤害。

The conventional framing positions institutions as the safeguard between dangerous technology and a vulnerable public. The structure operating beneath that framing is different: the institution's survival requires ongoing risk, the individual's delegation removes direct risk-reduction capacity, and the resulting delay produces the very harm both parties sought to avoid.

这并非针对监管本身的反对意见，而是一项结构性观察：把风险委托给集中的问责结构，会将一个分散且递减的问题转化为一个集中且自我维系的问题。在分散模式下——数百万个体自行选择接触一套持续改进的系统——问题会随着每多开一英里所带来的系统精进而不断缩小。而在集中模式下——审批关卡以零可归咎故障为优化目标——问题没有任何缩小的机制，因为现状的代价从未被归咎于任何人。[限制是选择性的税](../restriction-is-a-selective-tax/)只是同一收紧机制在能力差距外衣下的重演：禁令向接受封印的人征税，且主要向执行封印的人征税，而前沿依然按照那些不把封印当成根基之人的步伐向前推进。禁令同样是委托出去的风险；[起作用的是信念](../what-works-is-the-belief/)表明，它稳固的只是信念，而封不住任何事物。

This is not an argument against regulation as such. It is a structural observation: delegating risk to concentrated accountability structures converts a distributed, diminishing problem into a concentrated, self-sustaining one. The distributed version—millions of individuals choosing exposure to an improving system—shrinks as the system improves with each mile driven. The concentrated version—institutional gates that optimize for zero attributable failure—has no mechanism to shrink, because the cost of the status quo is never attributed. [Restriction Is a Selective Tax](../restriction-is-a-selective-tax/) is the same densification under capacity-gap costume: the hold taxes those who accept the seal, and mostly those who enforce it, while the frontier continues at the pace of those who do not treat the seal as ground. A ban is delegated risk too; [What Works Is the Belief](../what-works-is-the-belief/) shows it stabilizes belief rather than sealing anything.

你委托的风险就是你创造的风险——这不是悖论，而是机制。每年四万人的死亡之所以持续至今，不是因为缺乏更好的系统，而是因为用来汇总管理风险的制度结构本身，正是消减风险的首要障碍。[气候问题只作为感知被登记](../the-climate-problem-registers-only-as-perception/)也是披着行星外衣的同一套装置：各个解决方案层级的经费与必要性，都依赖一套封闭指标体系上的残差，而开放的多因素场域永远不会让这套指标迎来终结。正如[“物理学才是定律”的障眼法](../the-sleight-of-hand-in-physics-is-the-law-and-the-friction-of-reality/)所展示的，把规则当成物理定律掩盖了委托的动作；而如何面对这一机制，始终取决于你自己。

The risk you delegate is the risk you create—not as paradox, but as mechanism. The 40,000 annual deaths persist not because a better system is lacking, but because the institutional structure built to manage risk in aggregate is itself the primary obstacle to reducing it. [The Climate Problem Registers Only as Perception](../the-climate-problem-registers-only-as-perception/) is the same apparatus under planetary costume: solution layers whose funding and necessity require residual on a closed suite that an open multi-factor field will not finish. Treating a rule as physical law disguises the delegation, as [The Sleight of Hand in "Physics Is the Law"](../the-sleight-of-hand-in-physics-is-the-law-and-the-friction-of-reality/) shows; how you meet the mechanism stays yours.
