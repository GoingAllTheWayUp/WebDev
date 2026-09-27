import os
import re
from urllib.parse import urlparse

ROOT = r"X:\Local\Host\ROOT\example.com"
urls = set()

for root, dirs, files in os.walk(ROOT):

    for file in files:

        if file.endswith(".bak"):

            path = os.path.join(root, file)

            text = open(
                path,
                encoding="utf-8",
                errors="ignore"
            ).read()

            urls.update(
                re.findall(
                    r'https?://(?:www\.)?example\.com/[^"\'>)\s]+',
                    text,
                    re.I
                )
            )

for url in sorted(urls):

    rel = urlparse(url).path.lstrip("/")

    local = os.path.join(ROOT, rel)

    if not os.path.exists(local):

        print(url)