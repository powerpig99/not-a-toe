# 硬件的本地性不是信息的边界 / Hardware Locality Is Not the Information Boundary

*隐私跟随管辖共享的边界，能动性留在掌舵的边缘，二者都不随硬件同处一机而来。 / Privacy tracks the bound governing what is shared, agency stays at the edge that steers; neither comes with co-location.*

智能体时代反复出现一种主张：智能体需要在开放操作系统上本地执行，而且这套系统的整套代码必须进入模型预训练，理由是智能体需要深入、贴身地进入它所栖身的系统。可是智能体的工作流已经大多经由稳定的抽象运行，底层的内核与用户空间随之退到后面；把计算紧紧绑在某一台机器上，多半是可以改变的设计选择，并非技术上的必然。与之并行的数据本地化偏好，常以隐私或训练价值为理由，而隐私是信息边界的属性，个人化的残余在通用模型的预训练中也几乎没有贡献。要紧的是这条边界是否界定清楚、执行可靠，而不是进程恰好在哪台机器上运行。

A recurring claim in the agentic era holds that agents need local execution on an open operating system, and that its full codebase must enter model pretraining, on the grounds that agents need deep, intimate access to the systems they inhabit. Agentic workflows, though, already run largely through stable abstractions that let the underlying kernel and userspace recede, and keeping computation tightly coupled to one machine is mostly a design choice that can be changed, not a technical necessity. The parallel preference for local data is often argued from privacy or from training value, yet privacy is a property of the information boundary, and individualized residue adds almost nothing to the pretraining of general models. What matters is whether that boundary is clearly defined and reliably enforced, not which machine happens to run the process.

## 一、 能动性早已经由抽象运行 / 1. Agency Already Runs Through Abstractions

智能体的工作流大体上已经不依赖于某一套操作系统。多数生产系统经由 API、容器化运行时、浏览器环境和可移植的语言平台运作。一旦智能体通过稳定的接口取用工具与资源，内核与用户空间的分量就退了下去。能力取决于这些抽象的质量，以及围绕上下文设置的验证与控制是否可靠，而不取决于与某一套操作系统同处一处。

Agentic workflows already largely do not depend on any one operating system. Most production systems work through APIs, containerized runtimes, browser environments and portable language platforms. Once an agent uses tools and resources through stable interfaces, the kernel and userspace recede in weight. Capability depends on the quality of those abstractions and on the reliability of the verification and controls placed around context, not on co-location with a particular operating system.

主张整套开源代码必须进入预训练，是把对技术栈的贴身了解固定为能动性的条件。对某一个用户空间了如指掌，在某些负载下确有用处，但有用并不等于能动性的条件。[要紧的控制迁往边缘](../residual-control-recedes-to-the-edge/)追溯的是同一次挪移，并指明了它的去向：要紧的控制移到边缘，落在成败判据、风险界限与验证上，对底层基质的占有则成了剩余。[我们遗忘的脚手架](../the-scaffolding-we-forget-local-models-as-default/)追溯的是相伴的一种固化：彼处，一个好用的本地模型被当成了情境本身所指示的默认入口；此处被固化的，是与开放内核同处一处，被当作能动性的条件。

The claim that full open-source codebases must enter pretraining fixes intimate knowledge of the stack as the condition of agency. Knowing one userspace inside out is useful under some loads, but being useful is not the same as being the condition of agency. [Essential Control Moves to the Edge](../residual-control-recedes-to-the-edge/) traces the same relocation and names where it goes: the control that matters moves to the edge, into success criteria, risk bounds and verification, while ownership of the low-level substrate becomes residual. [The Scaffolding We Forget](../the-scaffolding-we-forget-local-models-as-default/) traces a companion freeze: there, a workable local model comes to register as the default entry the situation itself indicates; here, what freezes is co-location with an open kernel, held as the condition of agency.

## 二、 紧密的本地耦合是可改的设计 / 2. Tight Local Coupling Is a Changeable Design

坚持深度的本地介入，多半出自设计，而非技术上的必需。计算被紧紧绑在某一台机器上，于是对某一套操作系统的贴身了解看上去仍不可替代。这种绑定是可以改的：更高层的接口、远程执行或可远程证明的执行，以及把智能体的控制平面与具体宿主分开，都能把它松开。

The insistence on deep local access comes mostly from design rather than technical necessity. Computation is bound tightly to one machine, so intimate knowledge of one operating system keeps looking indispensable. That binding can be changed: higher-level interfaces, remote or attested execution, and a separation between the agent's control plane and any particular host all loosen it.

