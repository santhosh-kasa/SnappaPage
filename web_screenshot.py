#!/usr/bin/env python3
"""
Webpage Screenshot Scraper

This script visits a list of URLs (including those requiring JavaScript to render) and
saves full-page screenshots as JPEG images. Screenshots are organised under the output
folder using the pattern:

    output/<YYYYMMDD_HHMMSS>/<website_key>/<sanitised_url>.jpg

Configuration: update the WEBSITES dictionary at the top of the file to target the
sites you care about.

Dependencies are managed via requirements.txt (selenium, webdriver-manager, pillow).
Run `pip install -r requirements.txt` before executing.
"""

from __future__ import annotations

import datetime as _dt
import io as _io
import os as _os
import re as _re
from pathlib import Path as _Path
from typing import Dict, List
import time as _time

from PIL import Image as _Image
from selenium import webdriver as _webdriver
from selenium.webdriver.chrome.options import Options as _ChromeOptions
from selenium.webdriver.chrome.service import Service as _ChromeService
from webdriver_manager.chrome import ChromeDriverManager as _ChromeDriverManager

# --------------------------------------------------------------------------------------
# CONFIGURATION
# --------------------------------------------------------------------------------------
# Map a shorthand website key to a list of URLs belonging to that website. Feel free to
# edit this structure to suit your needs.
WEBSITES: Dict[str, List[str]] = {
    "python": [
        "https://www.python.org/",
    ]
}


# Root directory under which screenshots will be written.
OUTPUT_ROOT = _Path("/Users/kasa/Documents/webscapper")

# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def _slugify(url: str) -> str:
    """Convert a URL into a filesystem-safe slug."""
    slug = _re.sub(r"https?://", "", url, flags=_re.IGNORECASE)  # strip scheme
    slug = slug.rstrip("/")
    slug = _re.sub(r"[^A-Za-z0-9._-]", "_", slug)  # replace unsafe chars
    return slug


def _create_driver(*, headless: bool = True) -> _webdriver.Chrome:
    """Spin up a (headless) Chrome WebDriver instance using webdriver-manager."""
    chrome_options = _ChromeOptions()
    if headless:
        # Use the broadly compatible legacy headless flag. This avoids
        # "DevToolsActivePort file doesn't exist" errors on some systems.
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    service = _ChromeService(_ChromeDriverManager().install())
    driver = _webdriver.Chrome(service=service, options=chrome_options)
    # A small implicit wait helps ensure JS content has a moment to render.
    driver.implicitly_wait(5)
    return driver


def _save_png_as_jpeg(png_bytes: bytes, dest: _Path) -> None:
    """Convert PNG byte payload to JPEG and save to *dest*."""
    image = _Image.open(_io.BytesIO(png_bytes))
    rgb = image.convert("RGB")  # JPEG does not support alpha channel
    rgb.save(dest, "JPEG", quality=90)


def _capture_url(driver: _webdriver.Chrome, url: str, dest_dir: _Path) -> None:
    """Navigate to *url*, capture full-page screenshot, write to *dest_dir*."""
    dest_dir.mkdir(parents=True, exist_ok=True)

    driver.get(url)

    # Resize window height to full scroll height so we capture the entire page
    scroll_height = driver.execute_script("return document.body.parentNode.scrollHeight")
    driver.set_window_size(1920, scroll_height)

    png_data = driver.get_screenshot_as_png()
    filename = _slugify(url) + ".jpg"
    _save_png_as_jpeg(png_data, dest_dir / filename)
    print(f"✓ Saved screenshot for {url} → {dest_dir/filename}")
    _time.sleep(0.5)  # brief pause between requests

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    timestamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    driver = _create_driver(headless=True)

    try:
        for site_key, urls in WEBSITES.items():
            for url in urls:
                _capture_url(driver, url, OUTPUT_ROOT / timestamp / site_key)
    finally:
        driver.quit()


if __name__ == "__main__":
    main() 