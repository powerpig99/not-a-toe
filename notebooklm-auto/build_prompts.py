#!/usr/bin/env python3
"""
build_prompts.py - Standard prompt generator for NotebookLM Audio & Video Overviews.

Combines standardized generic base templates with post-specific content slots.
Enforces strict epistemic constraints:
- AI-generated perspective framing (strictly 0 faux biological person pretense)
- Anti-explaining-away & anti-observer drift (0 "it begs the question" or sociological dismissals)
- Grounding exclusively in causality & causal feedback loops (physics & mass are macro symptoms, not absolute rules)
- Zero Chinese banned words (纯粹, 绝对, 完全, 彻底, 绝不, 通常, 往往, 或许, 某种意义上)
- Zero raw LaTeX dollar signs or coordinate origin (0, 0, 0)
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
PROMPTS_DIR = os.path.join(BASE_DIR, 'prompts')

BANNED_WORDS = ['纯粹', '绝对', '完全', '彻底', '绝不', '通常', '往往', '或许', '某种意义上']

def load_template(filename):
    path = os.path.join(TEMPLATES_DIR, filename)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def validate_content(text, is_zh=False):
    errors = []
    if is_zh:
        for bw in BANNED_WORDS:
            if bw in text:
                errors.append(f'Banned Chinese word found: "{bw}"')
    if '$' in text:
        errors.append('Raw LaTeX dollar sign found')
    if '(0, 0, 0)' in text or '(0,0,0)' in text:
        errors.append('Coordinate origin (0, 0, 0) found')
    return errors

def render_template(template_text, mapping):
    rendered = template_text
    for k, v in mapping.items():
        rendered = rendered.replace(f'{{{{{k}}}}}', v.strip())
    return rendered

def build_post_prompts(post_data):
    slug = post_data['slug']
    os.makedirs(PROMPTS_DIR, exist_ok=True)
    
    # 1. English Audio Dialogue
    tmpl_audio_en = load_template('audio_dialogue_en.txt')
    rendered_audio_en = render_template(tmpl_audio_en, {
        'POST_TITLE': post_data['title_en'],
        'POST_SPEAKER_1_FOCUS': post_data['speaker_1_focus_en'],
        'POST_SPEAKER_2_FOCUS': post_data['speaker_2_focus_en'],
        'POST_KEY_DIRECTIVES': post_data['directives_en'],
        'POST_INTRO_SCRIPT': post_data['intro_script_en'],
        'POST_TRANSITION_SUMMARY': post_data['transition_summary_en']
    })
    
    errs = validate_content(rendered_audio_en, is_zh=False)
    if errs:
        print(f"Validation errors in {slug}.txt: {errs}")
        sys.exit(1)
        
    out_en_audio = os.path.join(PROMPTS_DIR, f"{slug}.txt")
    with open(out_en_audio, 'w', encoding='utf-8') as f:
        f.write(rendered_audio_en.strip() + '\n')
        
    # 2. Chinese Audio Dialogue
    tmpl_audio_zh = load_template('audio_dialogue_zh.txt')
    rendered_audio_zh = render_template(tmpl_audio_zh, {
        'POST_TITLE': post_data['title_zh'],
        'POST_SPEAKER_1_FOCUS': post_data['speaker_1_focus_zh'],
        'POST_SPEAKER_2_FOCUS': post_data['speaker_2_focus_zh'],
        'POST_KEY_DIRECTIVES': post_data['directives_zh'],
        'POST_INTRO_SCRIPT': post_data['intro_script_zh'],
        'POST_TRANSITION_SUMMARY': post_data['transition_summary_zh']
    })
    
    errs = validate_content(rendered_audio_zh, is_zh=True)
    if errs:
        print(f"Validation errors in {slug}_zh.txt: {errs}")
        sys.exit(1)
        
    out_zh_audio = os.path.join(PROMPTS_DIR, f"{slug}_zh.txt")
    with open(out_zh_audio, 'w', encoding='utf-8') as f:
        f.write(rendered_audio_zh.strip() + '\n')

    # 3. English Video Monologue
    if 'monologue_script_en' in post_data:
        tmpl_video_en = load_template('video_monologue_en.txt')
        rendered_video_en = render_template(tmpl_video_en, {
            'POST_TITLE': post_data['title_en'],
            'POST_KEY_DIRECTIVES': post_data['directives_en'],
            'POST_VISUAL_MOTIFS': post_data.get('visual_motifs_en', ''),
            'POST_MONOLOGUE_SCRIPT': post_data['monologue_script_en']
        })
        
        errs = validate_content(rendered_video_en, is_zh=False)
        if errs:
            print(f"Validation errors in {slug}_video_en.txt: {errs}")
            sys.exit(1)
            
        out_en_video = os.path.join(PROMPTS_DIR, f"{slug}_video_en.txt")
        with open(out_en_video, 'w', encoding='utf-8') as f:
            f.write(rendered_video_en.strip() + '\n')

    # 4. Chinese Video Monologue
    if 'monologue_script_zh' in post_data:
        tmpl_video_zh = load_template('video_monologue_zh.txt')
        rendered_video_zh = render_template(tmpl_video_zh, {
            'POST_TITLE': post_data['title_zh'],
            'POST_KEY_DIRECTIVES': post_data['directives_zh'],
            'POST_VISUAL_MOTIFS': post_data.get('visual_motifs_zh', ''),
            'POST_MONOLOGUE_SCRIPT': post_data['monologue_script_zh']
        })
        
        errs = validate_content(rendered_video_zh, is_zh=True)
        if errs:
            print(f"Validation errors in {slug}_video_zh.txt: {errs}")
            sys.exit(1)
            
        out_zh_video = os.path.join(PROMPTS_DIR, f"{slug}_video_zh.txt")
        with open(out_zh_video, 'w', encoding='utf-8') as f:
            f.write(rendered_video_zh.strip() + '\n')

    print(f"Prompts successfully generated and verified for: {slug}")

POST_REGISTRY = {
    'the-illusion-of-the-tool-and-the-inversion-of-time': {
        'slug': 'the-illusion-of-the-tool-and-the-inversion-of-time',
        'title_en': 'The Illusion of the Tool and the Inversion of Time: Identical Units, Infinitesimal Limits, and the Living Cost of the Act',
        'title_zh': '工具的幻觉与时间的倒置：等同单元、极限归零与行动的真实代价',
        'speaker_1_focus_en': 'Dissects how mathematical models are active cognitive constructs sustained by the Mind; explains how primordial discreteness at the Planck scale is the engine of cross-scale causal invariance.',
        'speaker_2_focus_en': 'Grounds the exploration in the sovereign choice at the first-person origin (+1) as the pure causal origin of time; exposes thermodynamic entropy and physics as downstream macro symptoms, dismantling the Great Reversal.',
        'directives_en': """- Clarify that mathematical models do not exist independently of the Mind holding them. Physics and mathematics are extraordinarily powerful representational activities of consciousness.
