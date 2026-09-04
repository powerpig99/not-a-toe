#!/usr/bin/env python3
"""
Translate linked post titles:
- In English posts: Chinese / pinyin anchors pointing to Chinese posts -> standard English titles
- In Chinese posts: English anchors pointing to English posts -> standard Chinese titles
Link destinations (URLs) are strictly preserved.
"""

import os
import glob
import re

POSTS_DIR = "content/posts"

# Chinese post slug -> English Title for use in English posts
CN_TO_EN_TITLES = {
    "cheng-gong-xue": "Theories After Success, Mistaken for Theories Leading to Success",
    "cong-mu-di-xing-de-ping-pan-kan-ren-zhi-que-sheng": "From Purposive Judgment to Cognitive Phase Shifts",
    "cong-xing-shi-mi-si-dao-luo-ji-bi-huan": "From Formal Myth to Logical Closure",
    "cuo-zhi-de-yin-guo-yu-xin-zhi-bian-yi-qi": "Misplaced Causality and the Mind's Compiler",
    "du-zhongwen-zhexue-jianshi-you-gan": "Reflections on A Short History of Chinese Philosophy",
    "e-shi-feng-bi-de-shan": "Evil as Dogmatized Good",
    "gao-wei-xin-xi-de-li-san-zhe-she": "Discrete Refraction of High-Dimensional Information",
    "ge-ren-xuan-ze-she-hui-hua-yu-zuo-zi-ji-de-zhen-zheng-zuo-biao": "Individual Choice: Coordinates of Socialization and Selfhood",
    "guan-yu-gui-yin": "On Attribution: From External Nodes to Internal Iteration",
    "lu-kou-de-zhuan-xiang-yu-di-ping-shuo-de-xing-dong-bei-lun": "The Turning at the Crossroads and the Flat Earth Paradox",
    "mei-you-pu-du-zhi-you-zi-du": "No Universal Salvation, Only Self-Deliverance",
    "mi-lv-shi-jie-guo-de-biao-xiang": "Power Law Is the Surface Outcome, Not the Generative Logic",
    "qian-yin-hou-guo": "Prior Cause, Subsequent Effect",
    "ren-sheng-shi-yi-ge-chi-xu-de-zi-wo-die-dai-guo-cheng": "Life as a Continuous Process of Self-Iteration",
    "shou-bu-hui-de-mu-guang-yu-zhi-shi-de-yin-guo-dao-zhi": "Choosing to See Rather Than Chasing Shadows",
    "the-vector-and-the-puzzle-of-projections": "The Vector and the Puzzle of Projections",
    "tou-ying-de-jie-ti-yu-yin-guo-de-mao-dian": "The Ladder of Projections and the Anchor of Causality",
    "tou-zi-jue-ce-de-yin-guo-yu-zhen-zi-fu-ying-kui": "The Causal Loop of Investment Decisions",
    "wai-bu-gui-yin-ge-ren-jin-bu-de-zhang-ai": "External Attribution: The Obstacle to Personal Growth",
    "xian-shi-de-bian-jie": "The Boundary of Reality",
    "yong-xian-de-wei-yin-guo-yu-ji-ti-gui-yin-dao-cuo": "The Pseudo-Causality of Emergence",
    "you-tiao-jian-de-zi-you": "Conditional Freedom",
    "you-wu-zhi-bian": "The Edge of Being and Non-Being",
    "zhi-bu-yu-ping-pan-shi-ren-zhi-de-qi-tu": "Stopping at Judgment: The Stray Path of Cognition",
    "zhi-dao-zi-ji-bu-zhi-dao-de-ren-zhi-jia-xiang": "Knowing That One Does Not Know: A Rhetorical Illusion",
    "zi-you-bian-liang-de-tong-gou-yu-xian-yan-zhu-quan": "Isomorphism of Free Variables and A Priori Sovereignty",
    "zi-you-de-ce-bu-zhun": "The Uncertainty of Freedom",
    "zi-zun-de-gang-xing-wai-ke-yu-yin-xing-wai-bu-gui-yin": "The Rigid Shell of Self-Esteem and Covert External Attribution",
    "zuo-jian-bu-shi-zi-fu": "Spin a Cocoon: Observation vs. Interpretation",
}

