#!/usr/bin/env python3
"""
NotebookLM Audio Overview Generator (Playwright + Brave CDP)

Automates Google NotebookLM Audio Overview generation from live blog URLs or local Markdown:
1. Connects to running Brave Browser via Chrome DevTools Protocol (CDP: 9222)
2. Reuses existing authenticated Google session
3. Creates new notebook, imports Website Link or copied Markdown source
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


async def generate_podcast(
    source_path: str = None,
    source_url: str = None,
    prompt_path: str = DEFAULT_PROMPT,
    output_path: str = DEFAULT_OUTPUT,
    cdp_url: str = DEFAULT_CDP_URL,
    timeout_mins: int = 15
):
    prompt_file = Path(prompt_path).resolve()
    output_file = Path(output_path).resolve()

    if not prompt_file.is_file():
        raise FileNotFoundError(f"Prompt template file not found at: {prompt_file}")

    output_file.parent.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    prompt_content = prompt_file.read_text(encoding="utf-8")

    if source_url:
        log(f"Source mode: Web URL -> {source_url}")
        doc_title = source_url.rstrip("/").split("/")[-1]
    elif source_path:
        source_file = Path(source_path).resolve()
        if not source_file.is_file():
            raise FileNotFoundError(f"Source file not found at: {source_file}")
        source_content = source_file.read_text(encoding="utf-8")
        doc_title = source_file.stem
        log(f"Source mode: Local File -> {source_file} ({len(source_content)} chars)")
    else:
        raise ValueError("Either --url or --source must be specified.")

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

            # 1. Click "New notebook" / "新建笔记本" / "Create new"
            new_notebook_selectors = [
                'button:has-text("Create new")',
                'button:has-text("New notebook")',
                'button:has-text("新建笔记本")',
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

            # 2. Add source: Website URL or Copied Text
            if source_url:
                log(f"Selecting 'Website' / 'Link' source option for URL: {source_url}...")
                website_selectors = [
                    'button:has-text("Website")',
                    'button:has-text("Link")',
                    'button:has-text("网站")',
                    'button:has-text("网页")',
                    'button:has-text("Web page")',
                    '[aria-label*="Website"]',
                    '[aria-label*="Link"]',
                    'div[role="button"]:has-text("Website")',
                    'div[role="button"]:has-text("Link")',
                    'div:has-text("Website")',
                    'div:has-text("Link")'
                ]
                await click_with_fallbacks(page, website_selectors, description="Website / Link source option", timeout=12000)
                await page.wait_for_timeout(2000)

                url_input_selectors = [
                    'input[type="url"]',
                    'input[placeholder*="http"]',
                    'input[placeholder*="URL"]',
                    'input[placeholder*="网址"]',
                    'input[placeholder*="链接"]',
                    'input[type="text"]'
                ]
                url_input = await find_element_with_fallbacks(page, url_input_selectors, description="Website URL input", timeout=8000)
                if not url_input:
                    raise RuntimeError("Could not find URL input field in Website source dialog")

                await url_input.fill(source_url)
                await page.wait_for_timeout(1000)

                insert_btn_selectors = [
                    'button:has-text("Insert")',
                    'button:has-text("插入")',
                    'button:has-text("Save")',
                    'button:has-text("保存")',
                    'button:has-text("Done")',
                    'button:has-text("完成")',
                    'button[type="submit"]'
                ]
                await click_with_fallbacks(page, insert_btn_selectors, description="Insert URL source button", timeout=8000)
                log("URL submitted. Waiting for page crawling and source indexing...")
                await page.wait_for_timeout(8000)

            else:
                log("Selecting 'Copied text' source type...")
                copied_text_selectors = [
                    'button:has-text("Copied text")',
                    'button:has-text("粘贴的文本")',
                    '[aria-label*="Copied text"]',
                    '[aria-label*="粘贴的文本"]',
                    'div[role="button"]:has-text("Copied text")',
                    'div[role="button"]:has-text("粘贴的文本")'
                ]
                await click_with_fallbacks(page, copied_text_selectors, description="Copied text source option", timeout=12000)
                await page.wait_for_timeout(2000)

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
                log("Source inserted. Waiting for source indexing...")
                await page.wait_for_timeout(6000)

            # 3. Close any open dialog/overlay before interacting with Studio
            close_btn_selectors = [
                'button[aria-label="Close"]',
                'button[aria-label="关闭"]',
                'button:has-text("Done")',
                'button:has-text("完成")',
                'mat-icon:has-text("close")'
            ]
            close_btn = await find_element_with_fallbacks(page, close_btn_selectors, timeout=1500)
            if close_btn:
                try:
                    await close_btn.click()
                    await page.wait_for_timeout(1000)
                except Exception:
                    pass

            # 4. Click "Audio Overview" card in Studio panel
            log("Clicking 'Audio Overview' card in Studio panel...")
            audio_overview_card_selectors = [
                '.studio-card:has-text("Audio Overview")',
                '.studio-card:has-text("音频概览")',
                '[role="button"]:has-text("Audio Overview")',
                '[role="button"]:has-text("音频概览")',
                'div:has-text("Audio Overview")',
                'div:has-text("音频概览")',
                'button:has-text("Audio Overview")',
                'button:has-text("音频概览")'
            ]
            await click_with_fallbacks(page, audio_overview_card_selectors, description="Studio Audio Overview card", timeout=12000)
            await page.wait_for_timeout(2000)

            # 5. Fill custom prompt instructions in the Customize Audio Overview modal
            log("Filling custom prompt instructions in Customize Audio Overview modal...")
            prompt_input_selectors = [
                'textarea[placeholder*="focus"]',
                'textarea[placeholder*="instructions"]',
                'textarea[placeholder*="关注"]',
                'textarea[placeholder*="提示"]',
                'textarea[aria-label*="instructions"]',
                'textarea'
            ]
            prompt_input = await find_element_with_fallbacks(page, prompt_input_selectors, description="Customize instructions textarea", timeout=8000)
            if not prompt_input:
                raise RuntimeError("Could not find textarea to input podcast prompt template")

            await prompt_input.fill(prompt_content)
            await page.wait_for_timeout(1000)

            # 6. Click "Generate" button in the modal
            log("Clicking 'Generate' button in modal...")
            generate_selectors = [
                'button:has-text("Generate")',
                'button:has-text("生成")',
                '[aria-label*="Generate"]',
                '[aria-label*="生成"]',
                'button:has-text("Create")',
                'button:has-text("创建")'
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

            quota_error_selectors = [
                ':has-text("limit reached")',
                ':has-text("quota exceeded")',
                ':has-text("try again tomorrow")',
                ':has-text("达到上限")'
            ]

            while True:
                elapsed = int(time.time() - start_time)
                if elapsed > max_seconds:
                    await page.screenshot(path=str(LOG_DIR / "generation_timeout.png"))
                    raise TimeoutError(f"Audio generation exceeded {timeout_mins} minutes timeout.")

                # Check if quota limit reached
                for q_sel in quota_error_selectors:
                    try:
                        if await page.locator(q_sel).first.is_visible(timeout=500):
                            log("WARNING: Daily Audio Overview limit appears to be reached.")
                            await page.screenshot(path=str(LOG_DIR / "quota_limit.png"))
                            return
                    except Exception:
                        pass

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
    parser = argparse.ArgumentParser(description="Generate NotebookLM Audio Overview from Web URL or Markdown")
    parser.add_argument("--url", default=None, help="Direct website URL of the blog post to index")
    parser.add_argument("--source", default=None, help="Path to input markdown file")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help=f"Path to prompt template file (default: {DEFAULT_PROMPT})")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help=f"Path to destination mp3 file (default: {DEFAULT_OUTPUT})")
    parser.add_argument("--cdp-url", default=DEFAULT_CDP_URL, help=f"Brave CDP URL (default: {DEFAULT_CDP_URL})")
    parser.add_argument("--timeout-mins", type=int, default=15, help="Generation timeout in minutes (default: 15)")

    args = parser.parse_args()
    asyncio.run(generate_podcast(
        source_path=args.source,
        source_url=args.url,
        prompt_path=args.prompt,
        output_path=args.output,
        cdp_url=args.cdp_url,
        timeout_mins=args.timeout_mins
    ))


if __name__ == "__main__":
    main()
