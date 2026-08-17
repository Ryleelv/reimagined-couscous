#!/usr/bin/env python3
"""Download authorized Coursera reading pages as PDFs and bilingual Markdown.

This tool does not bypass paywalls, DRM, or login. Run it with your own Coursera
account in an interactive browser, then it crawls reading/supplement pages that
are reachable from the supplied course URL.
"""
from __future__ import annotations

import argparse
import os
import re
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from playwright.sync_api import BrowserContext, Page
else:
    BrowserContext = Any
    Page = Any

DEFAULT_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")


def slugify(text: str, fallback: str) -> str:
    text = re.sub(r"\s+", "-", text.strip().lower())
    text = re.sub(r"[^a-z0-9\-\u4e00-\u9fff]+", "", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:90] or fallback


def clean_text_from_html(html: str) -> tuple[str, str]:
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg", "nav", "footer", "header"]):
        tag.decompose()

    title = ""
    if soup.title and soup.title.string:
        title = soup.title.string.split("|", 1)[0].strip()
    h1 = soup.find("h1")
    if h1 and h1.get_text(strip=True):
        title = h1.get_text(" ", strip=True)

    main = soup.find("main") or soup.find(attrs={"role": "main"}) or soup.body or soup
    lines: list[str] = []
    for node in main.find_all(["h1", "h2", "h3", "h4", "p", "li"], recursive=True):
        txt = node.get_text(" ", strip=True)
        if not txt or len(txt) < 2:
            continue
        prefix = ""
        if node.name in {"h1", "h2", "h3", "h4"}:
            prefix = "#" * int(node.name[1]) + " "
        elif node.name == "li":
            prefix = "- "
        lines.append(prefix + txt)
    return title, "\n\n".join(dict.fromkeys(lines))


def translate_to_chinese(text: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return ""
    import requests

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": DEFAULT_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Translate the user's course reading into clear Simplified Chinese. "
                        "Preserve headings and bullet structure. Do not add new facts."
                    ),
                },
                {"role": "user", "content": text[:45000]},
            ],
            "temperature": 0.2,
        },
        timeout=120,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


def wait_for_login(page: Page, url: str) -> None:
    page.goto(url, wait_until="domcontentloaded")
    print("If Coursera asks you to sign in, complete login in the browser window.")
    print("Press Enter here after the course page is visible and you are authorized...")
    input()


def collect_reading_links(context: BrowserContext, start_url: str, max_pages: int) -> list[str]:
    page = context.new_page()
    page.goto(start_url, wait_until="networkidle")
    parsed = urlparse(start_url)
    course_prefix = "/".join(parsed.path.split("/")[:3])
    seen: dict[str, None] = {}
    queue = [start_url]

    while queue and len(seen) < max_pages:
        url = queue.pop(0)
        if url in seen:
            continue
        page.goto(url, wait_until="networkidle")
        time.sleep(1)
        if "/supplement/" in url:
            seen[url] = None
        anchors = page.eval_on_selector_all("a[href]", "els => els.map(a => a.href)")
        for href in anchors:
            href = urljoin(url, href).split("#", 1)[0]
            p = urlparse(href)
            is_course_reading = (
                p.netloc.endswith("coursera.org")
                and p.path.startswith(course_prefix)
                and "/supplement/" in p.path
            )
            if is_course_reading:
                if href not in seen and href not in queue:
                    queue.append(href)
    page.close()
    return list(seen.keys())


def save_reading(context: BrowserContext, url: str, out_dir: Path, index: int, translate: bool) -> None:
    page = context.new_page()
    page.goto(url, wait_until="networkidle")
    time.sleep(1)
    title, markdown = clean_text_from_html(page.content())
    stem = f"{index:02d}-{slugify(title, 'reading')}"

    pdf_path = out_dir / "pdf-en" / f"{stem}.pdf"
    md_en_path = out_dir / "markdown-en" / f"{stem}.md"
    md_bi_path = out_dir / "markdown-bilingual" / f"{stem}.md"
    for path in [pdf_path.parent, md_en_path.parent, md_bi_path.parent]:
        path.mkdir(parents=True, exist_ok=True)

    page.emulate_media(media="screen")
    page.pdf(
        path=str(pdf_path),
        format="A4",
        print_background=True,
        margin={"top": "0.5in", "right": "0.5in", "bottom": "0.5in", "left": "0.5in"},
    )
    md_en_path.write_text(f"# {title}\n\nSource: {url}\n\n{markdown}\n", encoding="utf-8")

    zh = translate_to_chinese(markdown) if translate else ""
    if zh:
        md_bi_path.write_text(f"# {title}\n\nSource: {url}\n\n## English\n\n{markdown}\n\n## 中文\n\n{zh}\n", encoding="utf-8")
    else:
        md_bi_path.write_text(f"# {title}\n\nSource: {url}\n\n## English\n\n{markdown}\n\n## 中文\n\nSet OPENAI_API_KEY and rerun with --translate to generate this section.\n", encoding="utf-8")
    page.close()
    print(f"Saved {title}: {pdf_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Save authorized Coursera reading materials as PDFs and bilingual Markdown.")
    parser.add_argument("url", help="A Coursera course reading/supplement URL to start from")
    parser.add_argument("--out", default="coursera-readings", help="Output directory")
    parser.add_argument("--user-data-dir", default=".coursera-browser", help="Persistent browser profile for your Coursera login")
    parser.add_argument("--max-pages", type=int, default=200, help="Safety limit for crawled reading pages")
    parser.add_argument("--login", action="store_true", help="Open a visible browser and wait while you log in")
    parser.add_argument("--translate", action="store_true", help="Generate Simplified Chinese translations with OPENAI_API_KEY")
    args = parser.parse_args()

    out_dir = Path(args.out)
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(args.user_data_dir, headless=not args.login)
        try:
            if args.login:
                page = context.new_page()
                wait_for_login(page, args.url)
                page.close()
            links = collect_reading_links(context, args.url, args.max_pages)
            if not links:
                raise SystemExit("No Coursera /supplement/ reading links found. Make sure you are logged in and the URL is a reading page.")
            (out_dir / "manifest.txt").parent.mkdir(parents=True, exist_ok=True)
            (out_dir / "manifest.txt").write_text("\n".join(links) + "\n", encoding="utf-8")
            for i, link in enumerate(links, 1):
                save_reading(context, link, out_dir, i, args.translate)
        finally:
            context.close()


if __name__ == "__main__":
    main()
