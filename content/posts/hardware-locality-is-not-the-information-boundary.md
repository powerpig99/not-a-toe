# 硬件的本地性不是信息的边界 / Hardware Locality Is Not the Information Boundary

*能动性与隐私跟随的是管辖共享内容的界限，而不是与一套可检视的操作系统同处一机。 / Agency and privacy track the bound that governs what is shared, not co-location with an inspectable operating system.*

智能体时代反复出现一种主张：本地执行与开放操作系统不可或缺，尤其是那些整套代码能进入模型预训练的系统，理由是智能体需要深入、贴身地进入它所栖身的系统。可是智能体的工作流已经大多经由稳定的抽象运行，底层的用户空间随之退到后面；把计算紧紧绑在某一台机器上，多半是可以改变的设计选择，并非技术上的必然。与之并行的数据本地化偏好，常以隐私或训练价值为理由，而隐私是信息边界的属性，个人化的残余对通用模型的能力也几乎没有贡献。要紧的是这条边界是否被规定清楚、被可靠地维持，而不是进程恰好在哪台机器上运行。

A recurring claim in the agentic era holds that local execution and open operating systems are essential, especially those whose full codebases can enter model pretraining, on the grounds that agents need deep, intimate access to the systems they inhabit. Agentic workflows, though, already run largely through stable abstractions that let the underlying userspace recede, and keeping computation tightly coupled to one machine is mostly a design choice that can be changed, not a technical necessity. The parallel preference for local data is often argued from privacy or from training value, yet privacy is a property of the information boundary, and individualized residue adds almost nothing to general model capability. What matters is whether that boundary is clearly specified and reliably maintained, not which machine happens to run the process.

## 一、 能动性早已经由抽象运行 / 1. Agency Already Runs Through Abstractions

智能体的工作流大体上已经与操作系统无关。多数生产系统经由 API、容器化运行时、浏览器环境和可移植的语言平台运作。一旦智能体通过稳定的接口取用工具与资源，内核与用户空间的分量就退了下去。能力取决于这些抽象的质量，以及围绕上下文设置的控制是否可靠，而不取决于与某一套操作系统同处一处。

Agentic workflows are already largely independent of the operating system. Most production systems work through APIs, containerized runtimes, browser environments and portable language platforms. Once an agent reaches tools and resources through stable interfaces, the kernel and userspace recede in weight. Capability depends on the quality of those abstractions and on the reliability of the controls placed around context, not on co-location with a particular operating system.

主张整套开源代码必须进入预训练，等于把对技术栈的贴身了解固定为能动性的所在。对某一个用户空间了如指掌，在某些负载下确有用处，但有用并不等于能动性的条件。[剩余控制退向边缘](../residual-control-recedes-to-the-edge/)追溯的是同一次挪移，场景换成谁拥有外壳：一旦判据、界限与验证承担起要紧的结果，对底层基质的控制就成了剩余。[我们遗忘的脚手架](../the-scaffolding-we-forget-local-models-as-default/)追溯的是另一面的固化：一个好用的本地安排被当成了情境本身所指示的默认。这里被固化的，是与开放内核同处一处，被当作智能体能力的结构本身。

The claim that full open-source codebases must enter pretraining fixes intimate knowledge of the stack as the seat of agency. Knowing one userspace inside out is useful under some loads, but being useful is not the same as being the condition of agency. [Residual Control Recedes to the Edge](../residual-control-recedes-to-the-edge/) traces the same relocation in the case of who owns the shell: once criteria, bounds and verification carry the outcomes that matter, control of the low-level substrate becomes residual. [The Scaffolding We Forget](../the-scaffolding-we-forget-local-models-as-default/) traces the companion freeze, where a workable local arrangement comes to register as the default the situation itself indicates. Here what freezes is co-location with an open kernel, held as the very structure of agentic capacity.

## 二、 紧密的本地耦合是可改的设计 / 2. Tight Local Coupling Is a Changeable Design

坚持深度的本地能动性，多半出自设计，而非技术上的必需。计算被紧紧绑在某一台机器上，于是对某一套操作系统的贴身了解看上去仍不可替代。这种绑定是可以改的：更高层的接口、远程或可证明的执行，以及把智能体的控制平面与任何具体宿主分开，都能把它松开。

