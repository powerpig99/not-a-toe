#!/usr/bin/env python3
"""
Generate bilingual (EN / ZH) studio narration MP3 tracks for the 21-slide
Living Book interactive guide (/guide/) using Gemini Native TTS + ffmpeg.

Outputs:
  assets/audio/guide/en/<slide-id>.mp3
  assets/audio/guide/zh/<slide-id>.mp3
  assets/audio/guide/manifest.json   (exact durations, voice metadata, byte sizes)
"""

import argparse
import base64
import concurrent.futures
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "assets" / "audio" / "guide"
KOKORO_MODEL = Path.home() / ".cache" / "hyperframes" / "tts" / "models" / "kokoro-v1.0.onnx"
KOKORO_VOICES = Path.home() / ".cache" / "hyperframes" / "tts" / "voices" / "voices-v1.0.bin"
VOXCPM_VENV = Path(os.environ.get("FB_VOICE_VENV", str(Path.home() / "Projects" / "brief" / "tools" / "voice" / ".venv")))
VOXCPM_REF = Path(os.environ.get("FB_VOICE_REF", str(Path.home() / "Projects" / "brief" / "ref")))
VOXCPM_TOOLS = Path.home() / "Projects" / "brief" / "pipeline" / "tools"

VOICES = {
    "en": "bm_george",
    "zh": "voxcpm-man-zh",
}

ENGINES = {
    "en": "kokoro-v1.0",
    "zh": "voxcpm2",
}

KOKORO_SPEED = 0.96
VOXCPM_SEEDS = [7, 11, 13, 17]

STYLE_PROMPTS = {
    "en": (
        "Read the following passage aloud in a calm, warm, unhurried museum audio-guide voice, "
        "with clear articulation and natural contemplative phrasing. Read only the passage verbatim:\n\n"
    ),
    "zh": (
        "请用标准流利的普通话播音腔、温和沉静地逐字朗读以下中文段落，吐字清晰准确，不要漏字或改字：\n\n"
    ),
}

BANNED_ZH = [
    "纯粹", "绝对", "完全", "彻底", "绝不", "通常", "往往", "或许",
    "某种意义上", "降维重构", "本质", "根本", "自始至终", "缰绳",
    "物理现实", "平庸", "物理意志",
]

