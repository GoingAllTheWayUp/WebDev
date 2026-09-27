from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.resolve()

# Find all .html files
html_files = list(PROJECT_ROOT.rglob("*.html"))

deleted_count = 0
for html_file in html_files:
    # Check if corresponding .php file exists
    php_file = html_file.with_suffix(".php")
    if php_file.exists():
        html_file.unlink()  # Deletes the .html file
        deleted_count += 1
        print(f"Removed redundant static file: {html_file.name}")

print(f"\n[✓] Cleanup complete. Removed {deleted_count} .html files.")