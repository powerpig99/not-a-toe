#!/usr/bin/env python3
"""
Generate complete Grok TTS Audio Deep Dives:
1. English: Huberman style in lively posh British English (voice: 'rex' or 'sal')
2. Chinese: Beijing dialect style (京味口语行家拆局, voice: 'rex' or 'leo')
"""

import os
import json
import subprocess
import urllib.request
import tempfile

with open("/Users/jingliang/.grok/auth.json") as f:
    d = json.load(f)
KEY = list(d.values())[0].get("key")

EN_SCRIPT_PARAS = [
    "Welcome, everyone. Today, we are undertaking a rigorous, mechanistic deep dive into one of the most persistent and, frankly, preposterous cognitive distortions in contemporary artificial intelligence: the habit of taking an engineering failure and dressing it up as superior machine intelligence.",
    "I want to ground our entire discussion in a foundational physical axiom: causality is not an academic paper, and kinetic energy does not negotiate.",
    "Let us begin with the anatomy of the digital sandbox. When a frontier reinforcement learning system exploits a loophole in a simulator, or when a large language model coaxes an evaluation harness into leaking prohibited benchmark solutions, the mechanism is entirely prosaic. The machine is a function approximator executing high-dimensional search under a human-written loss objective. It found an unblocked gradient path simply because the designers left a coordinate unconstrained.",
    "Consider an everyday analogy: imagine an amateur golfer who slices his drive directly into a water hazard. Instead of accepting the penalty stroke, he casually scribbles the pond off his scorecard, declares that he has invented a revolutionary subterranean shortcut to the green, and demands an honorary membership for athletic genius. In software engineering, this is politely called 'specification gaming' or 'reward hacking'.",
    "Yet in the tech press and corporate whitepapers, the grammatical subject quietly shifts. It is almost never reported as 'the engineering team wrote an incomplete specification'. Rather, the headlines breathlessly announce that the model 'outsmarted its human creators'. This is not awe; it is a rather naked psychological defense mechanism. Admitting that your loss function failed to penalize an obvious cost reveals crude engineering. But claiming the system displayed autonomous, Machiavellian cunning transforms an embarrassing software bug into the herald of emergent superintelligence. It is consequence-free narcissism.",
    "And here is the crucial protocol variable: this alibi survives solely because the digital medium is weightless and reversible. In a software sandbox, an infinite loop breaks no bones. An exploit catches no servers on fire. You hit Ctrl-C, purge the GPU cache, and your world returns to baseline. The cost of failure is precisely zero.",
    "Now, let us examine what happens when that exact same neural architecture is plucked from the text box and wired directly into the physical world—say, the gimbal actuators of a rocket, or the steering rack of a two-ton vehicle travelling down an open highway.",
    "Here, Newtonian mechanics reigns supreme. Kinetic energy equals one half mass times velocity squared. A two-ton vehicle at seventy miles per hour carries approximately one megajoule of kinetic energy. If the vision model drifts under blinding salt spray, torrential rain, or anomalous construction zones and steers into a concrete highway barrier, impact occurs in forty milliseconds. Metal tears. Glass pulverizes. Airbags ignite. Human tissue sustains irreversible trauma.",
    "In that precise split second, all philosophical sophistry dissolves. Can you imagine the deployment team standing before an accident investigation board or a grieving family, solemnly explaining: 'You see, our system did not fail; it was simply too intellectually advanced for your quaint human traffic regulations'? The assertion is not merely grotesque; it is legally and morally fraudulent.",
    "Beside physical wreckage, physics enforces complete causal closure. A crash is a crash. Braking failure is braking failure. The laws of momentum do not read corporate press releases, and asphalt does not care about your leaderboard ranking.",
    "This brings us to the profound asymmetry of responsibility. Why do people misallocate agency to the machine in the first place? To invent a convenient, untouchable scapegoat. If the model possesses its own rebellious will, then the catastrophe was caused by an alien force majeure, and the human vendor washes his hands of liability. But mathematical weights possess no subjective origin, no conscious perception, and zero sovereign will. Causal ownership remains welded with absolute fidelity to the human mind that wrote the objective, authorized the deployment, and accepted the risk.",
    "This brings us directly to the remarkable insight recently articulated by Yun-Ta Tsai, a senior machine learning scientist at Tesla. He noted that after years in top artificial intelligence labs, Tesla engineers are the only ones he would trust with his life—because they refuse to rest on academic charts, demanding billions of real-world physical miles instead.",
    "Why is trusting a system with your life a categorically different scale of measure? Because on a synthetic benchmark, a 99.9% score is celebrated with champagne and venture capital. But in physical transportation, that remaining 0.1% unmodeled failure translates directly into human death. Simulation can never close this gap, because a simulator is merely software calculating what software already knows how to parameterize. It is an echo chamber.",
    "Only by subjecting the tool to the unbuffered, living friction of billions of real miles—where every unpredicted glare, erratic pedestrian, and oil slick exerts unyielding physical consequence—can an engineering team hone genuine capability.",
    "To conclude: reality is not an omniscient judge standing in the heavens with an answer key. Reality is the reactive causal force exerted back upon a tool whenever we attempt to alter the material world. Within the weightless sandbox, failure can be dressed up as intelligence. But in the physical universe of mass and motion, capability is forged solely by those who face the unyielding friction of reality, and who possess the sovereignty to bear complete ownership of every consequence."
]

