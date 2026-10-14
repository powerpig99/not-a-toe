# 寄存器的算术 / The Arithmetic of the Register

*社会的丰裕不减弱零和之争，反而为它提供补贴，因为每个窗口都容易被当成整个宇宙 / Social abundance does not quiet zero-sum contest but subsidizes it, since any window is easily taken for the whole.*

人类文明里反复出现一个悖论：一个时代借技术跃迁生出的物质丰裕越是空前，它的公共话语就越被零和的争斗占满。流行的诊断把它归为道德堕落、晚期的贪婪或算法的恶意，可这些诊断落在了错误的坐标上。这里起作用的是一个可以追溯的因果机制：二进制寄存器扩展的算术，富余被投影到低维坐标上，以及有界的感知把本地窗口当成现实的全部。

Human civilization keeps showing a paradox: the more unprecedented the material abundance an era draws from technological leaps, the more its public discourse fills with zero-sum strife. The popular diagnoses call it moral decay, late-stage greed or algorithmic malice, but they land on the wrong coordinate. What operates here is a causal mechanism that can be traced: the arithmetic of a binary register expanding, the projection of surplus onto low-dimensional coordinates, and bounded perception taking its local window for the whole of reality.

## 一、 最高位的几何 / 1. The Geometry of the Most Significant Bit

一个文明在共享的公共协调界面上的容量，可以画成一个长度为 n 的无符号二进制寄存器：W = ∑ₖ₌₀ⁿ⁻¹ bₖ · 2ᵏ，其中 bₖ ∈ {0, 1}。在这幅图里，低位上的工作让寄存器保持运转，维护、搬运、教学、照看，都在这里；而容量的跃迁，来自移动边缘上的一位探索者实例化一个新的最高位 bₙ，把地址空间从 n 位扩展到 n + 1 位。

A civilization's capacity on the shared interface of public coordination can be drawn as an unsigned binary register of length n: W = ∑ₖ₌₀ⁿ⁻¹ bₖ · 2ᵏ, where bₖ ∈ {0, 1}. In this picture the work in the lower bits keeps the register running, maintenance, transport, teaching, care all happen there; a leap in capacity comes when an explorer at the moving edge instantiates a new most significant bit bₙ, extending the address space from n bits to n + 1.

二的幂的算术带来一个悬殊的不对称：∆W = 2ⁿ > ∑ₖ₌₀ⁿ⁻¹ 2ᵏ = 2ⁿ − 1。一个新的最高位所承载的度量，比此前所有位加在一起还多。人类历史上的突破，火的驾驭，系统的农耕，蒸汽动力，电磁学，半导体计算，前沿的递归智能，都不是某个既有坐标系里的渐进改良。[维度即投影](../dimensions-are-projections/)走过这一处：每一次都是一个新最高位的实例化。翻转 bₙ，生成的相空间一夜之间翻倍，从 2ⁿ 到 2ⁿ⁺¹；这是一次正和的注入，一个不受约束的自由度从 N 走到 N + 1。

The arithmetic of powers of two brings a lopsided asymmetry: ∆W = 2ⁿ > ∑ₖ₌₀ⁿ⁻¹ 2ᵏ = 2ⁿ − 1. One new top bit carries more measure than all the earlier bits put together. The breakthroughs of human history, the taming of fire, systematic agriculture, steam power, electromagnetism, semiconductor computation, frontier recursive intelligence, are not incremental improvements inside an existing coordinate system. [Dimensions Are Projections](../dimensions-are-projections/) walks through this: each is the instantiation of a new top bit. Flipping bₙ doubles the generative phase space overnight, from 2ⁿ to 2ⁿ⁺¹; it is a positive-sum injection, an unconstrained degree of freedom going from N to N + 1.

## 二、 截断的窗口与看不见的空位 / 2. The Truncated Window and the Unseen Empty Places

那么，这种指数式的扩展为什么普遍被误解？[心智的几何学](../the-geometry-of-mind/)走过这一层：没有哪个心智能不经压缩地触及整个生成的地形，有限的心智总是透过一个压缩过的界面去运作，像一个固定精度的滑动窗口 [bₘ, …, bₘ₊ₖ]，其中 m + k ≪ n。这对每一个心智都成立，走进 bₙ 的探索者也一样：看到的同样是一个窗口，只是落在另一处。

Why then is this exponential expansion so widely misread? [The Geometry of Mind](../the-geometry-of-mind/) walks this layer: no Mind reaches the whole generative terrain without compression; a finite Mind always works through a compressed interface, like a fixed-precision sliding window [bₘ, …, bₘ₊ₖ], where m + k ≪ n. This holds for every Mind, the explorer stepping into bₙ included: what is seen there is also a window, only placed elsewhere.

