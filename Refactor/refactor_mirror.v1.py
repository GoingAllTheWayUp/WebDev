import os
import re
from pathlib import Path
from bs4 import BeautifulSoup, Comment

# Root directory of your local mirror
PROJECT_ROOT = Path(__file__).parent.resolve()
TEMPLATE_DIR = PROJECT_ROOT / "template-parts"
TEMPLATE_DIR.mkdir(exist_ok=True)

def find_all_html_files(root_dir: Path):
    """Recursively discover all static .html files excluding template-parts."""
    return [
        p for p in root_dir.rglob("*.html") 
        if "template-parts" not in p.parts
    ]

def extract_and_save_shared_components(html_files):
    """
    Analyzes primary index or first valid HTML file to extract 
    master header, footer, head resources, and global scripts.
    """
    # Prefer root index.html if available
    primary_file = PROJECT_ROOT / "index.html"
    if not primary_file.exists():
        primary_file = html_files[0]

    with open(primary_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "lxml")

    # 1. Extract Global Header (#masthead)
    header = soup.find("header", id="masthead")
    if header:
        (TEMPLATE_DIR / "header.php").write_text(str(header), encoding="utf-8")

    # 2. Extract Global Footer (#colophon)
    footer = soup.find("footer", id="colophon")
    if footer:
        (TEMPLATE_DIR / "footer.php").write_text(str(footer), encoding="utf-8")

    # 3. Extract Head Resources (Stylesheets & Inline CSS Blocks)
    head = soup.find("head")
    if head:
        # Collect stylesheets, theme inline styles, and Google fonts
        head_elements = head.find_all(["link", "style"])
        head_markup = "\n".join(str(el) for el in head_elements)
        (TEMPLATE_DIR / "head-resources.php").write_text(head_markup, encoding="utf-8")

    # 4. Extract Footer JS Scripts before </body>
    body = soup.find("body")
    if body:
        scripts = body.find_all("script")
        script_markup = "\n".join(str(s) for s in scripts)
        (TEMPLATE_DIR / "footer-scripts.php").write_text(script_markup, encoding="utf-8")

    print(f"[✓] Extracted master template components from: {primary_file.name}")

def get_php_include(from_file: Path, target_template: str) -> str:
    """Computes accurate relative path for PHP includes across nested directories."""
    target_path = TEMPLATE_DIR / target_template
    rel_path = os.path.relpath(target_path, start=from_file.parent).replace("\\", "/")
    return f'<?php include __DIR__ . "/{rel_path}"; ?>'

def process_file(file_path: Path):
    """Cleans up static markup and replaces shared blocks with PHP includes."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, "lxml")

    # Compute PHP includes for this file's relative depth
    inc_head = get_php_include(file_path, "head-resources.php")
    inc_header = get_php_include(file_path, "header.php")
    inc_footer = get_php_include(file_path, "footer.php")
    inc_scripts = get_php_include(file_path, "footer-scripts.php")

    # 1. Strip redundant stylesheets/inline styles from <head> and insert PHP include
    head = soup.find("head")
    if head:
        for el in head.find_all(["link", "style"]):
            # Preserve page-specific meta tags or canonical links if needed
            if el.get("rel") == ["canonical"]:
                continue
            el.decompose()
        head.append(BeautifulSoup(inc_head, "html.parser"))

    # 2. Replace Header (#masthead)
    header = soup.find("header", id="masthead")
    if header:
        header.replace_with(BeautifulSoup(inc_header, "html.parser"))

    # 3. Replace Footer (#colophon)
    footer = soup.find("footer", id="colophon")
    if footer:
        footer.replace_with(BeautifulSoup(inc_footer, "html.parser"))

    # 4. Remove scripts from body and append shared script include before </body>
    body = soup.find("body")
    if body:
        for script in body.find_all("script"):
            script.decompose()
        body.append(BeautifulSoup(inc_scripts, "html.parser"))

    # Output formatted HTML string back to .php
    output_php = file_path.with_suffix(".php")
    
    # Unescape raw PHP tags modified by BeautifulSoup parsing
    clean_html = str(soup).replace("&lt;?php", "<?php").replace("?&gt;", "?>")

    with open(output_php, "w", encoding="utf-8") as f:
        f.write(clean_html)

    print(f"[Processed] {file_path.relative_to(PROJECT_ROOT)} -> {output_php.name}")

def main():
    html_files = find_all_html_files(PROJECT_ROOT)
    if not html_files:
        print("[!] No HTML files found in local root directory.")
        return

    print(f"[*] Found {len(html_files)} HTML pages across site directories.")
    
    # Step 1: Generate common snippets
    extract_and_save_shared_components(html_files)

    # Step 2: Refactor all pages
    for html_file in html_files:
        process_file(html_file)

    print("\n[✓] Refactoring complete. You can now serve your directory via local PHP.")

if __name__ == "__main__":
    main()