The insistence on deep local agency comes mostly from design rather than technical necessity. Computation is bound tightly to one machine, so intimate knowledge of one operating system keeps looking indispensable. That binding can be changed: higher-level interfaces, remote or attested execution, and a clean separation between the agent's control plane and any particular host all loosen it.

自我区分的活动在发生，无因，不息。称它为心智：那个已经在进行中的观察者，它的每一个动作都是一次区分。工具与宿主是外化的痕迹，延长了心智的触及，却并不把边缘迁入基质。[因果停留在掌舵的边缘](../causality-stays-at-the-edge-that-steers/)把框定、选择与验证留在掌舵者一侧，工具只是在指引下重组残余。把发起动作的位置分给本地的开放技术栈，是把媒介当成了所在：可检视的代码越来越密，看上去就像媒介成了能动性的座位，其实那只是一次带宽更高的握持，握持之上仍是那个选定界限的边缘。

Self-distinguishing activity occurs, uncaused, unceasing. Call it the Mind: the observer already underway, every act of which is a distinction. Tools and hosts are externalized traces that extend its reach; they do not move the edge into the substrate. [Causality Stays at the Edge That Steers](../causality-stays-at-the-edge-that-steers/) keeps framing, selection and verification with the one who steers, while the instrument recombines residue under direction. Assigning initiation to the local open stack takes the medium for the locus: as inspectable code densifies, the medium seems to become the seat of agency, when it is a higher-bandwidth hold under the edge that still chooses the bounds.

## 三、 个人化的残余对通用模型是噪声 / 3. Individualized Residue Is Noise for General Models

偏好本地的另一条理由，是保护那些可能改进模型的数据。最能改进通用模型的，是可以泛化的信息，也就是能跨越用户与领域迁移的模式。真正个人化的信息，一个人的文件、习惯与上下文留下的私人残余，对模型能力几乎没有贡献，就训练而言它是噪声。因此，执意把这类数据留在本地，无法以它对机器学习的价值为根据。

A related justification for local preference is protecting data that might improve models. The data that most improves general models is generalizable information, patterns that transfer across users and domains. Truly individualized information, the private residue of one person's files, habits and context, adds almost nothing to model capability; for training purposes it is noise. The insistence on keeping such data local therefore cannot rest on its value for machine learning.

[数据是局部的，智能是分配的](../data-is-local-intelligence-is-allocated/)描述的正是这种几何，场景换成数据质量：每一个信号先是对产生它的那个中心价值最高，到了几乎其他所有地方都是噪声。聚合使剩余结构变密，却不会因为把私人残余搬进训练库存，就把它提升为通用能力。把个人化材料留在本地保管，仍可以是一条好用的界限，只是这条界限无法由一个材料本身撑不起的训练价值故事来担保。

[Data Is Local; Intelligence Is Allocated](../data-is-local-intelligence-is-allocated/) describes exactly this geometry, in the case of data quality: every signal is of highest value first to the center that produced it and noise almost everywhere else. Aggregation densifies residual structure; it does not turn private residue into general capability by moving it into the training stock. Keeping individualized material in local custody can remain a workable bound, but the bound cannot be warranted by a training-value story the material does not support.

## 四、 隐私是边界，不是技术栈 / 4. Privacy Is the Boundary, Not the Stack

隐私常被当作同一种本地偏好更易被接受的说法。在这个说法里，独占控制的愿望可以不被说出而一并通行。然而隐私并不是硬件位置的属性，也不是任何一套软件栈的属性。它是那条边界的属性：这条边界规定什么信息被共享、与谁共享、在什么条件下共享、附带什么保证。硬件与软件是可能执行、也可能未能执行这条边界的机制，它们并不构成边界本身。

Privacy is often offered as the more acceptable framing for the same local preference, and under that framing a wish for exclusive control can pass along without being named. Privacy, however, is not a property of hardware location or of any particular software stack. It is a property of the boundary that governs what information is shared, with whom, under what conditions and with what assurances. Hardware and software are mechanisms that may enforce that boundary or fail to; they do not constitute it.

[要求他人开放是对自我封闭的渴望](../advocating-openness-of-others-is-a-desire-for-closure-of-the-self/)是用道德语言说出来的隐私：这个词让向内的封闭显得可取，却没有为这段关系本身增添任何信息。去掉这层道德语言，剩下的是在一条界限下有选择地释放痕迹，这条界限让所在保持可区分。[主权、信念与规制结构的生成](../sovereignty-belief-and-regulatory-structures/)是用制度语言说出来的同一条界限：抉择的所在始终留在原处，而“这条界限可以交出去”的信念却越积越密。本地硬件可以实现一条被选定的边界，但硬件在本地，并不是隐私所指的那个属性。