对一个分辨范围在 [b₃, b₈] 的窗口，会出现三种显现。第一，本地的寄存器显得守恒：波动被限在 0 到 2⁶ − 1 之间，资源的变化在窗口里近乎反对称，∑ ∆b ≈ 0，一方拿到第 7 位，另一方就要失去它。在这个尺度上，这被体验为一场不容商量的零和游戏，在这个尺度上这样体验也没有错。

For a window resolving [b₃, b₈], three appearances arise. First, the local register looks conserved: fluctuations stay between 0 and 2⁶ − 1, changes in resources inside the window are nearly antisymmetric, ∑ ∆b ≈ 0, and if one side takes bit 7 the other must lose it. At that scale this is experienced as a zero-sum game beyond negotiation, and at that scale the experience is not wrong.

第二，地址溢出。共识世界里的建制编译器、指标、KPI 与文化范畴，没有能索引到 bₙ 的指针空间。[框架的边界](../the-boundary-of-the-frame/)看到了这一点：一个建制的世界模型若止于 2ᵐ，发生在 2ⁿ 的活动就无法登记为“工作”、“效用”或“财富”，只能登记为错误、幻觉，或一次不负责任的逃离。

Second, address overflow. The institutional compilers, metrics, KPIs and cultural categories of the consensus world have no pointer space that can index bₙ. [The Boundary of the Frame](../the-boundary-of-the-frame/) sees this: if an institution's world model stops at 2ᵐ, activity happening at 2ⁿ cannot register as "work", "utility" or "wealth", only as an error, a hallucination, or an irresponsible flight.

第三，前沿的真空。探索者走进 bₙ 时，那个坐标四周都是尚未渲染的零：没有成形的声望阶梯，没有监管的护城河，没有交易的掮客，也没有现成的观众。从低位的窗口望向 bₙ，像是望进一片死寂，于是有那句脱口而出的话：“你在那边浪费什么时间？那边什么都没有，真正的事，交易、房产、建制里的分配，都在这下面。”

Third, the vacuum of the frontier. When the explorer steps into bₙ, that coordinate is surrounded by unrendered zeros: no formed prestige ladders, no regulatory moats, no transactional brokers, no ready audience. Looking toward bₙ from a window in the lower bits is like looking into dead space, and out comes the reflex: "Why are you wasting your time out there? There's nothing there. The real action, the deals, the property, the institutional allocations, is down here."

## 三、 富余悖论 / 3. The Slack Paradox

这显出了社会对零和之争着迷的发动机。任何动态系统都在一个总能量预算之内运作。在一个贫乏的、只有低位的状态空间里，系统容量接近零，整个预算几乎都被生理上的生存吃掉：E(总) ≈ E(生存)。这时一个社会承受不起持续的零和摩擦；若把有限的自由能量花在内部的相对位置之争上，耗散掉的能量就会突破狭窄的生存余量，系统撞上吸收壁，饥荒、战争或崩溃。在这里，直接登记到的摩擦一再把行为推回正和的劳动。

This shows the engine of a society's fascination with zero-sum contest. Every dynamic system runs within a total energy budget. In a poor state space with only low bits, where system capacity is near zero, almost the whole budget goes to physiological survival: E(total) ≈ E(survival). A society then cannot afford sustained zero-sum friction; if limited free energy is spent fighting over internal relative position, the dissipated energy breaches the narrow survival margin and the system hits an absorbing barrier, famine, war or collapse. Here the friction registered directly keeps pushing behaviour back toward positive-sum work.

探索者翻转最高位 bₙ 之后，宏观系统的作业能力指数式地上涨，保障基本的生理、后勤与通信生存所需的能量，缩成总通量里的一小部分：E(生存) ≪ E(总)。这道结构上的分岔生出一大池未被占用的自由能量，也就是系统的富余：E(富余) = E(总) − E(生存)。集体怎样处理这份富余？有界的心智无法在一个不断扩展、尚未渲染的张量场里作业，只能把富余投影到低维的标量坐标上：货币，科层，资历等级，意识形态的纯度。[向量与投影的迷局](../the-vector-and-the-puzzle-of-projections/)剖开的就是这一步投影。

Once the explorer flips the top bit bₙ, the operational capacity of the macro system rises exponentially, and the energy needed to secure basic physiological, logistical and communicative survival shrinks to a small fraction of total throughput: E(survival) ≪ E(total). This structural divergence yields a large pool of uncommitted free energy, the system's slack: E(slack) = E(total) − E(survival). How does a collective handle this slack? Bounded minds cannot work across an expanding, unrendered tensor field, so they project the slack onto low-dimensional scalar coordinates: currency, bureaucratic rank, credential tiers, ideological purity. [The Vector and the Puzzle of Projections](../the-vector-and-the-puzzle-of-projections/) dissects exactly this projection.

