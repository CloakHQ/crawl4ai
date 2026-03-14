"""
CloakBrowser + Crawl4AI: stealth web crawling with source-level fingerprint patches.

CloakBrowser is a patched Chromium binary with fingerprint modifications compiled
into the C++ source. Unlike JS-injection stealth (playwright-stealth), the patches
survive any fingerprint check because the browser itself reports modified values.

Install: pip install cloakbrowser
GitHub:  https://github.com/CloakHQ/CloakBrowser

The binary auto-downloads on first run (~200MB, cached in ~/.cloakbrowser/).
"""

import asyncio

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig


async def main():
    # Step 1: Launch CloakBrowser with remote debugging enabled
    from cloakbrowser import launch_async

    browser = await launch_async(
        headless=True,
        args=["--remote-debugging-port=9222", "--remote-debugging-address=127.0.0.1"],
    )

    # Step 2: Connect Crawl4AI to the stealth browser via CDP
    async with AsyncWebCrawler(
        config=BrowserConfig(
            browser_mode="cdp",
            cdp_url="http://127.0.0.1:9222",
        )
    ) as crawler:
        result = await crawler.arun(
            url="https://example.com",
            config=CrawlerRunConfig(
                wait_until="domcontentloaded",
            ),
        )
        print("-" * 20)
        print(f"Status Code: {result.status_code}")
        print("-" * 20)
        print(f"Title: {result.metadata['title']}")
        print(f"Markdown length: {len(result.markdown)} chars")
        print("-" * 20)
        print(result.markdown[:500])

    await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
