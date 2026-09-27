import os
import re
from urllib.parse import urlparse
import requests

ROOT = r"X:\Local\Host\ROOT\example.com"

# Exclude HTML closing tags, quotes, whitespace, and typical trailing delimiters
url_pattern = re.compile(
    r'https?://(?:www\.)?example\.com/[^\s"<>\'\\)]+',
    re.IGNORECASE,
)

INVALID_WIN_CHARS = re.compile(r'[<>:"|?*]')

found_urls = set()

# 1. Collect URLs from .bak files
for root, dirs, files in os.walk(ROOT):
    for file in files:
        if not file.endswith(".bak"):
            continue

        path = os.path.join(root, file)

        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()

            for raw_url in url_pattern.findall(text):
                # Clean up trailing punctuation
                cleaned_url = raw_url.rstrip(".,;)")
                found_urls.add(cleaned_url)

        except Exception as e:
            print("Read error:", path, e)

print(f"Found {len(found_urls)} URLs")

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
        " like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}

# 2. Process and download missing files
for url in sorted(found_urls):
    parsed = urlparse(url)
    rel_path = parsed.path.lstrip("/")

    if not rel_path or rel_path.endswith("/"):
        rel_path = os.path.join(rel_path, "index.html")

    rel_path = rel_path.replace("/", os.path.sep)
    rel_path = INVALID_WIN_CHARS.sub("", rel_path)

    local_file = os.path.normpath(os.path.join(ROOT, rel_path))

    if os.path.exists(local_file):
        print("EXISTS:", rel_path)
        continue

    dir_name = os.path.dirname(local_file)

    # Safely create parent directories
    if dir_name:
        try:
            os.makedirs(dir_name, exist_ok=True)
        except (FileExistsError, OSError) as e:
            print(f"SKIPPING (Parent path is a file, not a directory): {url}")
            continue

    print("DOWNLOADING:", url)

    try:
        r = requests.get(url, headers=headers, timeout=20)

        if r.status_code == 200:
            with open(local_file, "wb") as f:
                f.write(r.content)
            print("OK")
        else:
            print("HTTP", r.status_code)

    except Exception as e:
        print("FAILED:", e)

print("DONE")