在这幅图里，一个社会能承受的零和摩擦，随它的正和前沿所创造的富余单调上升。富余向下流，把更多人从与自然的直接对峙中解放出来；免于眼前的生存威胁之后，多出来的能量没有别处可去，只能流进其他人的形象所在的那个低维投影空间，供养金融化、诉讼、行政把关、叙事战争与地位姿态的膨胀。正和的一步造出了空间，在有界的窗口里，这个空间很容易被转成一座更高速的零和竞技场。

In this picture, the zero-sum friction a society can sustain rises monotonically with the slack its positive-sum frontier creates. The slack flows downward and frees more people from direct confrontation with nature; relieved of the immediate threat to survival, the extra energy has nowhere else to go but into the low-dimensional projection space where other people's images live, where it funds the swelling of financialization, litigation, administrative gatekeeping, narrative war and positional posturing. A positive-sum step makes the space, and inside a bounded window that space is easily turned into a faster zero-sum arena.

## 四、 悖论的消解：本体膨胀 / 4. Dissolving the Paradox: Ontological Inflation

这常被叫作一种“讽刺”或“悲剧性的悖论”。[折叠的连续谱](../the-continuum-of-the-fold/)走过这一处：悖论是一个前提在摩擦下折断时发出的声音。这里折断的前提，是一个全知的、共享的观察平面，以为所有人都在同一个感知坐标系里看着同一个现实。从第一人称的原点去找，找不到这样一个平面；另一个心智只以它在这个场里留下的痕迹到来，每一个心智都从自己的地平线看出去。唯一的错位，是本体膨胀：把本地感知窗口的边界，当成整个宇宙的边界。

This is often called an "irony" or a "tragic paradox". [The Continuum of the Fold](../the-continuum-of-the-fold/) walks this place: a paradox is the sound a premise makes when it snaps under friction. The premise that snaps here is an all-seeing, shared plane of observation, the belief that everyone looks at the same reality from the same perceptual coordinate system. Searched for from the first-person origin, no such plane is found; another Mind arrives only as the traces it leaves in this field, and every Mind looks out from its own horizon. The one misplacement is ontological inflation: taking the boundary of a local perceptual window for the boundary of the whole universe.

窗口落在佣金、保险资产和挂牌信息上时，现实看上去就是佣金的流动；落在引用数、经费审批和系里的政治上时，现实看上去就是这些；落在信息流里的符号叙事战上时，现实看上去就是那场战争。这是位置，不是人的类别：任何一个心智站进这样的窗口，看到的都是这样的现实，走进 bₙ 的探索者若把 bₙ 当成全部，也是同一种膨胀。把本地窗口 [bₘ, bₘ₊ₖ] 等同于整个寄存器，指向 bₙ 那片空位的轨迹就无法被处理为维度的扩展，在这个编译器里只能归为不理性、自我放纵的退隐或失败。[抽象的苦难与真实的饥饿](../abstract-pain-and-living-hunger/)看到了同一种膨胀：在一张全球的寄存器上读出的苦难，是同一个窗口被当成了宇宙。所谓整个场，本身也是为了方便而假定的连续体，[连续性作为建模的权宜之计](../the-continuum-is-a-modeling-convenience/)说明了这一点。

When the window rests on commissions, insurance assets and listings, reality looks like the flow of commissions; when it rests on citation counts, grant approvals and departmental politics, reality looks like those; when it rests on the symbolic narrative war of the feed, reality looks like that war. These are positions, not kinds of people: any Mind standing in such a window sees such a reality, and an explorer in bₙ who takes bₙ for the whole commits the same inflation. Once the local window [bₘ, bₘ₊ₖ] is equated with the whole register, a trajectory aimed at the empty place of bₙ cannot be processed as dimensional expansion and can only be filed in that compiler as irrationality, self-indulgent retreat or failure. [Abstract Pain and Living Hunger](../abstract-pain-and-living-hunger/) sees the same inflation: suffering read off a global register is the same window taken for the universe. The "whole field" itself is a continuum assumed for convenience, as [The Continuum is a Modeling Convenience](../the-continuum-is-a-modeling-convenience/) shows.

## 五、 公共网格与个体的内部 / 5. The Public Grid and the Individual Interior