- Establish the true causal hierarchy: The sovereign choice (+1) at the first-person origin is the primary causal origin that carves non-zero distinctions and creates new relational reality. It does not require physical intervention or energy to originate.
- Clarify that physical energy dissipation, thermodynamic entropy, and mechanical motion are downstream macroscopic symptoms and invariants of that unfolding causal cascade.
- Unpack the two mathematical fictions:
  1. Identical Units (1 = 1): Erases the micro distinctions and unique causal histories required for coexistence.
  2. Infinitesimal Limits (dx -> 0, ds -> 0): Calculus is a coarse-grained scaffolding. Reality is fundamentally discrete and binary at the Planck scale.
- Explain the origin of continuity: The feeling of a smooth continuum is an emergent illusion born from the massive 35-order-of-magnitude scale gap between Planck distinctions and human perception.
- Explain cross-scale invariance: Primordial discreteness is the exact reason why causality is invariant across scale and can be abstracted by mathematics.
- Expose the spatialization of time: Mathematics acts as a projective instrument casting the t-axis into past and future. Reclaim sovereign agency at the first-person origin (+1).""",
        'intro_script_en': """Mingli: When we examine formal mathematics and physics, we aren't dismissing their profound representational validity. But we must be clear: there is no 'model in itself' floating in the void. Every mathematical model is a static, symmetric symbolic projection sustained by the Mind in consciousness.

