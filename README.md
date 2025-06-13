# Webpage Screenshot Scraper

This small Python project captures **full-page JPEG screenshots** of a list of websites — even those that rely on JavaScript to render. It uses Selenium running a headless Chrome browser and organises the output in timestamped folders.

```
output/
└── 20240521_152045/
    ├── python/
    │   └── www.python.org.jpg
    └── example/
        └── example.com.jpg
```

## Installation

1. Create/activate a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # .venv\Scripts\activate  # Windows PowerShell
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

The first run will automatically download the appropriate ChromeDriver binary via **webdriver-manager**. Make sure Google Chrome (or Chromium) is installed on your system.

## Configuration

Open `web_screenshot.py` and modify the `WEBSITES` dictionary near the top of the file:

```python
WEBSITES = {
    "myblog": [
        "https://my-blog.com/",
        "https://my-blog.com/about/",
    ],
    "news": [
        "https://news.ycombinator.com/",
    ],
}
```

Each key becomes a sub-folder, and every URL in the list will be captured.

## Running the scraper

```bash
python web_screenshot.py
```

Screenshots will be written to the `output/` directory using the pattern described above.

## Notes

* The script sets the browser window size to **1920×page-height** so the screenshot contains the entire page.
* Screenshots are first taken as PNG (the format Selenium provides) and immediately converted to **JPEG** using Pillow.
* Adjust implicit wait times or add explicit waits if a target site requires more time to load complex content. 