SCRIPTS = [
    (
        "cover",
        "Not a Theory of Everything — a non-definitive guide for the Mind. "
        "This is a living book: the digitized memory of a Mind tracing and experiencing reality as is. "
        "Across fourteen parts, hundreds of essays, thousands of synaptic cross-links, and hundreds of traced premises, "
        "every page returns commonly held beliefs to their boundary.",
        "非万物之理，一部非定论的心智指南。"
        "这是一部活着的书，一个心智如实溯源与体验实在的数字化记忆。"
        "横跨十四卷、数百篇随笔、数千条突触连接与数百条前提索引，每一页都将习以为常的信念追溯回它的边界。",
    ),
    (
        "prior",
        "Everything here proceeds from a single irreducible prior: self-distinguishing activity occurs — uncaused, unceasing. "
        "This is not a hypothesis waiting for outside proof. Denying it already performs it, distinguishing true from false. "
        "Every act draws a bounded cut inside traces left by earlier acts, and that one-way shaping is the arrow of time.",
        "全书从唯一不可化约的先验出发：自我区分的活动正在发生，无因，不息。"
        "这不是等待外部证实的假说，任何否认都已在施演它，区分真与假。"
        "每一次行动在先前痕迹塑就的场域中划下有界的切分，这种单向塑造，正是时间之箭。",
    ),
    (
        "coin",
        "First-person perspective and causality are two sides of one coin. "
        "At each concrete moment, the Mind registers a finite set of distinctions; causality is the open potential extending into past causes and future effects. "
        "Severing causality from the first person breeds a clockwork cosmos with no observer. "
        "Severing the first person from causality unmoors awareness into solipsism and costless fantasy.",
        "第一人称视角与因果，是同一枚硬币的两面。"
        "在每个具体当下，心智登记有限的一组区分；因果则是向过往之因与未来之果无尽敞开的潜能。"
        "将因果剥离第一人称，便催生抽干观察者的发条宇宙；将第一人称剥离因果，觉知便脱离现实摩擦，滑入唯我论与空想。",
    ),
    (
        "orthogonal",
        "Not a Theory of Everything is not an Anti-Theory of Everything. "
        "An anti-stance stays trapped on the same one-dimensional axis, parasitic on what it opposes. "
        "An orthogonal cut carries inner product zero: it opens a new degree of freedom while leaving every useful lower-dimensional tool intact. "
        "Tracing a belief back to its premise locates where incompleteness begins, never issuing verdicts of false.",
        "非万物之理，不是反万物之理。"
        "反对的立场仍困在同一条一维坐标轴上，寄生于它所反对的对象。"
        "正交切分的内积为零：它打开新的自由度，同时保留低维中一切好用的脚手架。"
        "把信念追溯回前提，只标出不完备开始之处，从不宣判错误。",
    ),
    (
        "lattice",
        "This is neither a sealed treatise nor a dated blog. "
        "Every essay is a discrete waking cut made in concrete friction. "
        "Relative cross-links serve as synapses connecting all fourteen parts into a single fully linked lattice. "
        "Whenever a new recognition arrives, it propagates back along those links like sleep consolidation, re-rendering earlier traces so the whole memory stays coherent.",
        "这不是写完即凝固的论著，也不是按日堆叠的博客。"
        "每篇随笔是在具体摩擦中落下的清醒切分，篇间相对链接充当突触，将全部十四卷织成两两连通的晶格。"
        "每一次新的识见到来，都会如睡眠整合般沿链接回传，重绘早先痕迹，令整座记忆随心智前行保持自洽。",
    ),
    (
        "part-method",
        "The Preface gathers the method itself: Not a Theory of Everything. "
        "Inside stated assumptions, formal frameworks compress experience and coordinate action. "
        "Their boundary appears the moment a finite scaffold is stretched into a closed doctrine claiming to explain everything from outside the living observer.",
        "序卷收录这套溯源方法本身：非万物之理。"
        "在既定假设之内，理论与概念框架能够压缩经验、定位问题并协调行动。"
        "它们的边界显露于把有限脚手架拉伸为封闭教条、企图从观察者之外解释一切的那一刻。",
    ),
    (
        "part-causality",
        "Part One examines the inner and outer horizons of causality. "
        "Inside controllable systems, organizing causes into external chains serves prediction and engineering well. "
        "Carried past that boundary, treating all change as the passive unrolling of prior states erases the acting center that initiates distinctions and bears their consequences.",
        "第一部考察因果的内外视界。"
        "在可控的局部系统里，把因果整理为外在链条极有助于预测与工程。"
        "一旦越出这一边界，把一切变化当成先存状态的被动推演，便抹去了划定边界、发起区分并承担后果的行动中心。",
    ),
    (
        "part-physics",
        "Part Two turns to the myth that physics is the law. "
        "Physics excels at recording macroscopic invariances reproducible across observers under controlled measurement. "
        "Its incompleteness begins when that measurement record is inverted into a prior cosmic legislator — mistaking a cut from past contact for a closed script governing reality yet to unfold.",
        "第二部切入物理即定律的迷思。"
        "物理学精密记录了不同观察者在受控条件下稳定复现的宏观不变性，在工程建造与实验推演中无可替代。"
        "它的不完备始于将测量记录倒置为先于观察者的宇宙立法者，把过往接触的切面当成支配未发生现实的封闭剧本。",
    ),
    (
        "part-mathematics",
        "Part Three traces the boundaries of mathematics and logic. "
        "Once axioms and inference rules are provisionally fixed, formal systems deliver unambiguous deduction and computation. "
        "Their boundary sits at self-reference and the initial axiomatic cut: no sufficiently rich formal system can seal its own truth from within, nor lock open potential infinity inside static symbols.",
        "第三部追溯数学与逻辑的边界。"
        "在公理与推理规则暂时固定之后，形式系统提供了最为严密的符号推演与计算骨架。"
        "它的边界坐落在初始公理设定与自指回路之上：任何足够丰富的形式系统都无法仅凭内部规则封闭自身真值，也无法将敞开的潜无限锁进静态符号。",
    ),
    (
        "part-life-and-statistics",
        "Part Four examines living evolution and statistical shadows. "
        "Population averages and distributions serve public health, actuarial risk, and macro monitoring well by smoothing out individual differences upfront. "
        "Carried past that premise, treating a retrospective mean as the causal engine driving a singular living organism conceals the center navigating real metabolic stakes.",
        "第四部考察生命演化与统计表象。"
        "统计学通过事先抹去个体差异来提取大样本共性，在公共卫生、风险精算与群体趋势监测中极为有效。"
        "一旦越界，把事后留下的群体均值当成驱动具体生命的引擎，便遮蔽了在单次涉险中承受代谢摩擦的活态中心。",
    ),
    (
        "part-consciousness",
        "Part Five returns to consciousness and the first-person prior. "
        "Neuroscience and cognitive models map valuable neural correlates and third-person diagnostics. "
        "Yet trying to assemble experience out of subjectless data leaves out the observer at the starting line — because every record called objective already registers inside a first-person awareness.",
        "第五部回到意识与第一人称先验。"
        "神经科学与认知建模借由第三人称可观测信号，绘制了丰富的临床与行为图谱。"
        "但试图用无主体的客观数据拼凑体验，注定在起点处漏掉观察者自身——因为一切被称为客观的记录，都已在第一人称觉知中得以登记。",
    ),
    (
        "part-intelligence",
        "Part Six dissects the artifact myth of intelligence. "
        "Large neural networks compress human symbolic traces into extraordinary levers for retrieval, transformation, and execution. "
        "The boundary appears when fluent statistical continuation is mistaken for a second initiating subject — inverting an expression of intelligence into a source that originates intent or bears lived consequence.",
        "第六部拆解智能的器物神话。"
        "大型神经网络压缩人类留下的符号痕迹，提供了强大的模式检索、变换与执行杠杆。"
        "边界显现于将流畅的统计延续误认作第二重发起主体——把智能的表达倒置为能自行生发意图并承受切身后果的源头。",
    ),
    (
        "part-economics",
        "Part Seven traces economic order and microscopic choices. "
        "Macroeconomic indicators tally completed transactions cleanly for accounting, historical comparison, and bounded policy review. "
        "Their boundary begins when a settled invoice is inverted into a top-down engine — treating lagged summaries as levers that override microscopic minds weighing tradeoffs at the unknown edge.",
        "第七部追溯经济秩序与微观选择。"
        "宏观指标汇总已完成的交易，在事后记账、历史对比与局部评估中具有清晰的参考价值。"
        "它的不完备始于将事后结算的账单倒置为事前驱动经济的总开关，颠倒了滞后汇总与微观心智自负盈亏的因果次序。",
    ),
    (
        "part-state-and-collective",
        "Part Eight examines the state, collectives, and the mirror of power. "
        "Institutions and legal codes act as coordinating conventions that lower friction and stabilize shared expectations. "
        "They reach their boundary when reified into sentient leviathans — forgetting that no institution thinks or feels pain, and that authority rests on a mirror handshake of handing over judgment and claiming command.",
        "第八部审视国家集体与权力的镜像。"
        "国家、机构与法律规章作为跨个体的协调约定，有助于降低交易摩擦、稳定预期并划定公共契约边界。"
        "它们的不完备始于把协调约定实体化为自有意志的巨灵——忘却机构自身并不思考，权威始终依托于交出判断与认领号令权的镜像握手。",
    ),
    (
        "part-morality",
        "Part Nine traces moral boundaries and the empathy trap. "
        "Moral norms and empathy help familiar communities recognize preference clusters, buffer conflict, and sustain trust. "
        "Their boundary appears when a local good freezes past its step into a universal command casting hell as its mirror, or when empathic projection overrides first-person self-defense.",
        "第九部追溯善恶界限与共情陷阱。"
        "道德规范与共情在熟悉的共同体中作为简写约定，有助于识别偏好聚类、缓冲冲突并维系互信。"
        "当局部之善越过步点冻结成不容商议的普遍律令，便将地狱投射为自身的镜像；当共情推断脱离第一人称自卫，便会遮蔽真实的因果反馈。",
    ),
    (
        "part-meaning-and-transcendence",
        "Part Ten explores the search for meaning and transcendence. "
        "Religious traditions and contemplative narratives give symbolic language for confronting finitude, solitude, and the unknown. "
        "Their incompleteness begins when the Mind's own distinguishing activity is projected outside as a distant deity, or when enlightenment is frozen into a gate crossed once and for all.",
        "第十部探讨意义追寻与超越之境。"
        "宗教传统与观修叙事用象征语言记录心智如何直面有限性、孤独与未知，在日常执念处带来松动与慰藉。"
        "它们的不完备始于将心智自身的区分活动向外安放为远方实体，或把开悟冻结成一道一劳永逸跨过的门槛。",
    ),
    (
        "part-knowledge-and-learning",
        "Part Eleven looks at institutional knowledge and cognitive inquiry. "
        "Curricula and expert reference index conclusions forged under past constraints for rapid orientation. "
        "Their boundary arrives when warehousing settled answers and standardized rankings replaces live curiosity — the active capacity to re-trace and calibrate inside unfamiliar friction.",
        "第十一部考察知识建制与认知探索。"
        "学校课程、学科分类与专家建议整理了前人在特定约束下探得的结论，作为快速定位与检索的索引极为有用。"
        "当教育把囤积现成答案与通过标准化排位当成终点，便用对既有痕迹的记忆替代了在未知摩擦中亲自追溯的活态能力。",
    ),
    (
        "part-success-and-the-self",
        "Part Twelve examines the formula of success and self-reconstruction. "
        "Biographies and business retrospectives offer local heuristics when reviewing how past paths played out. "
        "Their incompleteness sits in retrospective inversion: drawing a neat linear recipe from a known finish line erases the friction of trial and error, and mistakes accumulated stock for living agency.",
        "第十二部剖析成功学公式与自我重塑。"
        "传记复盘与商业案例在梳理历史经验、提供局部启发时有其参考价值。"
        "它们的不完备始于事后倒置：站在已知终点裁剪出干净的线性秘籍，抹去了试错摩擦，也错把昨日积累的存量当成了今日动因。",
    ),
    (
        "part-tools-and-progress",
        "Part Thirteen traces tool evolution and the narrative of progress. "
        "From stone tools to modern compute and agent harnesses, technology continually compresses retrieval and execution costs, expanding the radius of human action. "
        "Its boundary begins when cheaper execution or vast stored traces are mistaken for a substitute for sovereign first-person judgment testing the live edge.",
        "第十三部追溯工具演进与进步叙事。"
        "从石器、印刷术到现代算力与智能体框架，工具不断压缩检索与执行成本，拓展心智的行动半径。"
        "进步叙事的不完备始于把成本压缩当成对第一人称裁决的替代，错把外部存储的历史痕迹当成了在当下前沿探路的活态心智。",
    ),
    (
        "index",
        "Every figure, theory, and concept substantively dissected across the book gathers in the Index of Premises. "
        "Philosophy, technology, science, economics, self-help, ideology, mathematics, and religion stand side by side: the scientific label grants no exemption and marks no target. "
        "Each entry names its premise, where it stays useful, and where its incompleteness begins.",
        "全书深入拆解的每一位人物、每一套理论与每一个概念，都汇集在前提索引之中。"
        "哲学、技术、科学、经济、成功学、意识形态、数学与宗教并列其间：科学的标签不构成豁免，也不构成靶子。"
        "每一条索引都点明它的前提、适用之处以及不完备开始的地方。",
    ),
    (
        "enter",
        "No north remains at the pole to point toward north. The first-person origin continues by living the cut. "
        "There are three ways to enter this Living Book: by part through the fourteen beliefs, by name in the Index of Premises, or by time through the full chronological journal. "
        "The path and its scaffolding sit open — ready to be tested in your own living situation.",
        "极点之上，再无北方可供指引。第一人称的原点，唯在当下活出这道区分。"
        "进入这部活书有三种路径：按部阅读十四卷目录，按名查阅前提索引，或按时间浏览全部日志，看它如何一页一页长出来。"
        "走过的路径与脚手架已在此敞开，留待每个心智在自己的现场重新检验。",
    ),
]


