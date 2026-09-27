import os
import re
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup

LIVE_BASE = "https://example.com"
LOCAL_BASE = "http://localhost:8000"

# Set crawl depth (1 = homepage + direct subpages; 2 = subpages of subpages)
MAX_DEPTH = 2

def fetch_content(url):
    """Fetch HTML content from a given URL."""
    headers = {'User-Agent': 'MirrorComparator/2.0'}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.status, response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return None, str(e)

def clean_path(url, base_url):
    """Normalize local and live URLs into domain-relative paths."""
    full_url = urllib.parse.urljoin(base_url, url)
    parsed = urllib.parse.urlparse(full_url)
    
    # Strip domain and normalize trailing slashes
    path = parsed.path
    if not path:
        path = "/"
    if parsed.query:
        path += "?" + parsed.query
    return path

def extract_page_data(html_content, base_url):
    """Extract assets and discover internal subpage links from HTML."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    assets = {
        'scripts': set(),
        'stylesheets': set(),
        'images': set()
    }
    subpages = set()

    # Scripts
    for script in soup.find_all('script', src=True):
        assets['scripts'].add(clean_path(script['src'], base_url))

    # Stylesheets
    for link in soup.find_all('link', rel=lambda x: x and 'stylesheet' in x.lower()):
        if link.has_attr('href'):
            assets['stylesheets'].add(clean_path(link['href'], base_url))

    # Images
    for img in soup.find_all('img'):
        src = img.get('src') or img.get('data-src')
        if src:
            assets['images'].add(clean_path(src, base_url))

    # Internal subpage links
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith(('javascript:', 'mailto:', 'tel:', '#')):
            continue
            
        full_url = urllib.parse.urljoin(base_url, href)
        parsed = urllib.parse.urlparse(full_url)
        
        # Only crawl pages on the same domain
        if parsed.netloc in ("biketechdetroit.com", "localhost:8000", "127.0.0.1:8000", ""):
            # Skip media/static files from subpage queue
            if not any(parsed.path.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.pdf', '.zip', '.css', '.js']):
                subpages.add(clean_path(href, base_url))

    return assets, subpages

def crawl_entire_site():
    visited_paths = set()
    to_visit = {("/", 0)}  # (path, depth)

    live_all_assets = {'stylesheets': set(), 'scripts': set(), 'images': set()}
    local_all_assets = {'stylesheets': set(), 'scripts': set(), 'images': set()}
    
    page_status_report = []

    print(f"[*] Starting full site comparison between {LIVE_BASE} and {LOCAL_BASE}...")
    print(f"[*] Crawl Depth Limit: {MAX_DEPTH}\n")

    while to_visit:
        current_path, depth = to_visit.pop()
        if current_path in visited_paths:
            continue
            
        visited_paths.add(current_path)

        live_url = urllib.parse.urljoin(LIVE_BASE, current_path)
        local_url = urllib.parse.urljoin(LOCAL_BASE, current_path)

        print(f" -> Auditing page [{len(visited_paths)}]: {current_path}")

        status_live, live_html = fetch_content(live_url)
        status_local, local_html = fetch_content(local_url)

        page_status_report.append({
            'path': current_path,
            'live_status': status_live,
            'local_status': status_local
        })

        if status_live == 200 and live_html:
            live_assets, live_subpages = extract_page_data(live_html, LIVE_BASE)
            for k in live_all_assets:
                live_all_assets[k].update(live_assets[k])

            # Queue newly discovered subpages if within max depth
            if depth < MAX_DEPTH:
                for subpath in live_subpages:
                    if subpath not in visited_paths:
                        to_visit.add((subpath, depth + 1))

        if status_local == 200 and local_html:
            local_assets, _ = extract_page_data(local_html, LOCAL_BASE)
            for k in local_all_assets:
                local_all_assets[k].update(local_assets[k])

    # Display Consolidated Report
    print("\n" + "="*65)
    print(" DEEP MIRROR COMPARISON REPORT (ALL SUBPAGES)")
    print("="*65)

    print(f"\nTotal Subpages Audited: {len(visited_paths)}")
    
    # Check for HTTP status mismatches / 404s on subpages
    status_mismatches = [p for p in page_status_report if p['live_status'] != p['local_status']]
    if status_mismatches:
        print("\n [!] HTTP Status Mismatches / Broken Pages:")
        for item in status_mismatches:
            print(f"     - Path: {item['path']} | Live Status: {item['live_status']} | Local Status: {item['local_status']}")
    else:
        print(" [✓] All audited subpages returned matching HTTP status codes.")

    # Audit across all discovered pages
    for category in ['stylesheets', 'scripts', 'images']:
        live_set = live_all_assets[category]
        local_set = local_all_assets[category]

        missing_in_local = live_set - local_set
        
        # Filter out Cloudflare beacon dynamically from missing scripts
        missing_in_local = {item for item in missing_in_local if 'beacon.min.js' not in item}

        print(f"\n--- TOTAL AGGREGATED {category.upper()} ---")
        print(f" Live Site Total: {len(live_set)} | Local Mirror Total: {len(local_set)}")

        if missing_in_local:
            print(f"  [!] Missing in Local Mirror ({len(missing_in_local)}):")
            for item in sorted(missing_in_local):
                print(f"      - {item}")
        else:
            print(f"  [✓] All {category} across all audited pages are present in local mirror.")

if __name__ == "__main__":
    crawl_entire_site()