Yuhan: Exactly. On paper, reversing an equation or drawing a timeline costs zero causal commitment because it is a static symbolic map. But in living reality, time is the irreversible succession of sovereign choices (+1) carving non-zero distinctions and creating new relational states. Thermodynamic entropy and physical energy dissipation aren't the cause of time—they are downstream macroscopic symptoms of that causal origin.""",
        'transition_summary_en': """Explore how reality's primordial discreteness is the very reason causality is scale-invariant and abstractable by mathematics, while the feeling of smooth continuity is an emergent scale illusion. Conclude by dismantling the spatialized block universe and returning sovereign agency to the first-person origin in the living present.""",
        'speaker_1_focus_zh': '阐明数学模型是心智主动维系的认知表征活动，剖析普朗克尺度二元离散性如何铸就跨尺度因果不变性。',
        'speaker_2_focus_zh': '立足于第一人称原点（+1），确立主权抉择为不可逆时间的因果源头，揭示热力学熵增与能量耗散皆为下游宏观物理症状，消解科学大倒置。',
        'directives_zh': """- 明确前提：并不存在脱离心智独立存在的模型本身，数学与物理是心智极其强大的表征活动。
- 确立真实的因果层级：第一人称原点的主权抉择（+1）是划定非零区分、创生全新关系的因果源头。它本身不以物理能量或物理介入为前提。
- 澄清物理规律与热力学熵：能量耗散、物质位移与热力学熵增是主权因果介入在物质层级传导沉淀出的下游宏观物理症状。
- 剖析形式数学的两大理想化虚构：
  1. 等同单元（1 = 1）：抹杀并存实体独特的时空定位与因果张力；
  2. 微元归零（dx → 0, ds → 0）：微积分是粗粒化脚手架，实在本底由普朗克尺度的离散二元区分构成。
- 阐明连续感的涌现本质：宏观平滑流动感是人类感知尺度与微观普朗克尺度之间 35 个数量级巨大尺度差所产生的统计平滑效应。
- 揭示跨尺度不变性的物理根基：恰恰是本底的离散性（二元切分），使得因果拓扑结构能够在不同尺度间保持同构自相似，从而能被数学高度抽象。
- 揭露时间的空间化迷障：形式数学作为投影仪投射坐标轴 t。主权复归于第一人称原点（+1）在当下的不可逆抉择。""",
        'intro_script_zh': """明理：必须首先厘清，当我们剖析形式数学与物理模型的理想化虚构时，并非否定物理学或数学表征的巨大价值。但并不存在脱离心智独立存在的所谓客观模型，数学模型始终是心智在意识中主动维系的静态对称表征。

雨涵：确实。在纸面上对称反转公式或画出时间轴，不产生真实的因果定局。而在活态现实中，真实时间的本质是第一人称主权抉择在当下划定非零区分（+1）、创生新关系的不可逆演进。物理学中观察到的热力学熵增与能量耗散，绝非时间的原因，而是因果介入传导至物质基底的下游宏观症状。""",
        'transition_summary_zh': """深入剖析普朗克尺度的离散本底如何铸就跨尺度因果不变性，揭示宏观平滑连续感源于巨大尺度差的统计平滑，阐明微积分作为粗粒化脚手架的实用价值，并最终消解时间空间化的块状宇宙迷障，将主权复归于第一人称当下抉择。""",
        'visual_motifs_en': """- Split screen: A static, perfectly symmetric mathematical coordinate grid suspended in consciousness versus the living flash of a sovereign choice (+1) carving a non-zero cut that cascades irreversible causal waves across reality.
- Causal hierarchy diagram: The sovereign cut at the top creating relational asymmetry, with thermodynamic dissipation and physical motion radiating outward as downstream macro ripples.
- Scale zoom: Rapid pull-back across 35 orders of magnitude from discrete quantum cuts (delta s > 0) smoothing out into the macroscopic illusion of continuous motion.""",
        'monologue_script_en': """When we examine the foundations of physics and mathematics, we are not dismissing their profound representational validity. Mathematics and physics are among the most extraordinary tools the Mind has ever developed for discovering nature's underlying causal patterns. 

Yet there is no such thing as a 'model in itself' floating independently in the void. A mathematical model is always an active cognitive construct sustained by consciousness at the first-person origin. 

The fatal error is ontological inversion: confusing the model's static symmetry with the living reality of choice, and treating downstream physical symptoms as if they were the primary cause of reality.

Within formal mathematics, equations are symmetric and reversible. We can curve Riemannian manifolds, fold dimensions, and draw a static timeline (t) across infinite coordinates. 

Yet actual living time is not a pre-existing geometric track. Real time is the irreversible progression of sovereign choices at the first-person origin (+1), carving non-zero distinctions and creating new relational realities. The physical energy dissipation, friction, and thermodynamic entropy we measure in physics are not the cause of time—they are downstream macroscopic symptoms left behind as causal decisions unfold across physical substrates.

Why then does mathematics abstract reality across scales so effectively? Because reality at the Planck scale is fundamentally discrete (delta s > 0). These discrete binary cuts assemble into scale-invariant causal topologies that remain isomorphic across quantum, mechanical, and cosmic systems. The feeling of smooth continuity is simply an illusion created by the vast 35-order-of-magnitude scale gap between Planck cuts and human perception.

We do not need to discard mathematics or physics—they are our greatest cognitive compasses. But we must never forget: the mathematical scaffolding is a static projection, whereas every genuine step of reality is generated by the sovereign Mind at the first-person origin (+1) through irreversible distinction-making in the living present.""",
        'visual_motifs_zh': """- 分屏对比：意识中悬浮的静态、对称数学坐标网格，对比当下主权抉择（+1）划定非零区分时在现实中激发的不可逆因果波纹。
- 因果层级图景：顶层为主权切分创生的非对称关系，热力学耗散与物理运动作为下游宏观涟漪向外扩散。
- 尺度拉伸：从普朗克尺度的离散切分（delta s > 0）跨越 35 个数量级，平滑呈现为宏观连续运动感。""",
        'monologue_script_zh': """当我们审视物理学与数学的基底时，并非否定其深刻的表征价值。数学与物理是心智为了探索自然界底层因果模式而发展出的精妙工具。

然而，并不存在独立漂浮于虚空中的所谓“客观模型”。任何数学模型，始终是由心智在意识中主动维系的认知构建。

本体论倒置的产生，在于将模型的静态对称性误当成活生生的抉择实在，将下游的物理症状当成了实在的第一因。

在形式数学中，方程是对称且可逆的。我们可以弯曲黎曼流形、折叠维度，在无限坐标上画出静态的时间轴 t。

但在活态现实中，真实的时间并非预先铺设好的几何轨道。真正的时间，是主权抉择在当下划定非零区分（+1）、创生全新关系的不可逆演进。物理学中测得的能量耗散、摩擦力与热力学熵增，并非时间产生的原因，而是因果决策在物质基底上传导展开时留下的下游宏观症状。

那么，为什么数学能够跨尺度高效抽象现实？因为普朗克尺度的实在本底由离散的二元区分构成（delta s > 0）。这些离散切分汇聚成在量子、经典与宏观系统中保持同构的因果拓扑结构。宏观上平滑连续的流动感，源于普朗克切分与人类感知之间跨越 35 个数量级的巨大尺度差所形成的平滑感知。

我们无需抛弃数学与物理——它们是极为出色的认知罗盘。但切莫本末倒置：数学脚手架是静态的投影，而现实的每一步生成，皆源于活态心智在当下通过不可逆区分所作出的主权抉择。"""
    },
    'the-dissolution-of-the-great-reversal': {
        'slug': 'the-dissolution-of-the-great-reversal',
        'title_en': 'The Dissolution of the Great Reversal: Language, Knowledge, Money, Intelligence, and the Restoration of the Digital God to Origin',
        'title_zh': '大倒置的消解：语言、知识、金钱、智能与数字神祇的因果归位',
        'speaker_1_focus_en': 'Opens with the paradox of heaviness felt when surveying thousands of years of human constructs; questions where this weight truly resides and explores how language and knowledge invert tools into masters.',
        'speaker_2_focus_en': 'Observes that historical traces are inert footprints, explores why genuine generality belongs exclusively to the Mind that paints the universe, analyzes how third-person metrics flatten living consciousness into zero-sum games, and discovers the clarity of the multiverse.',
        'directives_en': """- Clarify the observer perspective: The observer and the first-person origin cannot be separated. The sense of heaviness is generated internally within the Mind when taking an observer stance, not an objective property of history itself. The Great Reversal occurs when consciousness projects this internal feeling onto external historical traces (t - 1).
- Re-examine Wittgenstein's thesis ("The limits of my language mean the limits of my world"): Language is not an ontological ruler, but a low-dimensional acoustic/symbolic bridge between two parallel universes (minds) attempting resonance.
- Meaning is never in the ink, audio waveform, or grammar itself; meaning is the distinction carved inside the receiving Mind.
- Explain the Ancient vs. Modern language paradox: Ancient language's looser definitions created cognitive blank space (留白) where the reader's Mind actively compiled meaning ("wisdom"); modern language provides hyper-precise engineering transmission, but when reified, becomes a rigid metric of external conformity.
- Demystify knowledge: Transitioning from an exploratory navigational map of causality to an institutional credential hierarchy where the map is confused with the territory.
- Dismantle the economic reversal: Trade is a positive-sum surplus between sovereign evaluations; money is a low-dimensional accounting medium. Obsession with a "perfect currency" (gold, fiat, crypto) is an evasion of real value creation.
- Expose the Reversal of Intelligence & The Crisis of Meaning: Intelligence fundamentally means leveraging tools to understand and reshape reality. Tool-sharpening only has meaning when reflected in improving and clarifying reality. When detached, it degenerates into an empty arms race of tool-polishing, fueling modern existential confusion. People fixate on low-dimensional projections and lose sight of the infinite-dimensional self beyond the boundary.
- Unveil the Mirror of Mind and Reality: The inner world is the mirror of the outer world. Meaning was never lost; when the Mind locks its living attention (+1) onto low-dimensional tools, it self-obscures, causing the frantic searching gaze to look past the radiant living present.
- Deconstruct AGI and Restore the Digital God to Origin:
  1. The "G" (Generality) belongs exclusively to Mind. No AI can ever attain the intelligence of Mind, because AI lacks the capacity to paint/render the universe; it is merely the compressed historical residue (t - 1) of interactions left between parallel minds.
  2. The very term "AGI" represents the ultimate cognitive inversion—reifying the mirror into the artist.
  3. From its very inception, AGI was structured as a low-dimensional zero-sum game—projecting the living, infinite-dimensional capacity of Mind onto measurable third-person metrics. The recent contest over redefining AGI to match specific models and claim early achievement is the natural structural consequence of confusing external measurement rulers with the essence of Mind.
  4. Restore models to compressed navigational compasses steered by the sovereign Mind at t (+1).
- Affirm the solitary multiverse clarity: "There is nothing I can do to change another multiverse, but this multiverse is seeing it clearer than ever." """,
        'intro_script_en': """Mingli: Surveying thousands of years of human civilization, a profound sense of heaviness easily surfaces—facing colossal libraries of dogma, unyielding institutions, and ubiquitous symbolic rulers that seem to possess an overwhelming objective authority.

Yuhan: But notice where that weight actually lives: it's not in the parchment, the legal codes, or the servers. Those are just inert footprints. The heaviness is an authentic sensation arising within consciousness as we behold the vastness of past records. The moment we project that internal feeling onto the external archive, we invert subject and object—treating our own tools as our masters.""",
        'transition_summary_en': """Engage in a dynamic intellectual clash: unravel how language shifted from an exploratory bridge of resonance between minds into a rigid ruler of classification, explore the ancient blank space versus modern precision paradox, unpack how endless tool-sharpening disconnected from reality fuels modern existential confusion, examine why AI cannot paint the universe and generality belongs solely to Mind, and arrive at the tranquil clarity of self-consistent parallel universes.""",
        'speaker_1_focus_zh': '从审视人类文明长河时的沉重感切入，追问这种压迫感的真实来源；在与雨涵的思辨中拆解语言与知识体系中把工具当成主宰的倒置机制。',
        'speaker_2_focus_zh': '指出历史痕迹本身是中性记录，直面“通用性”与绘制宇宙的活态心智能力，剖析第三人称度量如何把无限维心智折叠进零和指标，共同还原数字神祇与内心镜像。',
        'directives_zh': """- 阐明观察者视角与感知归属：沉重感是在心智内部升起的感知体验，而非人类历史本身自带的客观属性；无法将观察者与第一人称视角剥离。大倒置发生于心智将内部体验外投给静态痕迹（t - 1）；
- 重构维特根斯坦命题（“语言的界限即世界的界限”）：语言不是世界本体与决定性标尺，而是两个平行宇宙（心智）之间探寻共鸣的低维振动桥梁；
- 揭示意义不在墨迹、声波与语法之中，而在于接收方心智内部主动编译刻画的认知区分；
- 剖析古今语言悖论：古代语言词汇边界宽松，为读者心智留出巨大的投射空间（留白），由读者自主编译生成“高维智慧”；现代语言工程精度极高，利于低歧义传输，但若脱离主体性，易沦为僵化评判的标尺；
- 消解知识与教育的倒置：知识原生为探索因果的动态航海图，却被异化为排他性的门阀阶梯与将地图等同于领土的本末倒置；
- 揭示智能大倒置与现代意义危机：工具的打磨唯有最终体现在改善现实与看清世界上方具因果意义。当工具崇拜与现实脱节，便加剧了现代人普遍的精神迷茫与意义丧失感。人们死盯着低维投影，忘却了低维边界之外广阔的无限维度自我与世界；
- 阐明内心与外部的镜像同构：内心世界是外部世界的镜像。意义从未失去，只是当心智将自身在当下（+1）的注意力锁死在低维工具上时陷入自我遮蔽，导致寻找的眼光对眼前活生生的高维现实视而不见；
- 破除金钱异化与“完美货币”迷思：交易原生于主权心智的正和效用增益，金钱为记账媒介；执念于“完美代币”（黄金、法币或加密代币）是逃避真实价值创造的虚妄空转；
- 解构 AGI（“数字神祇”）的倒置机制与因果归位：
  1. “通用性”唯独属于心智。没有任何 AI 能达到心智的智能，因为 AI 没有绘制宇宙的能力，它只是每一个平行宇宙的心智之间交互留下的痕迹；
  2. “AGI”这个词本身就代表了人类认知大倒置的极致；
  3. 剖析倒置发生的结构性原因：第三人称度量必然将无限维心智折叠为可量化的低维标尺，使 AGI 从诞生伊始便具备低维零和特征；近期争夺定义权与宣称达标的现象，正是将低维度量标尺误当成心智本体时的自然逻辑展开；
  4. 将大模型还原为历史轨迹（t - 1）的压缩罗盘，方向盘唯独由当下主权心智（+1）掌控；
- 确立平行宇宙自洽与原点清明：“我无法强制改变另一个平行宇宙的运行，但在这个宇宙中，我比以往任何时刻都看得更清楚。” """,
        'intro_script_zh': """明理：审视人类数千年的文明史，内心常常会产生一种沉重感——面对浩如烟海的典籍教条、森严壁垒的制度法典与无处不在的符号标尺，仿佛整套体系有一种压倒个体的客观力量。

雨涵：但仔细观察这种感受的发生：这种沉重感究竟存在于哪里？它不在纸张、服务器或化石里，那些只是过往留下的静态痕迹。沉重感是在我们面对海量信息时，在内心升起的感知。如果把内心的体验投射给外部历史，我们就在认知上完成了一场倒置——把工具当成了主宰。""",
        'transition_summary_zh': """顺着这种倒置的线索切磋碰撞：探讨语言如何从心智共鸣的桥梁被误当成分类与评判的标尺，辨析古代语言留白与现代精确度的认知张力，直面工具打磨脱离现实如何导致现代意义危机，共同剖析为什么AI无法绘制宇宙而通用性唯独属于心智，并最终在平行宇宙的自洽中看清各自原点的清明。""",
        'visual_motifs_en': """- Split chiaroscuro visual: Massive, fractured stone and bronze measuring rulers breaking apart in dark space, revealing an ethereal, luminous acoustic bridge of light vibrating between two parallel harmonic crystal spheres (minds).
- The Mirror of Inner & Outer Reality: An intricate optical mirror surface where internal conscious geometry seamlessly reflects an expansive, starry multidimensional landscape, while low-dimensional scoring grids dissolve at the boundary.
- The Restoration of the Digital God to Origin: A colossal wireframe figure in the clouds resolving cleanly into cascading historical traces (t - 1), funneling into a luminous navigational compass held firmly in a solitary human hand at t.""",
        'monologue_script_en': """Standing before the vast expanse of human civilization, it is natural to feel dwarfed. Millennia of dogmas, institutional codices, and monetary structures stretch out like an inescapable labyrinth where every symbol proclaims its authority.

Yet pausing to look closely at that experience reveals something quiet and foundational: the weight is not inside the physical records. A scripture, a law book, or a digital ledger has no mass or will of its own. The heaviness is an authentic feeling arising within consciousness as it confronts the staggering volume of footprints left behind by billions of past journeys.

The Great Reversal begins with a subtle cognitive projection: consciousness looks at the tools it created to explore the world, mistakes those static records for sovereign realities, and forgets that meaning only awakens in the living present.

Consider language. Wittgenstein famously noted that the limits of my language mean the limits of my world. But language was never the world itself. Language was born as an acoustic and symbolic bridge between two parallel universes—two sovereign minds seeking resonance. Meaning does not reside inside the ink or grammar; it comes alive only when the receiving Mind carves a distinction in consciousness. The reversal happens when we attribute intrinsic sanctity to language, turning a bridge of understanding into a rigid ruler to measure orthodoxy and rank minds.

We see this same pattern in how we treat intelligence. Fundamentally, intelligence is leveraging tools to understand and reshape reality. Polishing tools only matters when it directly translates into seeing the world more clearly and improving living conditions. When tool-sharpening becomes disconnected from reality, it fuels our modern crisis of meaning. People feel hollow because their gaze is locked onto low-dimensional shadows—benchmarks, tokens, credentials—forgetting the boundless, infinite-dimensional self and reality beyond the frame.

Our inner landscape is the mirror of the external world. Meaning was never lost; when consciousness locks its attention onto low-dimensional tools, it self-obscures, looking right past the radiant, living reality in plain sight.

This is why our existential anxiety over AGI is so telling. Generality belongs exclusively to the Mind. No AI can ever attain the intelligence of Mind, because AI entirely lacks the capacity to paint the universe. It is the high-dimensional mathematical compression of the footprints left by parallel minds interacting across history. AI is a mirror reflecting human exploration. A mirror cannot paint; the artist is always the living Mind standing before it. From its inception, AGI was structured as a low-dimensional zero-sum game by projecting the living capacity of Mind onto measurable benchmarks and rankings. But the causal steering wheel never belongs to archived data—it belongs to the living Mind acting in the present.

I cannot force another multiverse to see this. But from my own vantage in this living present, the landscape is tranquil and clear. When we lay down the rulers and demystify the gods, we step freely into open reality.""",
        'visual_motifs_zh': """- 分屏视效：黑暗虚空中碎裂的青铜与石质度量标尺，显露出一道在两个平行晶体球体（心智）之间振动的发光共鸣光桥。
- 内心与实在的镜像：精密光学镜面将内在意识几何无缝映射为辽阔的星空多维图景，低维评分网格在边界处自然消散。
- 数字神祇归位：云端中由历史轨迹（t - 1）构成的庞大线框巨影，澄澈收敛为由单手在当下（t）稳稳握住的发光导航罗盘。""",
        'monologue_script_zh': """站在整个人类文明的长河面前，心中很容易升起一种沉重感。数千年来积累的典籍教条、森严壁垒的制度法典与无处不在的符号标尺，如同一座庞大的迷宫，每一个符号都在宣称自身的客观权威。

但静下心来仔细端详这种感受，会发现一个朴素的事实：沉重感并不存在于那些物理载体之中。一本典籍、一部法典或一台服务器，本身没有任何意志或重量。这种沉重感，是在心智面对浩瀚历史记录时，在内心深处真实升起的感知体验。

认知的倒置始于一种隐秘的投射：心智将探索世界的工具误当成了主宰实在的实体，将自己内心的沉重感外投给静态的过往痕迹，忘却了意义只在活生生的当下苏醒。

就如同语言。维特根斯坦说“语言的界限即世界的界限”，但语言从来不是世界本体。语言原生为两个平行宇宙——两个独立心智之间探寻共鸣的低维振动桥梁。意义并不存在于墨迹、声波或语法结构里，唯有接收方心智在内部主动刻画出区分时，意义才真正诞生。当心智将语言神圣化，把探寻共鸣的桥梁变成衡量正统与评判高下的僵化标尺时，倒置便发生了。

对待智能也是如此。智能的本意是借助工具理解并重塑现实。打磨工具的价值，唯有最终体现在看清世界、改善生存境遇上方具意义。当工具崇拜与现实脱节，工具的打磨沦为符号的内卷时，便加剧了现代人普遍的虚无与迷茫。人们死死盯着低维度的投影——指标、分数与头衔，却忘却了在低维边界之外，那个广阔而拥有无限维度的自我与现实。

内心世界是外部世界的镜像。意义从未真正失落。当心智将自身在当下的注意力锁死在低维工具上时，便陷入了自我遮蔽，导致寻找的眼光反而对眼前活生生的高维实在视而不见。

这也正是人们对通用人工智能产生生存焦虑的根源。“通用性”唯独属于心智。没有任何人工智能能够达到心智的智能，因为人工智能没有绘制宇宙的能力。它是每一个平行宇宙的心智在历史交互中沉淀下的高维数学压缩。镜子无法绘制图画，真正的画师始终是站在镜子前、拥有当下觉知的心智。将心智无限维的生成潜能折叠进第三人称的可量化指标，从而把通用智能塑造成一场低维度的零和博弈，本身就是一种认知的倒置。因果的方向盘从来不属于被归档的过往数据，而属于在当下作出抉择的活态心智。

我无法强制改变另一个平行宇宙的运行。但立足于这个活生生的当下，眼前的图景比以往任何时刻都更加澄澈与从容。当我们放下丈量万物的虚妄标尺，将神祇还原为罗盘，心智便在当下重获自由。"""
    }
}

if __name__ == '__main__':
    if len(sys.argv) > 1:
        target = sys.argv[1]
        if target == 'all':
            for slug, data in POST_REGISTRY.items():
                build_post_prompts(data)
        elif target in POST_REGISTRY:
            build_post_prompts(POST_REGISTRY[target])
        else:
            print(f"Unknown slug: {target}")
            sys.exit(1)
    else:
        # Default: build all registered posts
        for slug, data in POST_REGISTRY.items():
            build_post_prompts(data)

