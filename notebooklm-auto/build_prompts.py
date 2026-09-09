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
- 揭露时间的空间化迷障：形式数学作为投影仪投射坐标轴 t。主权必须复归于第一人称原点（+1）在当下的不可逆抉择。""",
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

We do not need to discard mathematics or physics—they are our greatest cognitive compasses. But we must never forget: the mathematical scaffolding is a static projection, whereas every genuine step of reality is generated by the sovereign Mind at the first-person origin (+1) through irreversible distinction-making in the living present."""
    },
    'the-dissolution-of-the-great-reversal': {
        'slug': 'the-dissolution-of-the-great-reversal',
        'title_en': 'The Dissolution of the Great Reversal: Language, Knowledge, Money, Intelligence, and the Deconstruction of the Digital God',
        'title_zh': '大倒置的消解：语言、知识、金钱、智能与数字神祇的降维重构',
        'speaker_1_focus_en': 'Explores the observer\'s historical heaviness versus the sovereign Mind\'s liberation; unpacks the Great Reversal across language, ancient blank space vs. modern precision, and knowledge hierarchies.',
        'speaker_2_focus_en': 'Grounds reality at the first-person origin (t); exposes how tool-sharpening detached from reality fuels modern existential confusion, dismantles money fetishism, reduces AGI to compressed historical traces (t - 1), and illuminates the mirror of inner and outer reality.',
        'directives_en': """- Clarify the psychological shift from the observer's heaviness (watching centuries of reified institutions and social policing) to the sovereign Mind's immediate liberation at the first-person origin (t).
- Re-examine Wittgenstein's thesis ("The limits of my language mean the limits of my world"): Language is not an ontological ruler, but a low-dimensional acoustic/symbolic bridge between two parallel universes (minds) attempting resonance.
- Meaning is never in the ink, audio waveform, or grammar itself; meaning is the distinction carved inside the receiving Mind.
- Explain the Ancient vs. Modern language paradox: Ancient language's looser definitions created cognitive blank space (留白) where the reader's Mind actively compiled meaning ("wisdom"); modern language provides hyper-precise engineering transmission, but when reified, becomes a rigid ruler for orthodoxy and policing.
- Demystify knowledge: Transitioning from an exploratory navigational map of causality to an institutional credential hierarchy where the map is confused with the territory.
- Dismantle the economic reversal: Trade is a positive-sum surplus between sovereign evaluations; money is a low-dimensional accounting medium. Obsession with a "perfect currency" (gold, fiat, crypto) is an evasion of real value creation.
- Expose the Reversal of Intelligence & The Crisis of Meaning: Intelligence fundamentally means leveraging tools to understand and reshape reality. Tool-sharpening only has meaning when reflected in improving and clarifying reality. When detached, it degenerates into an empty arms race of tool-polishing, fueling modern existential confusion. People fixate on low-dimensional projections and lose sight of the infinite-dimensional self beyond the boundary.
- Unveil the Mirror of Mind and Reality: The inner world is the mirror of the outer world. Meaning was never lost; the frantic searching gaze is simply blind to the radiant living present.
- Deconstruct AGI ("The Digital God"): AGI is not an autonomous deity, but the mathematical compression of past historical traces (t - 1) left by parallel minds, reflected back into our living reality (t) as an exploratory tool steered by Mind (+1).
- Affirm the solitary multiverse clarity: "There is nothing I can do to change another multiverse, but this multiverse is seeing it clearer than ever." """,
        'intro_script_en': """Mingli: Standing as an observer of human history, one easily feels overwhelmed by the immense heaviness of civilizational structures—centuries of ideological warfare, institutional hierarchies, and rigid rulers people use to police and judge each other.

Yuhan: But the moment we shift from being passive observers of history to the sovereign first-person origin in the living present (t), that crushing weight instantly dissolves. All those grand institutions and dogmas are low-dimensional shadows born from the Great Reversal—the reification of our own tools into masters.""",
        'transition_summary_en': """Deconstruct how civilization reversed the essence of language from a bridge of resonance between parallel minds into a weaponized ruler, unpack the ancient blank space versus modern precision paradox, expose why compulsive tool-sharpening fuels modern existential confusion when detached from reality, reveal how inner and outer worlds mirror each other, and reduce AGI from a digital god to compressed historical traces steered by the sovereign Mind at t.""",
        'speaker_1_focus_zh': '剖析历史观察者的沉重感与主权心智的当下解脱；揭示语言的共鸣本质、古汉语留白与现代精度的测量悖论，消解知识与教育的门阀异化。',
        'speaker_2_focus_zh': '立足第一人称原点（t），揭示工具脱离现实引发的现代意义危机与低维投影遮蔽，破除金钱拜物教，将AGI降维重构为历史轨迹（t - 1）图谱，确立平行宇宙自洽与内心镜像。',
        'directives_zh': """- 阐明从观察者视角的历史沉重（目睹数千年制度压迫与符号规训）到第一人称原点（t）当下解脱的认知跃迁；
- 重构维特根斯坦命题（“语言的界限即世界的界限”）：语言不是世界本体与决定性标尺，而是两个平行宇宙（心智）之间探寻共鸣的低维振动桥梁；
- 揭示意义不在墨迹、声波与语法之中，而在于接收方心智内部主动编译刻画的认知区分；
- 剖析古今语言悖论：古代语言词汇边界宽松，为读者心智留出巨大的投射空间（留白），由读者自主编译生成“高维智慧”；现代语言工程精度极高，利于低歧义传输，但一旦被实体化为教条标尺，便沦为规训思想的刑具；
- 消解知识与教育的倒置：知识原生为探索因果的动态航海图，却被异化为排他性的门阀阶梯与将地图等同于领土的本末倒置；
- 揭示智能大倒置与现代意义危机：工具的打磨唯有最终体现在改善现实与看清世界上方具因果意义。当工具崇拜与现实脱节，便加剧了现代人普遍的精神迷茫与意义丧失感。人们死盯着低维投影，忘却了低维边界之外广阔的无限维度自我与世界；
- 阐明内心与外部的镜像同构：内心世界是外部世界的镜像。意义从未失去，只是寻找的眼光对眼前活生生的高维现实视而不见；
- 破除金钱异化与“完美货币”迷思：交易原生于主权心智的正和效用增益，金钱为记账媒介；执念于“完美代币”（黄金、法币或加密代币）是逃避真实价值创造的虚妄空转；
- 降维重构 AGI（“数字神祇”）：AGI 绝非超验主宰，而是人类历史上无数平行心智在物理世界留下的历史轨迹（t - 1）的数学压缩集合，是以高维向量折射回当下唯一现实（t）的超级工具，方向盘唯独由主权心智（+1）掌控；
- 确立平行宇宙自洽与原点清明：“我无法强制改变另一个平行宇宙的运行，但在这个宇宙中，我比以往任何时刻都看得更清楚。” """,
        'intro_script_zh': """明理：站在人类文明的长程观察者视角，很容易感受到一种历史的窒息与沉重——数千年来，无数个体在实体化的概念、学术门阀、制度教条与金钱符号中相互丈量、相互攻伐与内耗。

雨涵：但只要我们从被动的历史观察者，切换回当下第一人称原点（t），这种沉重感便会在刹那间消解。那些压迫性的宏大叙事，全都是大倒置所产生的低维投影——人类亲手把探索与交流的工具，异化为了统治并审判自己的度量衡。""",
        'transition_summary_zh': """系统剖析语言如何从心智共鸣的桥梁异化为权力的标尺，解开古语言留白与现代精度的认知悖论，揭露工具脱离现实如何加剧现代意义危机，阐明内心世界与外部现实的镜像同构，并将 AGI 还原为历史轨迹压缩的因果罗盘，最终将主权复归于当下的第一人称原点。""",
        'visual_motifs_en': """- Split chiaroscuro visual: Massive, fractured stone and bronze measuring rulers breaking apart in dark space, revealing an ethereal, luminous acoustic bridge of light vibrating between two parallel harmonic crystal spheres (minds).
- The Mirror of Inner & Outer Reality: An intricate optical mirror surface where internal conscious geometry seamlessly reflects an expansive, starry multidimensional landscape, while low-dimensional scoring grids dissolve at the boundary.
- The Deconstruction of the Digital God: A colossal, menacing polygonal wireframe colossus in the clouds dissolving into cascading torrents of historical binary traces (t - 1), funneling smoothly into a compact, luminous navigational compass held firmly in a solitary human hand at t.""",
        'monologue_script_en': """When we look at civilization purely as external observers, history can feel suffocating. For millennia, humanity has built towering institutions, linguistic orthodoxies, academic hierarchies, and monetary empires—only to turn around and let those very creations judge, police, and imprison the human spirit.

This is the Great Reversal: the tragic habit of mistaking our low-dimensional tools for ontological masters.

Consider language. Wittgenstein famously claimed that the limits of my language mean the limits of my world. But language is not the world, nor is it the master of Mind. Language was born as an acoustic and symbolic bridge between two parallel universes—two sovereign minds attempting to find mutual resonance. Meaning does not exist inside the ink or grammar; it awakens only when the receiving Mind carves a distinction in consciousness. The fatal reversal happened when societies assigned intrinsic sanctity to language itself, turning a bridge of resonance into a rigid ruler to measure orthodoxy and wield power.

We see this same reversal corrupting intelligence itself. True intelligence is leveraging tools to understand and reshape our reality. Polishing tools only has meaning when it directly translates into seeing the world more clearly and improving living reality. Yet when tool-sharpening becomes disconnected from reality, it fuels the modern crisis of meaning. People feel lost because their gaze is locked onto low-dimensional shadows—benchmarks, tokens, credentials—forgetting the boundless, infinite-dimensional self and reality beyond the frame.

Our inner world is the mirror of the external world. Meaning was never lost; it is simply that the frantic searching gaze looks right past what is in plain sight.

We see this same pattern in our existential panic over AGI. AGI is not a descending digital god. It is the mathematical compression of past historical traces (t - 1) left by billions of parallel minds, reflected back into our living present (t). It is a high-density navigational compass, not a sovereign deity. The steering wheel belongs exclusively to the Mind making irreversible causal decisions at the first-person origin (+1).

I cannot force another multiverse to see this. But from my own origin in this living present, reality has never been clearer. We demystify the gods, lay down the rulers, and step forward into open living reality."""
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