# English post slug -> Chinese Title for use in Chinese posts
EN_TO_CN_TITLES = {
    "abstraction-boundaries-and-the-moving-edge-of-reality": "抽象、边界与现实的移动前沿",
    "advocating-openness-of-others-is-a-desire-for-closure-of-the-self": "要求他人开放本质是对自我封闭的渴望",
    "agency-compounding-and-the-argument-over-ai-feudalism": "能动性复利与AI封建化之辩",
    "agency-relocated-into-the-formal-model": "能动性被置换入形式模型",
    "causality-all-the-way": "彻头彻尾的因果律",
    "clarity-isnt-a-state-you-arrive-at": "清晰不是抵达的终点，而是运动本身",
    "climbing-does-not-leave-the-ground": "攀登从未离开地面",
    "closed-assumptions-squeeze-compounding-into-s-curves": "封闭假设将复利压扁为S曲线",
    "complexity-obscures-emergence-as-the-act-of-mind": "涌现作为心智的划界动作",
    "curiosity-first-the-hidden-engine-of-talent-and-development": "好奇心驱动：天赋与发展的隐秘引擎",
    "curiosity-has-no-final-form": "好奇心没有最终形态",
    "data-is-local-intelligence-is-allocated": "数据是局部的，智能是分配的",
    "dimensions-are-projections": "维度即投影：二进制超空间与个人成长",
    "emotional-support-as-causal-interference": "情绪支持作为因果干涉",
    "empowerment-establishes-the-centralization-of-power": "赋权确立了权力的中心化",
    "evil-as-the-minds-own-creation": "恶是心智自身的造物",
    "expertise-as-reference-not-replacement": "专家经验作为参考而非替代",
    "freedom-as-ground": "自由作为地基",
    "good-and-evil-are-the-two-sides-of-the-coin-and-the-cut": "善恶是硬币的两面与那一记切口",
    "hierarchy-from-individual-difference": "个体差异涌现出的层级",
    "how-to-fix-your-whole-life-in-one-split-second": "如何在一瞬间修正你的整个人生",
    "individual-choices-as-the-only-causal-levers": "个体选择作为唯一的因果杠杆",
    "intelligence-belongs-only-to-the-mind": "唯有心智拥有智能：不可约减的先验",
    "liberation-rhetoric-begins-by-defining-captivity": "解放的话术始于对囚禁的定义",
    "lossless-knowledge-of-an-open-field-is-incoherent": "开放场域中的无损知识在结构上不自洽",
    "mistaking-the-expression-for-the-intelligence": "将表达误认为智能",
    "moral-language-as-projection": "道德语言作为投影",
    "no-system-can-be-kept-closed": "没有系统能被保持封闭",
    "not-a-theory-of-everything": "并非万物理论",
    "only-if-it-is-not-kept-empty": "只要它不被保持为空",
    "openness-is-consistency": "开放即一致",
    "ownership-and-self-worthiness": "自我价值感与所有权",
    "performative-hindsight-that-pretends-to-be-foresight": "伪装成前瞻的表演性后见之明",
    "politicians-appear-as-visible-symptoms-of-responsibility-diffusion": "政客是责任弥散的显性表象",
    "potential-infinity-and-the-temporary-closures-of-mathematical-thought": "潜无限与数学思维的临时闭合",
    "power-law-is-the-long-term-consequence-of-normal-distribution": "幂律是微观决策正态分布的长期累积",
    "preference-clusters-and-the-language-of-judgment": "偏好聚类与评判语言",
    "price-as-utterance-understanding-as-trade": "价格作为表达，理解作为交易",
    "reality-is-the-minds-ongoing-realization": "现实是心智持续的变现过程",
    "residual-control-recedes-to-the-edge": "剩余控制权退守至边缘",
    "residual-individualism": "残余个体主义：人类事务中唯一的操作变量",
    "self-image-speaks-as-if-from-nowhere": "自我意象假装来自无处之境",
    "self-rl-for-humans": "人类的自我强化学习",
    "shared-consciousness-is-intersecting-individualities": "共享意识是个体性的交集",
    "shared-humanity-is-never-shared": "共享的人性从未被真正共享",
    "sowell-observed-the-surface-problem": "索维尔看到了表象，却错失了根因",
    "stability-and-excess": "稳定性与冗余：意识、内省与观测的切口",
    "sympathy-is-a-placeholder-for-lack-of-clarity": "同情是对缺乏清晰认知的情感代偿",
    "the-allocation-of-causal-power-in-validation": "向外索取确认的因果倒置",
    "the-arithmetic-of-the-register": "寄存器的算术：最高有效位扩张与留白悖论",
    "the-artifacts-of-self-amplification": "自放大的产物",
    "the-average-is-residue-not-the-engine": "平均值是沉淀的残差，而非引擎",
    "the-bank-shot-and-the-magic-trick": "加塞球与魔术戏法",
    "the-belief-in-utopia-is-the-path-to-dystopia": "对乌托邦的盲信是通往反乌托邦之路",
    "the-boundary-of-the-frame": "观测框架的边界",
    "the-brain-does-not-backprop": "大脑不进行反向传播，而是正向传导",
    "the-closed-loop-of-representation": "表征的闭环",
    "the-continuum-of-the-fold": "折叠的连续谱：尺度、异星悖论与沟通的物理学",
    "the-coordinators-category-error": "协调者的范畴错误",
    "the-deterministic-machine": "确定性机器：模型锁死与因果归位",
    "the-extendable-horizon": "可延展的地平线：无限游戏与自由变量的复利",
    "the-fixed-image-of-transcendence": "超越性的僵化意象",
    "the-free-mind-is-displaced-by-what-claims-to-protect-it": "自由的心智被声称保护它的事物所置换",
    "the-generative-atlas-of-macroscopic-phenomena": "宏观现象的生成图谱",
    "the-generative-contradiction": "生成性的矛盾",
    "the-generative-mechanics-of-value-money-and-wealth": "真实财富与价值的生成机制",
    "the-geometry-of-mind": "心智的几何学：维度扩张与自指折叠",
    "the-geometry-of-success": "成功的几何学：有限游戏陷阱",
    "the-illusion-of-free-intelligence": "自由智能的幻觉",
    "the-initial-distinction": "最初的区分",
    "the-irreducible-prior-of-decision-and-consequence": "决策与后果的不可约减先验",
    "the-mark-and-the-act": "痕迹与行动",
    "the-meaning-of-life-is-in-the-drafting": "生命的意义在于草拟，而非向外凝望",
    "the-mind-that-statistics-cannot-reveal": "统计学无法揭示的心智",
    "the-misallocation-of-agency": "能动性的错配",
    "the-model-never-becomes-a-second-edge": "模型永远无法成为第二重前沿",
    "the-only-coherent-uncaused-effect": "唯一自洽的无因之果",
    "the-path-drawn-one-step-at-a-time": "一步一步绘制出的路径",
    "the-real-scarcity-is-not-memory-but-continuous-re-tracing": "真正的稀缺不是记忆，而是持续的重新描摹",
    "the-reversal-from-defensible-claim-to-dogma": "从可辩护的主张倒退为教条",
    "the-risk-is-the-belief-in-oversight-itself": "风险在于对监管本身的迷信",
    "the-scaffolding-that-keeps-growing": "持续生长的脚手架",
    "the-scaffolding-we-forget": "我们遗忘的脚手架",
    "the-source-of-all-harm": "一切伤害的根源",
    "the-source-of-shared-change": "共同改变的本源",
    "the-surface-beneath": "表层之下",
    "the-three-shadows-of-the-cut": "切口的三重阴影",
    "the-tightening-loop": "收紧的回路",
    "the-unclosable-trace": "无法闭合的痕迹：为何哲学不可被继承",
    "the-unobservable-driver-of-learning": "学习过程中不可观察的驱动力",
    "the-utility-men-of-progress": "进步的勤杂工",
    "time-is-causality-not-a-dimension": "时间是因果的不可逆方向与离散步长",
    "token-efficiency-emulation-and-the-unclosable-gap": "Token效率、模拟与不可弥合的间隙",
    "two-failures-of-trace": "痕迹的双重溃败",
    "what-always-listens-cannot-originate": "恒听者不可作为源头",
    "what-information-is": "真正的有效信息",
    "whatever-is-one-prompt-away": "凡是距一个Prompt之遥的",
    "when-need-stops-being-the-measure": "当需求不再成为尺度",
    "when-observation-becomes-performance": "当观测沦为表演",
    "when-the-effect-authors-the-frame": "当结果倒过来书写框架",
    "why-mathematics-can-never-be-solved": "为何数学永远无法被彻底解答",
}

