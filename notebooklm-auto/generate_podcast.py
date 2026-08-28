#!/usr/bin/env python3
"""
NotebookLM Audio Overview Generator (Playwright + Brave CDP)

Automates Google NotebookLM Audio Overview generation from local markdown essays:
1. Connects to running Brave Browser via Chrome DevTools Protocol (CDP: 9222)
2. Reuses existing authenticated Google session
3. Creates new notebook, uploads copied markdown source
4. Injects custom podcast instructions
5. Triggers generation, monitors progress, and downloads output MP3
"""

import argparse
import asyncio
import os
import sys
import time
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

DEFAULT_CDP_URL = "http://localhost:9222"
DEFAULT_SOURCE = "./input/essay.md"
DEFAULT_PROMPT = "./prompt_template.txt"
DEFAULT_OUTPUT = "./output/episode.mp3"
LOG_DIR = Path("./logs")


def log(msg: str):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}", flush=True)


async def find_element_with_fallbacks(page, selectors, description="element", timeout=5000):
    for sel in selectors:
        try:
            elem = page.locator(sel).first
            if await elem.is_visible(timeout=timeout):
                return elem
        except Exception:
            continue
    return None


async def click_with_fallbacks(page, selectors, description="element", timeout=8000):
    for sel in selectors:
        try:
            elem = page.locator(sel).first
            if await elem.is_visible(timeout=timeout):
                await elem.click()
                log(f"Clicked {description} using selector: {sel}")
                return True
        except Exception:
            continue
    raise RuntimeError(f"Could not find or click {description}. Tried selectors: {selectors}")