自我区分的活动在发生，无因，不息。称它为心智：那个已经在进行中的观察者，它的每一个动作都是一次区分。工具与宿主是外化的痕迹，延长了心智的触及，却并不把边缘迁入基质；重新设计过的接口与执行环境也一样，它们松开的是绑定，并不成为新的所在。[因果停留在掌舵的边缘](../causality-stays-at-the-edge-that-steers/)把框定、选择与验证留在掌舵者一侧，工具只是在指引下重组残余。把发起动作的位置分给本地的开放技术栈，是把媒介当成了所在：可检视的代码越来越密，看上去就像媒介成了能动性的座位，其实那只是一次带宽更高的握持，握持之上仍是那个选定界限的边缘。

Self-distinguishing activity occurs, uncaused, unceasing. Call it the Mind: the observer already underway, every act of which is a distinction. Tools and hosts are externalized traces that extend its reach; they do not move the edge into the substrate, and neither do redesigned interfaces and execution environments, which loosen a binding without becoming a new seat. [Causality Stays at the Edge That Steers](../causality-stays-at-the-edge-that-steers/) keeps framing, selection and verification with the one who steers, while the instrument recombines residue under direction. Assigning initiation to the local open stack takes the medium for the locus: as inspectable code densifies, the medium seems to become the seat of agency, when it is a higher-bandwidth hold under the edge that still chooses the bounds.

## 三、 个人化的残余在预训练中是噪声 / 3. Individualized Residue Is Noise in Pretraining

偏好本地的另一条理由，是保护那些可能改进模型的数据。在通用模型的预训练中起作用的，是可以泛化的信息，也就是能跨越用户与领域迁移的模式。一个人的文件、习惯与上下文留下的私人残余，对这样的训练几乎没有贡献，就这个目标而言它是噪声。因此，执意把这类数据留在本地，无法以它对机器学习的价值为根据。

A related justification for local preference is protecting data that might improve models. What counts in the pretraining of general models is generalizable information, patterns that transfer across users and domains. The private residue of one person's files, habits and context adds almost nothing to such training; for that objective it is noise. The insistence on keeping such data local therefore cannot rest on its value for machine learning.

[数据是局部的，智能是分配的](../data-is-local-intelligence-is-allocated/)描述的是这种关系：每一个信号先是对产生它的那个中心价值最高，到了几乎其他所有地方都是噪声；噪声与价值是对某个中心而言的关系，不是材料本身的等级。聚合使剩余结构变密，却不会因为把私人残余搬进训练库存，就把它变成通用能力。把个人化材料留在本地保管，仍可以是一条好用的界限，只是这条界限无法由一个材料本身撑不起的训练价值故事来担保。

[Data Is Local; Intelligence Is Allocated](../data-is-local-intelligence-is-allocated/) describes this relation: every signal is of highest value first to the center that produced it and noise almost everywhere else; noise and value are relations to a center, not grades of the material. Aggregation densifies residual structure; it does not turn private residue into general capability by moving it into the training stock. Keeping individualized material in local custody can remain a workable bound, but the bound cannot be warranted by a training-value story the material does not support.

## 四、 隐私是边界，不是技术栈 / 4. Privacy Is the Boundary, Not the Stack

隐私常被当作同一种本地偏好的另一种说法。然而隐私并不是硬件位置的属性，也不是任何一套软件栈的属性。它是那条边界的属性：这条边界规定什么信息被共享、与谁共享、在什么条件下共享。硬件与软件，连同它们提供的各种保证，是可能执行、也可能未能执行这条边界的机制，它们并不构成边界本身。

Privacy is often offered as another way of stating the same local preference. Privacy, however, is not a property of hardware location or of any particular software stack. It is a property of the boundary that governs what information is shared, with whom and under what conditions. Hardware and software, together with the assurances they provide, are mechanisms that may enforce that boundary or fail to; they do not constitute it.

[要求他人开放是对自我封闭的渴望](../advocating-openness-of-others-is-a-desire-for-closure-of-the-self/)把“隐私”一词看作向内封闭的道德语言：这个词让封闭显得可取，却没有为这段关系本身增添任何信息。去掉这层道德语言，剩下的是在一条界限下有选择地释放痕迹，这条界限让所在保持可区分；本文所说的隐私，指的就是这条界限，而不是那层语言。[主权、信念与规制结构的生成](../sovereignty-belief-and-regulatory-structures/)追溯的是抉择的所在：具体的抉择可以托付出去，抉择的所在却始终留在原处，而“这个所在本身可以交出去”的信念越积越密。把共享规则托付给某种机制，正是那种可以托付的抉择。本地硬件可以实现一条被选定的边界，但硬件在本地，并不是隐私所指的那个属性。

