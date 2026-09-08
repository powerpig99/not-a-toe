#!/usr/bin/env python3
"""
build_prompts.py - Prompt generator for NotebookLM Audio & Video Overviews.

Combines standard, unchanging generic base templates with post-specific content slots.
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
        'POST_CORE_SPIRIT': post_data['core_spirit_en'],
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
        'POST_CORE_SPIRIT': post_data['core_spirit_zh'],
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

if __name__ == '__main__':
    print("build_prompts.py module ready.")