[Advocating Openness of Others Is a Desire for Closure of the Self](../advocating-openness-of-others-is-a-desire-for-closure-of-the-self/) is privacy said in moral language: the word makes the inward close seem desirable without adding any information about the relation itself. With the moral language removed, what remains is the selective release of traces under a bound that keeps the locus distinct. [Sovereignty, Belief, and the Generation of Regulatory Structures](../sovereignty-belief-and-regulatory-structures/) is the same bound said in institutional language: the locus of choosing stays where it is, while the belief that the bound can be handed over densifies. Local hardware can implement a chosen boundary, but the hardware being local is not the property privacy names.

## 五、 不存在绝对的本地性 / 5. There Is No Absolute Locality

再者，绝对的本地性并不存在。每一个系统都早已卷入供应链、固件、网络与外部服务。绝对的隔离是一个修辞上的理想，不是一个稳定的技术状态。能做到的只是隔离与信任的程度。于是对智能体系统而言，相关的问题不是计算是否发生在本地设备上，而是信息边界是否被界定清楚、被可靠地维持。

There is, moreover, no absolute locality. Every system is already entangled in supply chains, firmware, networks and external services. Absolute isolation is a rhetorical ideal, not a stable technical state; what can be had are degrees of isolation and trust. The relevant question for agentic systems is therefore not whether computation happens on a local device, but whether the information boundary is clearly defined and reliably maintained.

[没有系统能被保持封闭](../no-system-can-be-kept-closed/)是在形式层面说出的同一个剩余：一次有限的握持封不住使用它的那个活动。[开放即一致](../openness-is-consistency/)从另一侧提出同样的要求：强迫一个有限结构去为只会继续的东西奠基，表面上的矛盾就会成倍出现。绝对的本地隔离，是把一种偏好的隔离程度固化为穷尽一切的根据。隔离的程度作为工程手段依然可用，但穷尽性并不随任何一种程度而来。

[No System Can Be Kept Closed](../no-system-can-be-kept-closed/) states the same remainder at the formal level: a finite hold cannot seal the activity that uses it. [Openness Is Consistency](../openness-is-consistency/) makes the same demand from the other side: force a finite structure to ground what only continues, and surface contradictions multiply. Absolute local isolation fixes one preferred degree of isolation as an exhaustive ground. Degrees of isolation stay usable as engineering, but exhaustiveness does not come with any one degree.

## 六、 能力跟随边界，而不是机器 / 6. Capability Tracks the Boundary, Not the Machine

对隐私而言，要紧的是信息边界是否清晰、是否完整，硬件的本地性不在这个属性之内。一旦边界被规定并得到执行，处理发生的物理或架构位置就不再决定隐私的结果。同样的道理也延伸到能动性：能力取决于抽象的质量和围绕上下文设置的控制是否可靠，而不取决于与某一套操作系统同处一处。

For privacy, what matters is the clarity and integrity of the information boundary; the locality of the hardware is not part of that property. Once the boundary is specified and enforced, the physical or architectural site of processing no longer decides the privacy outcome. The same holds for agency more broadly: capability depends on the quality of the abstractions and on the reliability of the controls placed around context, not on co-location with a particular operating system.

本地的开放系统依然是好用的工具；在某些训练目标下，整套代码进入预训练也依然可以是有用的残余。成本、延迟、离线运行与偏好的信任模式，都是各个中心会继续在其上划定界限的维度。这一刀并不是说这些安排是空的，而是说它们的必然性并不来自能动性或隐私的要求。在智能体系统里，起作用的是它所遵守的信息边界有多精确、它能运用的知识有多通用，而不是它恰好在哪台机器上运行。

Local open systems remain workable instruments, and under some training objectives full codebases in pretraining can remain useful residue. Cost, latency, offline operation and preferred trust models are axes on which centers will keep drawing bounds. The cut is not that those arrangements are empty; it is that their necessity does not come from the requirements of agency or of privacy. What tells in an agentic system is the precision of the information boundaries it respects and the generality of the knowledge it can apply, not the machine it happens to run on.
