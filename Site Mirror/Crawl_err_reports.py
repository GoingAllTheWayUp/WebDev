import os
import requests
from urllib.parse import urljoin

# >>> SET THESE TO MATCH YOUR SETUP <<<
BASE_URL   = "https://biketechdetroit.com/"
OUTPUT_DIR = r"F:\Text\Hyper Text Markup\TECH\biketechdetroit.com"
ERROR_LOG  = os.path.join(OUTPUT_DIR, "crawl_errors_REBUILT.txt")

errors = []

def check_url(url):
    try:
        # Use HEAD to avoid downloading full content
        r = requests.head(url, timeout=10, allow_redirects=True)
        if r.status_code != 200:
            errors.append(f"ERROR: {url}\nDETAILS: Status {r.status_code}\n")
    except Exception as e:
        errors.append(f"ERROR: {url}\nDETAILS: {str(e)}\n")

# Walk mirrored folder and rebuild URLs from file paths
for root, dirs, files in os.walk(OUTPUT_DIR):
    for file in files:
        # Only care about pages you mirrored
        if file.endswith(".html") or file.endswith(".xml"):
            full_path = os.path.join(root, file)
            rel_path  = os.path.relpath(full_path, OUTPUT_DIR)
            rel_url   = rel_path.replace("\\", "/")
            url       = urljoin(BASE_URL, rel_url)
            check_url(url)

# Write rebuilt error log
with open(ERROR_LOG, "w", encoding="utf-8") as f:
    f.write("\n".join(errors))

print("Rebuilt crawl error log:", ERROR_LOG)
