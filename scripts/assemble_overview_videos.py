#!/usr/bin/env python3
"""
Assembles high-quality cinematic Video Overviews for Post #377 in Chinese and English.
Combines:
- 21:9 Cover Art (assets/covers/when-malfunction-is-scored-as-intelligence.jpg)
- 1:1 Infographics (assets/covers/when-malfunction-is-scored-as-intelligence_infographic_zh.jpg / en.jpg)
- Grok TTS Audio Deep Dives (assets/audio/when-malfunction-is-scored-as-intelligence_zh_beijing_deepdive.mp3 / en_huberman_posh.mp3)
- Embedded Subtitles generated via Whisper (assets/videos/when-malfunction-is-scored-as-intelligence_zh.srt / en.srt via MP4 mov_text stream)
"""

import os
import sys
import subprocess
import tempfile

def get_audio_duration(path: str) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", path
    ]
    out = subprocess.check_output(cmd, text=True).strip()
    return float(out)

def build_overview_video(lang: str):
    is_zh = (lang == "zh")
    audio_file = (
        "assets/audio/when-malfunction-is-scored-as-intelligence_zh_beijing_deepdive.mp3"
        if is_zh else
        "assets/audio/when-malfunction-is-scored-as-intelligence_en_huberman_posh.mp3"
    )
    srt_file = (
        "assets/videos/when-malfunction-is-scored-as-intelligence_zh.srt"
        if is_zh else
        "assets/videos/when-malfunction-is-scored-as-intelligence_en.srt"
    )
    infographic_file = (
        "assets/covers/when-malfunction-is-scored-as-intelligence_infographic_zh.jpg"
        if is_zh else
        "assets/covers/when-malfunction-is-scored-as-intelligence_infographic_en.jpg"
    )
    cover_file = "assets/covers/when-malfunction-is-scored-as-intelligence.jpg"
    out_video = (
        "assets/videos/when-malfunction-is-scored-as-intelligence_overview_zh.mp4"
        if is_zh else
        "assets/videos/when-malfunction-is-scored-as-intelligence_overview_en.mp4"
    )

    if not os.path.exists(audio_file):
        raise FileNotFoundError(f"Missing audio: {audio_file}")
    if not os.path.exists(srt_file):
        raise FileNotFoundError(f"Missing SRT: {srt_file}")

    total_dur = get_audio_duration(audio_file)
    print(f"\n==========================================")
    print(f"🎬 Assembling {lang.upper()} Overview Video")
    print(f"Total Duration: {total_dur:.2f}s ({total_dur/60:.2f} min)")
    print(f"Output: {out_video}")
    print(f"==========================================")

    # 4 distinct visual segments
    # Segment 1: Cover wide pan
    # Segment 2: Infographic upper half (sandbox vs crash)
    # Segment 3: Infographic lower half / chart details
    # Segment 4: Cover resolve
    d1 = total_dur * 0.22
    d2 = total_dur * 0.28
    d3 = total_dur * 0.28
    d4 = total_dur - (d1 + d2 + d3)

    # 1344x768 (16:9 cinematic landscape)
    width, height = 1344, 768

    with tempfile.TemporaryDirectory() as tmpdir:
        seg1 = os.path.join(tmpdir, "seg1.mp4")
        seg2 = os.path.join(tmpdir, "seg2.mp4")
        seg3 = os.path.join(tmpdir, "seg3.mp4")
        seg4 = os.path.join(tmpdir, "seg4.mp4")

        # Seg 1: Cover art slow zoom-in & rightward drift
        f1 = f"scale=2688:1152,zoompan=z='min(zoom+0.0004,1.25)':x='iw*0.1+iw*0.2*(on/{int(d1*24)})':y='ih/2-(ih/zoom/2)':d={int(d1*24)}:s={width}x{height}:fps=24"
        subprocess.run([
            "ffmpeg", "-y", "-loop", "1", "-i", cover_file,
            "-vf", f1, "-t", str(d1),
            "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", seg1
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✓ Segment 1 rendered")

        # Seg 2: Infographic slow zoom on core conceptual architecture
        f2 = f"scale=1536:1536,zoompan=z='min(zoom+0.0003,1.2)':x='iw/2-(iw/zoom/2)':y='ih*0.2':d={int(d2*24)}:s={width}x{height}:fps=24"
        subprocess.run([
            "ffmpeg", "-y", "-loop", "1", "-i", infographic_file,
            "-vf", f2, "-t", str(d2),
            "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", seg2
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✓ Segment 2 rendered")

        # Seg 3: Infographic pan down to physical collision & fleet miles
        f3 = f"scale=1536:1536,zoompan=z='1.2':x='iw/2-(iw/zoom/2)':y='ih*0.2+ih*0.4*(on/{int(d3*24)})':d={int(d3*24)}:s={width}x{height}:fps=24"
        subprocess.run([
            "ffmpeg", "-y", "-loop", "1", "-i", infographic_file,
            "-vf", f3, "-t", str(d3),
            "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", seg3
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✓ Segment 3 rendered")

        # Seg 4: Cover resolve, slow zoom-out
        f4 = f"scale=2688:1152,zoompan=z='max(1.2-0.0003*(on/{int(d4*24)}),1.0)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={int(d4*24)}:s={width}x{height}:fps=24"
        subprocess.run([
            "ffmpeg", "-y", "-loop", "1", "-i", cover_file,
            "-vf", f4, "-t", str(d4),
            "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", seg4
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✓ Segment 4 rendered")

        # Concat segments
        concat_txt = os.path.join(tmpdir, "concat.txt")
        with open(concat_txt, "w") as f:
            for s in [seg1, seg2, seg3, seg4]:
                f.write(f"file '{s}'\n")

        merged_v = os.path.join(tmpdir, "merged.mp4")
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", concat_txt, "-c", "copy", merged_v
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✓ Video stream concatenated")

        # Final mux with Audio and Embedded Subtitles Track (mov_text)
        print("Final Composite: embedding subtitles track and muxing audio...")
        lang_code = "chi" if is_zh else "eng"
        track_title = "中文字幕" if is_zh else "English Subtitles"
        
        cmd = [
            "ffmpeg", "-y",
            "-i", merged_v,
            "-i", audio_file,
            "-i", srt_file,
            "-map", "0:v",
            "-map", "1:a",
            "-map", "2:s",
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            "-c:s", "mov_text",
            "-metadata:s:s:0", f"language={lang_code}",
            "-metadata:s:s:0", f"title={track_title}",
            "-shortest",
            out_video
        ]
        subprocess.run(cmd, check=True)
        print(f"🎉 Successfully Generated Video Overview: {out_video}")

if __name__ == "__main__":
    lang = sys.argv[1] if len(sys.argv) > 1 else "zh"
    build_overview_video(lang)
