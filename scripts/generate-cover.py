#!/usr/bin/env python3
"""
Not-a-ToE Standard Cover Image Generator
Uses local Qwen-Image-2.1 (7B DiT + Qwen3-VL 8B, bfloat16 on Apple Silicon MPS)
Default: Ultra-wide 21:9 aspect ratio (1344x576, ~0.77 MP, 30 steps, ~5 min on M4 Pro)
"""

import argparse
import os
import sys
from pathlib import Path

# Auto-reexec inside the dedicated Qwen-Image-2.1 virtualenv if not already active
VENV_PYTHON = "/Users/jingliang/.gemini/antigravity/scratch/qwen-image-2.1/.venv/bin/python"
if sys.executable != VENV_PYTHON and os.path.exists(VENV_PYTHON):
    os.execv(VENV_PYTHON, [VENV_PYTHON] + sys.argv)

import torch
from PIL import Image
from diffusers import QwenImage21Pipeline

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_COVERS_DIR = REPO_ROOT / "assets" / "covers"


def parse_args():
    parser = argparse.ArgumentParser(description="Generate Not-a-ToE 21:9 Cover Art via Qwen-Image-2.1")
    parser.add_argument(
        "slug",
        type=str,
        help="Post slug (e.g. 'all-that-can-be-spoken-is-the-product-of-the-unspeakable')",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default=None,
        help="Prompt description for cover image generation",
    )
    parser.add_argument(
        "--prompt-file",
        type=str,
        default=None,
        help="Path to text file containing prompt description",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=1344,
        help="Width in pixels (default: 1344, exact 21:9)",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=576,
        help="Height in pixels (default: 576, exact 21:9)",
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=30,
        help="Denoising steps (default: 30, ~5 min on M4 Pro)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility",
    )
    parser.add_argument(
        "--format",
        choices=["jpg", "png"],
        default="jpg",
        help="Output image format (default: jpg)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Custom output file path (default: assets/covers/<slug>.<format>)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Determine output path
    if args.output:
        out_path = Path(args.output).resolve()
    else:
        out_path = DEFAULT_COVERS_DIR / f"{args.slug}.{args.format}"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Read prompt
    if args.prompt_file:
        with open(args.prompt_file, "r", encoding="utf-8") as f:
            prompt = f.read().strip()
    elif args.prompt:
        prompt = args.prompt.strip()
    else:
        print("Error: Either --prompt or --prompt-file must be provided.", file=sys.stderr)
        sys.exit(1)

    # Determine device
    device = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")

    print("=== Not-a-ToE Cover Art Generation ===")
    print(f"Target Slug:  {args.slug}")
    print(f"Output File:  {out_path}")
    print(f"Aspect Ratio: 21:9 ({args.width}x{args.height})")
    print(f"Denoise Steps:{args.steps}")
    print(f"Device:       {device} (bfloat16)")
    print(f"Prompt:\n{prompt}\n")

    print("Loading Qwen-Image-2.1 pipeline...")
    pipe = QwenImage21Pipeline.from_pretrained(
        "Qwen/Qwen-Image-2.1",
        dtype=torch.bfloat16 if device in ("cuda", "mps") else torch.float32,
    )
    if device != "cpu":
        pipe.enable_model_cpu_offload(device=device)
    else:
        pipe = pipe.to(device)

    generator = torch.Generator(device=device if device != "mps" else "cpu").manual_seed(args.seed)

    print("Running diffusion...")
    output = pipe(
        prompt=prompt,
        width=args.width,
        height=args.height,
        num_inference_steps=args.steps,
        generator=generator,
    )
    img = output.images[0]

    # Convert RGBA to RGB if saving as JPEG
    if args.format == "jpg" or out_path.suffix.lower() in (".jpg", ".jpeg"):
        if img.mode != "RGB":
            # Composite over black background to match dark aesthetic
            background = Image.new("RGB", img.size, (0, 0, 0))
            if img.mode == "RGBA":
                background.paste(img, mask=img.split()[3])
            else:
                background.paste(img)
            img = background
        img.save(out_path, format="JPEG", quality=95, optimize=True)
    else:
        img.save(out_path, format="PNG", optimize=True)

    print(f"\n[OK] Cover art generated successfully: {out_path}")
    print(f"Dimensions: {img.width}x{img.height}, File size: {out_path.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