async def generate_podcast(source_path: str, prompt_path: str, output_path: str, cdp_url: str, timeout_mins: int = 15):
    source_file = Path(source_path).resolve()
    prompt_file = Path(prompt_path).resolve()
    output_file = Path(output_path).resolve()

    if not source_file.is_file():
        raise FileNotFoundError(f"Source markdown file not found at: {source_file}")
    if not prompt_file.is_file():
        raise FileNotFoundError(f"Prompt template file not found at: {prompt_file}")

    output_file.parent.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    source_content = source_file.read_text(encoding="utf-8")
    prompt_content = prompt_file.read_text(encoding="utf-8")
    doc_title = source_file.stem

    log(f"Source file: {source_file} ({len(source_content)} chars)")
    log(f"Prompt file: {prompt_file} ({len(prompt_content)} chars)")
    log(f"Output destination: {output_file}")
    log(f"Connecting to Brave via CDP at {cdp_url}...")

    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp(cdp_url)
        except Exception as e:
            log(f"ERROR: Failed to connect to Brave CDP at {cdp_url}: {e}")
            log("Make sure Brave is running with --remote-debugging-port=9222")
            sys.exit(1)

        contexts = browser.contexts
        if not contexts:
            log("No browser context found, creating one...")
            context = await browser.new_context()
        else:
            context = contexts[0]

        page = await context.new_page()
        # Set large viewport for reliable element visibility
        await page.set_viewport_size({"width": 1440, "height": 900})

        try:
            log("Navigating to https://notebooklm.google.com/ ...")
            await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(3000)

            # Check if redirected to login
            if "accounts.google.com" in page.url:
                log("WARNING: Redirected to Google login page. Please log in to Google in your Brave Browser first.")
                await page.screenshot(path=str(LOG_DIR / "login_required.png"))
                sys.exit(1)

            log("NotebookLM home loaded. Creating a new notebook...")

            # 1. Click "New notebook" / "新建笔记本"
            new_notebook_selectors = [
                'button:has-text("New notebook")',
                'button:has-text("新建笔记本")',
                'button:has-text("Create new")',
                'button:has-text("新建")',
                '[aria-label*="Create notebook"]',
                '[aria-label*="New notebook"]',
                '[aria-label*="新建笔记本"]',
                '.create-notebook-button',
                'mat-card.create-new'
            ]
            await click_with_fallbacks(page, new_notebook_selectors, description="New Notebook button", timeout=12000)
            await page.wait_for_timeout(4000)

            log(f"Entered notebook view: {page.url}")

            # 2. Add source: select "Copied text" / "粘贴的文本"
            log("Selecting 'Copied text' source type...")
            copied_text_selectors = [
                'button:has-text("Copied text")',
                'button:has-text("粘贴的文本")',
                '[aria-label*="Copied text"]',
                '[aria-label*="粘贴的文本"]',
                'div[role="button"]:has-text("Copied text")',
                'div[role="button"]:has-text("粘贴的文本")',
                'div:has-text("Copied text")',
                'div:has-text("粘贴的文本")'
            ]
            await click_with_fallbacks(page, copied_text_selectors, description="Copied text source option", timeout=12000)
            await page.wait_for_timeout(2000)

            # 3. Paste source text and title
            log("Pasting essay content into text source...")
            # Look for textarea or contenteditable editor
            text_area_selectors = [
                'textarea[placeholder*="Paste"]',
                'textarea[placeholder*="粘贴"]',
                'textarea[aria-label*="Source text"]',
                'textarea',
                'div[contenteditable="true"]'
            ]
            text_input = await find_element_with_fallbacks(page, text_area_selectors, description="Text source input", timeout=8000)
            if not text_input:
                raise RuntimeError("Could not find textarea to paste source content")

            await text_input.fill(source_content)
            await page.wait_for_timeout(1000)

            # Optional: fill title input if present
            title_selectors = [
                'input[placeholder*="Title"]',
                'input[placeholder*="标题"]',
                'input[aria-label*="Title"]',
                'input[aria-label*="标题"]'
            ]
            title_input = await find_element_with_fallbacks(page, title_selectors, description="Source title input", timeout=2000)
            if title_input:
                try:
                    await title_input.fill(doc_title)
                    log(f"Set source title to '{doc_title}'")
                except Exception:
                    pass

            # Click "Insert" / "插入" / "Save"
            insert_btn_selectors = [
                'button:has-text("Insert")',
                'button:has-text("插入")',
                'button:has-text("Save")',
                'button:has-text("保存")',
                'button:has-text("Done")',
                'button:has-text("完成")',
                'button[type="submit"]'
            ]
            await click_with_fallbacks(page, insert_btn_selectors, description="Insert source button", timeout=8000)
            log("Source inserted. Waiting for source indexing to complete...")
            await page.wait_for_timeout(5000)

            # 4. In the Audio Overview section, click "Customize" / "自定义"
            log("Locating Audio Overview 'Customize' button...")
            customize_selectors = [
                'button:has-text("Customize")',
                'button:has-text("自定义")',
                '[aria-label*="Customize"]',
                '[aria-label*="自定义"]',
                'div[role="button"]:has-text("Customize")',
                'div[role="button"]:has-text("自定义")'
            ]
            
            # Ensure Guide / Studio panel is open if needed
            guide_panel_btn = await find_element_with_fallbacks(page, ['button:has-text("Notebook guide")', 'button:has-text("笔记本指南")', 'button:has-text("Studio")'], timeout=2000)
            if guide_panel_btn:
                try:
                    await guide_panel_btn.click()
                    await page.wait_for_timeout(1500)
                except Exception:
                    pass

            await click_with_fallbacks(page, customize_selectors, description="Customize Audio Overview button", timeout=12000)
            await page.wait_for_timeout(2000)

            # 5. Fill custom instructions prompt
            log("Filling custom prompt instructions...")
            prompt_input_selectors = [
                'textarea[placeholder*="focus"]',
                'textarea[placeholder*="instructions"]',
                'textarea[placeholder*="关注"]',
                'textarea[placeholder*="提示"]',
                'textarea'
            ]
            prompt_input = await find_element_with_fallbacks(page, prompt_input_selectors, description="Customize instructions textarea", timeout=8000)
            if not prompt_input:
                raise RuntimeError("Could not find textarea to input podcast prompt template")

            await prompt_input.fill(prompt_content)
            await page.wait_for_timeout(1000)

            # Click "Save" / "保存" in the customize modal
            save_custom_selectors = [
                'button:has-text("Save")',
                'button:has-text("保存")',
                'button:has-text("Done")',
                'button:has-text("完成")',
                'button:has-text("Confirm")',
                'button:has-text("确定")'
            ]
            await click_with_fallbacks(page, save_custom_selectors, description="Save customize modal button", timeout=8000)
            await page.wait_for_timeout(2000)
            log("Custom prompt saved successfully.")

            # 6. Click "Generate" / "生成"
            log("Clicking 'Generate' Audio Overview button...")
            generate_selectors = [
                'button:has-text("Generate")',
                'button:has-text("生成")',
                '[aria-label*="Generate"]',
                '[aria-label*="生成"]'
            ]
            await click_with_fallbacks(page, generate_selectors, description="Generate audio button", timeout=10000)
            log("Audio Overview generation triggered!")

            # 7. Poll for completion
            log(f"Monitoring generation progress (timeout: {timeout_mins} minutes)...")
            start_time = time.time()
            max_seconds = timeout_mins * 60
            poll_interval = 15

            play_selectors = [
                'button:has-text("Play")',
                'button:has-text("播放")',
                '[aria-label*="Play"]',
                '[aria-label*="播放"]',
                'button[aria-label*="play" i]',
                'mat-icon:has-text("play_arrow")'
            ]

            generating_selectors = [
                ':has-text("Generating...")',
                ':has-text("正在生成...")',
                ':has-text("Generating audio")',
                ':has-text("正在生成音频")',
                'button:has-text("Cancel")',
                'button:has-text("取消")'
            ]

            while True:
                elapsed = int(time.time() - start_time)
                if elapsed > max_seconds:
                    await page.screenshot(path=str(LOG_DIR / "generation_timeout.png"))
                    raise TimeoutError(f"Audio generation exceeded {timeout_mins} minutes timeout.")

                # Check if Play button or audio player is ready
                play_btn = await find_element_with_fallbacks(page, play_selectors, timeout=1000)
                is_generating = False
                for g_sel in generating_selectors:
                    try:
                        if await page.locator(g_sel).first.is_visible(timeout=500):
                            is_generating = True
                            break
                    except Exception:
                        pass

                if play_btn and not is_generating:
                    log(f"Audio Overview generation completed in {elapsed // 60}m {elapsed % 60}s!")
                    break

                log(f"Still generating... ({elapsed // 60}m {elapsed % 60}s elapsed)")
                await page.wait_for_timeout(poll_interval * 1000)

            # 8. Open options menu and download MP3
            log("Opening audio options menu to download MP3...")
            menu_selectors = [
                'button[aria-label*="More options"]',
                'button[aria-label*="更多选项"]',
                'button:has-text("more_vert")',
                'mat-icon:has-text("more_vert")',
                '[data-test-id*="audio-menu"]',
                'button[aria-label*="Audio menu"]',
                'button[aria-label*="音频菜单"]'
            ]
            await click_with_fallbacks(page, menu_selectors, description="Audio more options menu", timeout=10000)
            await page.wait_for_timeout(1500)

            download_menu_selectors = [
                'div[role="menuitem"]:has-text("Download")',
                'div[role="menuitem"]:has-text("下载")',
                'button:has-text("Download")',
                'button:has-text("下载")',
                '[aria-label*="Download"]',
                '[aria-label*="下载"]'
            ]

            log("Triggering download...")
            async with page.expect_download(timeout=30000) as download_info:
                await click_with_fallbacks(page, download_menu_selectors, description="Download option", timeout=8000)

            download = await download_info.value
            await download.save_as(str(output_file))
            log(f"SUCCESS! Podcast audio saved to: {output_file} ({output_file.stat().st_size // 1024} KB)")

        except Exception as err:
            log(f"ERROR encountered: {err}")
            screenshot_path = LOG_DIR / "error_state.png"
            try:
                await page.screenshot(path=str(screenshot_path))
                log(f"Debug screenshot saved to {screenshot_path}")
            except Exception:
                pass
            raise
        finally:
            try:
                await page.close()
            except Exception:
                pass


def main():
    parser = argparse.ArgumentParser(description="Generate NotebookLM Audio Overview from Markdown essay")
    parser.add_argument("--source", default=DEFAULT_SOURCE, help=f"Path to input markdown file (default: {DEFAULT_SOURCE})")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help=f"Path to prompt template file (default: {DEFAULT_PROMPT})")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help=f"Path to destination mp3 file (default: {DEFAULT_OUTPUT})")
    parser.add_argument("--cdp-url", default=DEFAULT_CDP_URL, help=f"Brave CDP URL (default: {DEFAULT_CDP_URL})")
    parser.add_argument("--timeout-mins", type=int, default=15, help="Generation timeout in minutes (default: 15)")

    args = parser.parse_args()
    asyncio.run(generate_podcast(
        source_path=args.source,
        prompt_path=args.prompt,
        output_path=args.output,
        cdp_url=args.cdp_url,
        timeout_mins=args.timeout_mins
    ))


if __name__ == "__main__":
    main()