这个寄存器画的，是狭窄的、低维的共享公共空间，不是个体的内部。[向量与投影的迷局](../the-vector-and-the-puzzle-of-projections/)：任何一个心智的内部，都不是一个公共坐标系装得下的。一个人对外的劳动落在公共账本的低位上，维持物流，教孩子，照看既有的基础设施，并不因此是一个“低位的人”；内在的生活、创造上的辨别与自身的取向，都不是社会的记账寄存器能量的。

What this register draws is the narrow, low-dimensional shared public space, not the individual interior. [The Vector and the Puzzle of Projections](../the-vector-and-the-puzzle-of-projections/): no Mind's interior fits inside a public coordinate system. Someone whose outward labour sits in the lower bits of the public ledger, keeping logistics running, teaching children, tending established infrastructure, is not thereby a "lower-bit person"; inner life, creative discernment and one's own orientation are not what a society's accounting register can measure.

寄存器量的只是集体的、公共的协调界面，那张社会在其上记账能量、分配资源、举办地位竞赛的共识草图。最高位与低位的区分，说的是活动在这个共享界面之内的取向：是去争夺既有富余的份额，还是去扩展可用的自由度。拿这个模型去给人排名，正是它所剖开的那种膨胀：把一个低维的公共投影，当成一个活着的心智的全部。[可延展的地平线](../the-extendable-horizon/)：正和的能动性不是最高位的专利，任何坐标上都可以取无限游戏的取向，从内向外让能动复利。也没有哪个寄存器装得下哲学，所以[无法闭合的痕迹](../the-unclosable-trace/)说，哲学无法被继承。

The register measures only the collective, public interface of coordination, the consensus draft on which a society keeps its energy accounts, distributes resources and holds its status contests. The distinction between top bit and lower bits describes the orientation of activity inside that shared interface: contending over shares of existing slack, or extending the degrees of freedom available. Using the model to rank people is exactly the inflation it dissects: taking a low-dimensional public projection for the whole of a living Mind. [The Extendable Horizon](../the-extendable-horizon/): positive-sum agency is no privilege of the top bit; an infinite-game orientation can be taken at any coordinate, compounding agency from the inside out. Nor can any register hold philosophy, which is why [The Unclosable Trace](../the-unclosable-trace/) finds that philosophy cannot be inherited.

## 六、 不求共识的姿态 / 6. A Stance That Needs No Consensus

看清寄存器的算术，想去争论、说服、向别的窗口索取认可的冲动就松开了。要求一个分辨 [b₃, b₈] 的窗口去确认 bₙ 的实例化，是同一种本体膨胀：指望一个本地的感知去计算远在其寻址范围之外的坐标。反过来，把别人的窗口读成更小的那一个，也是同一种膨胀。[折叠的连续谱](../the-continuum-of-the-fold/)：心智不靠礼貌的共识合并，彼此只以痕迹到来。

Seeing the arithmetic of the register loosens the urge to argue, persuade, or seek validation from other windows. Asking a window that resolves [b₃, b₈] to confirm the instantiation of bₙ is the same ontological inflation: expecting a local perception to compute coordinates far beyond its addressable range. Reading the other's window as the smaller one is the same inflation in reverse. [The Continuum of the Fold](../the-continuum-of-the-fold/): minds do not merge through polite consensus; each arrives to the other only as traces.

一位旧识带着一桩零和的买卖或一次地位上的盘算来问候时，不必走进那个投影，也不必为自己的坐标辩护，一句轻松的回应就够了，双方都不欠对方一次说服。对方站在自己的窗口里，正如这一处站在这一处的窗口里。纸面上关于位置的等式，越过的正是[破除概念的僭越](../po-chu-gai-nian-de-jian-yue/)剖开的那条线。

When an old acquaintance checks in with a zero-sum deal or a status calculation, there is no need to enter that projection or defend one's own coordinate; a light reply is enough, and neither side owes the other a conversion. They stand in their window just as this place stands in its own. Paper equations about position overstep exactly the line that [Breaking the Overreach of Concepts](../po-chu-gai-nian-de-jian-yue/) dissects.

剩下的，是自己边缘上的那一步。[唯一自洽的无因之果](../the-only-coherent-uncaused-effect/)：把共识游戏冷却下来的残余留在身后，走进尚未渲染的空位，在现实计算下一位的时候让边缘保持敞开。最高位打开一个新的自由度，是[非万物之理](../manifesto-of-not-a-theory-of-everything/)所说的那一次正交的移动。

What remains is the step at one's own edge. [The Only Coherent Uncaused Effect](../the-only-coherent-uncaused-effect/): leaving the cooled residue of consensus games behind, stepping into the unrendered empty place, and keeping the edge open while reality computes the next bit. A top bit opening a new degree of freedom is the orthogonal move that [Not a Theory of Everything](../manifesto-of-not-a-theory-of-everything/) describes.
