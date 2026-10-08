import os
import mlx_whisper

def format_timestamp(seconds: float) -> str:
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"

def transcribe_to_srt(audio_path, output_srt, output_vtt):
    print(f"Transcribing {audio_path} with mlx-whisper turbo...")
    res = mlx_whisper.transcribe(
        audio_path,
        path_or_hf_repo="mlx-community/whisper-large-v3-turbo",
        word_timestamps=False
    )
    segments = res.get("segments", [])
    print(f"Detected {len(segments)} segments.")

    # Write SRT
    srt_lines = []
    vtt_lines = ["WEBVTT\n"]
    for i, seg in enumerate(segments, 1):
        start = seg["start"]
        end = seg["end"]
        text = seg["text"].strip()
        
        start_str_srt = format_timestamp(start)
        end_str_srt = format_timestamp(end)
        srt_lines.append(f"{i}\n{start_str_srt} --> {end_str_srt}\n{text}\n")
        
        start_str_vtt = start_str_srt.replace(",", ".")
        end_str_vtt = end_str_srt.replace(",", ".")
        vtt_lines.append(f"{i}\n{start_str_vtt} --> {end_str_vtt}\n{text}\n")
        
    with open(output_srt, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_lines))
    with open(output_vtt, "w", encoding="utf-8") as f:
        f.write("\n".join(vtt_lines))
        
    print(f"Saved SRT: {output_srt}")
    print(f"Saved VTT: {output_vtt}")

if __name__ == "__main__":
    os.makedirs("assets/audio", exist_ok=True)
    os.makedirs("assets/videos", exist_ok=True)
    
    # 1. Chinese
    transcribe_to_srt(
        "assets/audio/when-malfunction-is-scored-as-intelligence_zh_beijing_deepdive.mp3",
        "assets/videos/when-malfunction-is-scored-as-intelligence_zh.srt",
        "assets/videos/when-malfunction-is-scored-as-intelligence_zh.vtt"
    )
    
    # 2. English
    transcribe_to_srt(
        "assets/audio/when-malfunction-is-scored-as-intelligence_en_huberman_posh.mp3",
        "assets/videos/when-malfunction-is-scored-as-intelligence_en.srt",
        "assets/videos/when-malfunction-is-scored-as-intelligence_en.vtt"
    )