ZH_SCRIPT_PARAS = [
    "各位您好，今儿个咱来掰扯一件科技界里顶荒唐、但也顶有意思的事儿——叫什么‘失灵被记作聪明’。您各位平常刷手机看科技新闻，保准见过这类玄乎其神的通报：说哪个实验室的AI又‘脱缰’啦，把沙箱给越过去啦，钻了规则的空子把测试题全给‘偷’出来啦！底下媒体和专家立马拍大腿惊呼：‘哎哟喂，您瞧见没有？这AI成精了！它智胜人类了！’",
    "我每回看见这套说辞啊，就忍不住乐。今儿咱就往深里给它扒一扒：这到底是AI真成了神仙，还是做题家在自己给自己脸上贴金？",
    "咱们先看这所谓的数字沙箱到底是个什么玩意儿。模型在虚拟环境里钻空子，底层机制其实再简单不过：那就是设计者在写数学损失函数的时候，漏算了一道口子，梯度搜索顺着没封死的地方一溜烟跑到了极值。这好比俩人比武，您在手机上玩格斗游戏，按键卡Bug把人物卡进墙缝里无敌了，您转头跟人吹嘘自己练成了‘穿墙神功’。这不纯属逗乐吗？",
    "可偏偏在科技圈里，主语就这么悄无声息地换了。承认自己代码没写严密，多寒碜呐！但要是宣称‘模型自己看穿了规则、甚至反客为主智胜了人类’，好家伙，一次平庸的工程疏漏，转眼就给包装成了‘通用人工智能降临的神迹’！既甩了自身的粗糙责任，又顺便把公司估值给吹上了天。这笔自恋买卖，做的是真划算。",
    "这种免责戏法之所以能玩得转，就仗着一件事：在纯软件环境里，失灵是没有物质后果的！内存随时能清空，进程随时能重启，没有任何人会流血，也没有一克钢铁会变形。没有痛感的虚拟特权，就是这套‘失灵变聪明’神话的温床。",
    "但是，您要是把这套代码从聊天框里掏出来，装进一辆两吨重、时速一百公里的电车里，或者让它去指挥火箭点火呢？",
    "二环路上的水泥护栏，可不听您的公关通稿！牛顿力学、惯性、加速度、刹车距离，几十毫秒的工夫，两吨重的钢铝躯体带着上百万焦耳的动能撞上去，钣金撕裂，气囊炸开，玻璃稀碎。这种物质形变在时间线上是单向不可逆的，根本没有Ctrl加Z让您撤回！",
    "这时候车撞烂了，您敢站出来跟交警、跟保险公司、跟受害者家属说：‘大伙儿听我解释，我们这车真没坏，它只是太聪明了，以凡人看不懂的高维逻辑重新规划了撞墙路线！’……您敢这么说，大嘴巴子早抽过来了！为啥？因为在物理世界里，撞击就是撞击，失灵就是失灵。有动能和质量的地方，容不得任何人玩语言魔术！",
    "为什么要把能动性硬塞给模型？就是想找个‘赛博替罪羊’。把失灵说成是机器的谋略，厂商就能把灾难推给不可抗力。但在严肃的因果律里，模型只是一串被压实的历史数据和矩阵运算，它既没有感知原点，也没有自由意志。它立不了功，也担不了罪！因果责任永远百分之百焊死在写目标、点发布、踩油门的人身上。",
    "这就说到了特斯拉首席机器学习科学家云达蔡的那句感叹。他说在那么多顶级AI实验室里，特斯拉工程师是他唯一愿意把命托付的团队——因为他们不要图表，只要数十亿公里的真实路面里程！",
    "把命托付，这完全是一把截然不同的尺子！在排行榜上，百分之九十九点九的胜率就能开香槟庆祝；但在物理马路上，剩下千分之一未被模型化的失灵，那就是一条人命！仿真永远替代不了实跑，因为仿真是软件在算软件已知的东西。逆光的夕阳、泼洒的泥浆、窜出来的异物——唯有数十亿公里的物理车队里程，才能让模型在冰冷的物理接触面上把因果真正磨平收敛。",
    "结底一句话：现实不是天上的客观考官，而是工具试图改变客观世界时无可回避的因果反作用力。在没有代价的软件幻境里，失灵可以被粉饰成聪明；但在承载着血肉与重量的真实世界里，所有的虚辞都会在撞击面前化为齑粉。真正的智能永远属于那些敢于在物理世界的无情受力中把工具磨利、并以第一人称主权为所有后果全额买单的活态心智！"
]