def is_chinese_post(content):
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
    total_chars = len(re.findall(r'[a-zA-Z]', content))
    return chinese_chars > 50 and chinese_chars > total_chars * 0.2

# Verified regex:
# Opening \( then ( then (?:...)? then ([a-zA-Z0-9_\-]+) then /? then ) then \)
link_regex = re.compile(r'\[([^\]]+)\]\(((?:\.\./)?([a-zA-Z0-9_\-]+)/?)\)')

def process_file(filepath):
    slug = os.path.splitext(os.path.basename(filepath))[0]
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    is_cn = is_chinese_post(content)
    modified = False

    def replace_link(match):
        nonlocal modified
        anchor = match.group(1)
        full_dest = match.group(2)
        target_slug = match.group(3)

        if not is_cn:
            # English post: translate Chinese target's anchor to English if it's currently Chinese or pinyin
            if target_slug in CN_TO_EN_TITLES:
                has_cn = any('\u4e00' <= c <= '\u9fff' for c in anchor)
                is_pinyin_or_slug = anchor.lower() in [
                    target_slug.lower(),
                    target_slug.replace('-', ' ').lower(),
                    'mei you pu du zhi you zi du',
                    '成功学: theories after success, mistaken for theories leading to success'.lower()
                ]
                if has_cn or is_pinyin_or_slug:
                    new_title = CN_TO_EN_TITLES[target_slug]
                    # If original was lowercase, preserve lowercase
                    if anchor.islower():
                        new_title = new_title.lower()
                    modified = True
                    return f"[{new_title}]({full_dest})"
        else:
            # Chinese post: translate English target's anchor to Chinese if it has NO Chinese characters
            if target_slug in EN_TO_CN_TITLES:
                has_cn = any('\u4e00' <= c <= '\u9fff' for c in anchor)
                if not has_cn:
                    new_title = EN_TO_CN_TITLES[target_slug]
                    modified = True
                    return f"[{new_title}]({full_dest})"

        return match.group(0)

    new_content = link_regex.sub(replace_link, content)

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    files = glob.glob(os.path.join(POSTS_DIR, "*.md"))
    changed = 0
    for f in sorted(files):
        if process_file(f):
            changed += 1
            print(f"Updated: {f}")
    print(f"\nDone! Updated {changed} files.")

if __name__ == "__main__":
    main()