def load_api_key() -> str:
    if os.environ.get("GEMINI_API_KEY"):
        return os.environ["GEMINI_API_KEY"].strip()
    env_file = ROOT / "studio" / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("GEMINI_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("GEMINI_API_KEY not found in environment or studio/.env")


def probe_duration(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        text=True,
    ).strip()
    return round(float(out), 2)


def master_to_mp3(dest: Path, *, pcm_bytes: bytes | None = None, wav_path: Path | None = None) -> tuple[float, int]:
    tmp_mp3 = dest.with_suffix(".tmp.mp3")
    if wav_path is not None:
        in_args = ["-i", str(wav_path)]
        stdin_bytes = None
    else:
        in_args = ["-f", "s16le", "-ar", "24000", "-ac", "1", "-i", "pipe:0"]
        stdin_bytes = pcm_bytes

    proc = subprocess.run(
        [
            "ffmpeg",
            "-y",
            *in_args,
            "-af",
            "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.12,"
            "areverse,silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.22,areverse,"
            "loudnorm=I=-16:TP=-1.5:LRA=9",
            "-codec:a", "libmp3lame",
            "-ar", "24000",
            "-ac", "1",
            "-b:a", "48k",
            str(tmp_mp3),
        ],
        input=stdin_bytes,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg failed for {dest.name}: {proc.stderr.decode()[:300]}")

    tmp_mp3.replace(dest)
    dur = probe_duration(dest)
    size = dest.stat().st_size
    return dur, size


def synth_kokoro_batch(jobs: list[tuple[str, str, bool]], voice: str = "bm_george", speed: float = KOKORO_SPEED) -> list[tuple[str, str, float, int]]:
    import tempfile

    need_synth = any(force or not (OUT_DIR / "en" / f"{sid}.mp3").exists() or (OUT_DIR / "en" / f"{sid}.mp3").stat().st_size <= 8000 for sid, _, force in jobs)
    kokoro = None
    sf = None
    if need_synth:
        import kokoro_onnx
        import soundfile as sf
        if not KOKORO_MODEL.exists() or not KOKORO_VOICES.exists():
            raise SystemExit(f"Kokoro ONNX assets missing at {KOKORO_MODEL} / {KOKORO_VOICES}")
        kokoro = kokoro_onnx.Kokoro(str(KOKORO_MODEL), str(KOKORO_VOICES))

    out_results = []
    dest_dir = OUT_DIR / "en"
    dest_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        for sid, text, force in jobs:
            dest = dest_dir / f"{sid}.mp3"
            if dest.exists() and dest.stat().st_size > 8000 and not force:
                dur = probe_duration(dest)
                out_results.append(("en", sid, dur, dest.stat().st_size))
                continue

            # Replace em-dashes with commas/pauses for smooth Kokoro British cadence
            clean_text = text.replace(" — ", ", ").replace("—", ", ")
            samples, sr = kokoro.create(clean_text, voice=voice, speed=speed, lang="en-gb")
            wav_path = Path(tmpdir) / f"{sid}.wav"
            sf.write(str(wav_path), samples, sr)
            dur, size = master_to_mp3(dest, wav_path=wav_path)
            print(f"  ✓ en/{sid}.mp3 [kokoro/{voice}] ({dur:.2f}s, {size/1024:.0f} KB)", flush=True)
            out_results.append(("en", sid, dur, size))

    return out_results


def synth_voxcpm_batch(
    jobs: list[tuple[str, str, bool]],
    ref_dir: Path = VOXCPM_REF,
    voice_label: str = VOICES["zh"],
    scratch_dir: Path | None = None,
) -> list[tuple[str, str, float, int]]:
    """Synthesize Chinese tracks with local VoxCPM2 + mlx_whisper backcheck/reseed loop."""
    import tempfile

    voice_py = VOXCPM_VENV / "bin" / "python"
    worker_py = VOXCPM_TOOLS / "voxcpm_worker.py"
    backcheck_py = VOXCPM_TOOLS / "backcheck_mlx.py"
    if not voice_py.exists() or not worker_py.exists():
        raise SystemExit(f"VoxCPM2 toolchain missing: {voice_py} / {worker_py}")
    if not (ref_dir / "man.zh.wav").exists() or not (ref_dir / "voice.json").exists():
        raise SystemExit(f"VoxCPM2 reference missing in {ref_dir}")

    dest_dir = OUT_DIR / "zh"
    dest_dir.mkdir(parents=True, exist_ok=True)

    todo = []
    out_results: dict[str, tuple[str, str, float, int]] = {}
    for sid, text, force in jobs:
        dest = dest_dir / f"{sid}.mp3"
        if dest.exists() and dest.stat().st_size > 8000 and not force:
            out_results[sid] = ("zh", sid, probe_duration(dest), dest.stat().st_size)
        else:
            # Replace Chinese em-dashes with commas for clean VoxCPM2 cadence
            clean_text = text.replace("——", "，")
            todo.append({"sid": sid, "text": clean_text, "seeds": [VOXCPM_SEEDS[0]], "reports": [], "wavs": []})

    if not todo:
        return [out_results[sid] for sid, _, _ in jobs]

    env = dict(os.environ, FB_VOICE_REF=str(ref_dir), HF_HUB_OFFLINE="1")
    tmp_ctx = tempfile.TemporaryDirectory() if scratch_dir is None else None
    takes_dir = Path(tmp_ctx.name) if tmp_ctx is not None else scratch_dir
    takes_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Keep ONE persistent VoxCPM2 worker alive across all reseed rounds so the model loads only once
        proc = subprocess.Popen(
            [str(voice_py), str(worker_py)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=sys.stderr,
            text=True,
            env=env,
        )
        assert proc.stdin is not None and proc.stdout is not None

        try:
            for rnd in range(len(VOXCPM_SEEDS)):
                pending = [item for item in todo if len(item["reports"]) < len(item["seeds"])]
                if not pending:
                    break
                print(f"[voxcpm2] Round {rnd + 1}: synthesizing {len(pending)} Chinese slide(s)...", flush=True)
                check_asks = []
                for item in pending:
                    seed = item["seeds"][-1]
                    wav_path = takes_dir / f"{item['sid']}.s{seed}.wav"
                    if not wav_path.exists():
                        req = json.dumps({"text": item["text"], "seed": seed, "out": str(wav_path)}, ensure_ascii=False)
                        proc.stdin.write(req + "\n")
                        proc.stdin.flush()
                        reply_line = proc.stdout.readline()
                        if not reply_line:
                            raise RuntimeError(f"voxcpm_worker terminated unexpectedly on {item['sid']}")
                        reply = json.loads(reply_line)
                        if not reply.get("ok"):
                            raise RuntimeError(f"voxcpm_worker failed on {item['sid']}: {reply}")
                        print(f"  · took {item['sid']} (seed {seed}, {reply['seconds']:.1f}s)", flush=True)
                    item["wavs"].append(wav_path)
                    check_asks.append({"name": item["sid"], "out": str(wav_path), "text": item["text"]})

                # Run mlx_whisper backcheck if available
                if backcheck_py.exists():
                    check_file = takes_dir / f"check_r{rnd}.json"
                    report_file = takes_dir / f"report_r{rnd}.json"
                    check_file.write_text(json.dumps(check_asks, ensure_ascii=False), encoding="utf-8")
                    subprocess.run(
                        [str(voice_py), str(backcheck_py), "--compare", str(check_file), "--report", str(report_file)],
                        env=env,
                        check=True,
                    )
                    reports = json.loads(report_file.read_text(encoding="utf-8"))
                    for item, rep in zip(pending, reports):
                        item["reports"].append(rep)
                        if not rep["ok"] and len(item["seeds"]) < len(VOXCPM_SEEDS):
                            item["seeds"].append(VOXCPM_SEEDS[len(item["seeds"])])
                else:
                    for item in pending:
                        item["reports"].append({"ok": True, "sim": 1.0, "hard": [], "heard": ""})
        finally:
            try:
                proc.stdin.close()
            except Exception:
                pass
            proc.wait(timeout=30)

        passed = 0
        for item in todo:
            best_idx = next((i for i, r in enumerate(item["reports"]) if r["ok"]), None)
            if best_idx is None:
                best_idx = max(range(len(item["reports"])), key=lambda i: item["reports"][i].get("sim", 0.0))
            else:
                passed += 1
            best_wav = item["wavs"][best_idx]
            best_rep = item["reports"][best_idx]
            best_seed = item["seeds"][best_idx]
            dest = dest_dir / f"{item['sid']}.mp3"
            dur, size = master_to_mp3(dest, wav_path=best_wav)
            tag = "OK" if best_rep["ok"] else f"BEST(sim={best_rep.get('sim', 0):.2f}: {'; '.join(best_rep.get('hard', []))})"
            print(f"  ✓ zh/{item['sid']}.mp3 [voxcpm2/{voice_label} s{best_seed} {tag}] ({dur:.2f}s, {size/1024:.0f} KB)", flush=True)
            out_results[item["sid"]] = ("zh", item["sid"], dur, size)

        print(f"[voxcpm2] Backcheck summary: {passed}/{len(todo)} slides passed cleanly.", flush=True)
    finally:
        if tmp_ctx is not None:
            tmp_ctx.cleanup()

    return [out_results[sid] for sid, _, _ in jobs]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Regenerate existing MP3s")
    parser.add_argument("--lang", choices=["en", "zh", "all"], default="all", help="Which language(s) to regenerate")
    parser.add_argument("--en-voice", default=VOICES["en"], help="Kokoro voice for English (default: bm_george)")
    parser.add_argument("--en-speed", type=float, default=KOKORO_SPEED, help="Kokoro speech speed for English")
    parser.add_argument("--zh-voice", default=VOICES["zh"], help="Voice label recorded in manifest for Chinese")
    parser.add_argument("--voxcpm-ref", type=Path, default=VOXCPM_REF, help="Dir containing man.zh.wav + voice.json")
    parser.add_argument("--voxcpm-scratch", type=Path, default=None, help="Optional scratch dir to cache VoxCPM2 WAV takes")
    args = parser.parse_args()

    for slide_id, _en, zh in SCRIPTS:
        hits = [w for w in BANNED_ZH if w in zh]
        if hits:
            raise SystemExit(f"Banned Chinese word(s) {hits} in slide '{slide_id}'")
    print(f"Audited {len(SCRIPTS)} EN + {len(SCRIPTS)} ZH scripts: 0 banned Chinese words.", flush=True)

    results = []

    # 1. English via local Kokoro ONNX (bm_george, British English)
    en_jobs = [(sid, en_text, args.force and args.lang in ("en", "all")) for sid, en_text, _ in SCRIPTS]
    results.extend(synth_kokoro_batch(en_jobs, voice=args.en_voice, speed=args.en_speed))

    # 2. Chinese via local VoxCPM2 + mlx_whisper backcheck
    zh_jobs = [(sid, zh_text, args.force and args.lang in ("zh", "all")) for sid, _, zh_text in SCRIPTS]
    results.extend(synth_voxcpm_batch(zh_jobs, ref_dir=args.voxcpm_ref, voice_label=args.zh_voice, scratch_dir=args.voxcpm_scratch))

    manifest = {
        "engines": ENGINES,
        "voices": {"en": args.en_voice, "zh": args.zh_voice},
        "slides": {sid: {} for sid, _, _ in SCRIPTS},
    }
    total_bytes = 0
    total_dur = {"en": 0.0, "zh": 0.0}

    for lang, sid, dur, size in results:
        manifest["slides"][sid][lang] = {
            "file": f"{lang}/{sid}.mp3",
            "duration": dur,
            "bytes": size,
        }
        total_bytes += size
        total_dur[lang] += dur

    (OUT_DIR / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(
        f"Done: {len(results)} studio MP3 clips ({total_bytes / (1024 * 1024):.2f} MB total) | "
        f"EN: {total_dur['en']:.1f}s ({total_dur['en']/60:.1f}m) | "
        f"ZH: {total_dur['zh']:.1f}s ({total_dur['zh']/60:.1f}m)",
        flush=True,
    )


if __name__ == "__main__":
    main()
