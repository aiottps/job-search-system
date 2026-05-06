import asyncio
import random
from playwright.async_api import async_playwright, Page, Locator
from typing import Optional, Callable, Any
from app.utils.logger import logger

class PlaywrightBrowser:
    """Async context manager for Playwright browser and context."""
    def __init__(self, headless: bool = True, timeout: int = 15000):
        self.headless = headless
        self.timeout = timeout
        self.playwright = None
        self.browser = None
        self.context = None

    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        self.context.set_default_timeout(self.timeout)
        return self.context

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

async def random_delay(min_seconds: float = 1.5, max_seconds: float = 4.0):
    """Polite delay for rate limiting between public page requests."""
    delay = random.uniform(min_seconds, max_seconds)
    await asyncio.sleep(delay)

async def retry_async(func: Callable, retries: int = 2, delay_seconds: float = 2.0) -> Any:
    """Retries an async function for network or timeout errors."""
    last_err = None
    for i in range(retries + 1):
        try:
            return await func()
        except (asyncio.TimeoutError, Exception) as e:
            # Note: Do not retry on logic blocks (CAPTCHA/Login) handled separately
            last_err = e
            if i < retries:
                logger.warning(f"Retry {i+1}/{retries} after error: {e}")
                await asyncio.sleep(delay_seconds)
            else:
                logger.error(f"Max retries reached. Error: {e}")
                raise last_err

async def detect_blocking_or_login(page: Page) -> Optional[str]:
    """Detects if the page is blocked by CAPTCHA, login wall, or bot detection."""
    content = await page.content()
    block_keywords = [
        "CAPTCHA", "驗證", "機器人", "登入", "login", "sign in", 
        "human verification", "安全驗證", "異常流量"
    ]
    for kw in block_keywords:
        if kw in content:
            return f"Detected blocking/login keyword: {kw}"
    return None

async def safe_text(locator: Locator, default: str = "") -> str:
    """Safely retrieves text content from a locator without throwing."""
    try:
        if await locator.count() > 0:
            text = await locator.first.text_content()
            return text.strip() if text else default
    except Exception:
        pass
    return default

async def safe_attr(locator: Locator, attr: str, default: str = "") -> str:
    """Safely retrieves an attribute from a locator without throwing."""
    try:
        if await locator.count() > 0:
            val = await locator.first.get_attribute(attr)
            return val.strip() if val else default
    except Exception:
        pass
    return default