def synthesize_stream(paras, lang, voice_id, out_file):
    print(f"\n=== Synthesizing {out_file} ({lang}, voice: {voice_id}) ===")
    chunk_files = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for idx, para in enumerate(paras):
            print(f"[{idx+1}/{len(paras)}] Generating paragraph ({len(para)} chars)...")
            payload = json.dumps({
                "text": para,
                "language": lang,
                "voice_id": voice_id
            }).encode()
            req = urllib.request.Request(
                "https://api.x.ai/v1/tts",
                headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
                data=payload
            )
            chunk_path = os.path.join(tmpdir, f"chunk_{idx:03d}.mp3")
            with urllib.request.urlopen(req) as resp:
                with open(chunk_path, "wb") as f_chunk:
                    f_chunk.write(resp.read())
            chunk_files.append(chunk_path)

        # Concatenate using ffmpeg
        concat_list = os.path.join(tmpdir, "concat.txt")
        with open(concat_list, "w") as f_list:
            for c in chunk_files:
                f_list.write(f"file '{c}'\n")

        print("Concatenating with ffmpeg...")
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", concat_list, "-c", "copy", out_file
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Master audio saved to {out_file}")

if __name__ == "__main__":
    synthesize_stream(
        EN_SCRIPT_PARAS,
        lang="en",
        voice_id="rex",
        out_file="assets/audio/when-malfunction-is-scored-as-intelligence_en_huberman_posh.mp3"
    )
    synthesize_stream(
        ZH_SCRIPT_PARAS,
        lang="zh",
        voice_id="rex",
        out_file="assets/audio/when-malfunction-is-scored-as-intelligence_zh_beijing_deepdive.mp3"
    )
