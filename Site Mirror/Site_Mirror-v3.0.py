import os
import requests
import tldextract
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

visited = set()
asset_log = []
error_log = []

def is_same_domain(base_url, target_url):
    base = tldextract.extract(base_url)
    target = tldextract.extract(target_url)
    return (base.domain == target.domain and base.suffix == target.suffix)

def save_file(local_path, content, mode="wb"):
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    with open(local_path, mode) as f:
        f.write(content)

def log_asset(referrer, asset_url, local_path):
    asset_log.append(f"ASSET: {asset_url}\nFROM: {referrer}\nSAVED AS: {local_path}\n")

def log_error(url, error):
    error_log.append(f"ERROR: {url}\nDETAILS: {error}\n")

def download_asset(base_url, asset_url, output_dir, referrer):
    try:
        full_url = urljoin(base_url, asset_url)
        parsed = urlparse(full_url)

        # Fix: ensure assets have filenames
        asset_path = parsed.path.lstrip("/")
        if asset_path.endswith("/"):
            asset_path += "index.html"

        local_path = os.path.join(output_dir, asset_path)

        # SKIP if file already exists
        if os.path.exists(local_path):
            return

        resp = requests.get(full_url, timeout=10)

        if resp.status_code == 200:
            save_file(local_path, resp.content)
            log_asset(referrer, full_url, local_path)
        else:
            log_error(full_url, f"Status {resp.status_code}")

    except Exception as e:
        log_error(asset_url, str(e))

def crawl_page(base_url, url, output_dir):
    if url in visited:
        return
    visited.add(url)

    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            log_error(url, f"Status {resp.status_code}")
            return

        # XML vs HTML parser selection (safe fallback)
        content_type = resp.headers.get("Content-Type", "")
        if content_type.startswith("application/xml") or url.endswith(".xml"):
            try:
                soup = BeautifulSoup(resp.text, "xml")
            except Exception:
                soup = BeautifulSoup(resp.text, "html.parser")
        else:
            soup = BeautifulSoup(resp.text, "html.parser")

        parsed = urlparse(url)

        # Fix: ensure directories save as index.html
        html_path = parsed.path.lstrip("/")
        if html_path == "" or html_path.endswith("/"):
            html_path += "index.html"

        local_html_path = os.path.join(output_dir, html_path)

        # SKIP if HTML file already exists
        if os.path.exists(local_html_path):
            return

        save_file(local_html_path, resp.text.encode("utf-8"), "wb")

        # Download assets
        for tag, attr in [
            ("img", "src"),
            ("script", "src"),
            ("link", "href")
        ]:
            for element in soup.find_all(tag):
                asset_url = element.get(attr)
                if asset_url:
                    download_asset(base_url, asset_url, output_dir, url)

        # Crawl internal links
        for a in soup.find_all("a"):
            href = a.get("href")
            if not href:
                continue

            full = urljoin(base_url, href)
            if is_same_domain(base_url, full):
                crawl_page(base_url, full, output_dir)

    except Exception as e:
        log_error(url, str(e))

def write_logs(output_dir):
    with open(os.path.join(output_dir, "crawl_assets.txt"), "w") as f:
        f.write("\n".join(asset_log))

    with open(os.path.join(output_dir, "crawl_errors.txt"), "w") as f:
        f.write("\n".join(error_log))

def mirror_site(start_url, output_dir="site_mirror"):
    os.makedirs(output_dir, exist_ok=True)
    crawl_page(start_url, start_url, output_dir)
    write_logs(output_dir)

if __name__ == "__main__":
    start_url = "https://*domain.com"
    output_dir = "X:\\Local\\Host\\ROOT\\*domain.com"

    mirror_site(start_url, output_dir)
    print("Mirror complete.")