[Advocating Openness of Others Is a Desire for Closure of the Self](../advocating-openness-of-others-is-a-desire-for-closure-of-the-self/) reads the word "privacy" as the moral language of an inward close: the word makes the close seem desirable without adding any information about the relation itself. With the moral language removed, what remains is the selective release of traces under a bound that keeps the locus distinct; privacy here names that bound, not the language. [Sovereignty, Belief, and the Generation of Regulatory Structures](../sovereignty-belief-and-regulatory-structures/) traces the locus of choosing: particular choices can be entrusted, while the locus of choosing stays where it is, and the belief that the locus itself can be handed over densifies. Entrusting sharing rules to a mechanism is one of those choices that can be entrusted. Local hardware can implement a chosen boundary, but the hardware being local is not the property privacy names.

## 五、 不存在孤立自足的本地系统 / 5. There Is No Self-Contained Local System

本地并不等于隔离。计算可以在本地发生，系统却早已卷入供应链、固件、网络与外部服务。一个孤立自足的本地系统，是一个修辞上的理想，不是一个稳定的技术状态；能做到的只是隔离与信任的程度，离线运行便是其中一种。于是对智能体系统而言，计算是否发生在本地设备上，本身并不回答隐私的问题；要回答它，得看信息边界是否界定清楚、执行可靠。

Locality is not isolation. Computation can happen locally while the system is already entangled in supply chains, firmware, networks and external services. A self-contained local system is a rhetorical ideal, not a stable technical state; what can be had are degrees of isolation and trust, offline operation among them. For agentic systems, then, whether computation happens on a local device does not by itself answer the question of privacy; that turns on whether the information boundary is clearly defined and reliably enforced.

供应链只是经验上的限度，[没有系统能被保持封闭](../no-system-can-be-kept-closed/)说的是形式上的剩余：一次有限的握持封不住使用它的那个活动，即使把每一条外部依赖都收进本地，这一点也不变。[开放即一致](../openness-is-consistency/)是从另一侧给同一个要求命名：要求一个有限结构为只会继续的东西奠基，表面上的矛盾就会成倍出现。孤立自足的本地系统，是把一种偏好的隔离程度固化为穷尽一切的根据。隔离的程度作为工程手段依然可用，但穷尽性并不随任何一种程度而来。

Supply chains are only an empirical limit; [No System Can Be Kept Closed](../no-system-can-be-kept-closed/) states the formal remainder: a finite hold cannot seal the activity that uses it, and that stays so even if every external dependency were brought inside the local machine. [Openness Is Consistency](../openness-is-consistency/) names the same demand from the other side: require a finite structure to ground what only continues, and surface contradictions multiply. The self-contained local system fixes one preferred degree of isolation as an exhaustive ground. Degrees of isolation stay usable as engineering, but exhaustiveness does not come with any one degree.

## 六、 边界与边缘，而不是机器 / 6. The Boundary and the Edge, Not the Machine

对隐私而言，要紧的是信息边界是否界定清楚、执行可靠，硬件的本地性不在这个属性之内。一旦边界被界定并得到执行，处理发生的物理或架构位置就不再决定隐私的结果。能动性是另一回事：智能体能做成什么，取决于抽象的质量和围绕上下文设置的验证与控制；发起动作、选定界限、评判结果，则始终留在掌舵的边缘，并不因为同处一机而迁入操作系统。

For privacy, what matters is whether the information boundary is clearly defined and reliably enforced; the locality of the hardware is not part of that property. Once the boundary is defined and enforced, the physical or architectural site of processing no longer decides the privacy outcome. Agency is a different relation: what an agent can accomplish depends on the quality of the abstractions and on the verification and controls placed around context, while initiating, choosing the bounds and judging the outcome stay at the edge that steers, and do not move into an operating system through co-location.

本地的开放系统依然是好用的工具；在某些训练目标下，整套代码进入预训练也依然可以是有用的残余。这里的残余与第三节的私人残余是同一个词：都是痕迹，区别只在对某个目标是否有用。成本、延迟、离线运行与偏好的信任模式，都是各个中心会继续在其上划定界限的维度；隐私不在其中，因为它不是这些权衡里的一项，而是边界本身。这一刀并不是说这些安排是空的，而是说它们的必然性并不来自能动性或隐私的要求。在智能体系统里，可以衡量的是它所遵守的信息边界有多精确、它能运用的残余有多通用；这些都是掌舵的边缘手里的工具，而不是能动性的所在，更不是它恰好在哪台机器上运行。

Local open systems remain workable instruments, and under some training objectives full codebases in pretraining can remain useful residue. Residue here is the same word as the private residue of section 3: both are traces, and what differs is only whether they are of use to a given objective. Cost, latency, offline operation and preferred trust models are axes on which centers will keep drawing bounds; privacy is not among them, because it is not one more term in those tradeoffs but the boundary itself. The cut is not that those arrangements are empty; it is that their necessity does not come from the requirements of agency or of privacy. What can be measured in an agentic system is the precision of the information boundaries it respects and the generality of the residue it can apply; these are instruments in the hands of the edge that steers, not the seat of agency, and still less the machine it happens to run on.
