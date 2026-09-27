\# Site Mirror v3.0



A recursive Python web crawler and site archiving tool designed to create local static mirrors of target domains. It automatically extracts HTML content, captures linked assets (images, scripts, and stylesheets), preserves directory structures, and logs execution details.



\---



\## Features



\- \*\*Domain-Bounded Crawling\*\*: Restricts recursive link discovery to the target root domain using `tldextract`.

\- \*\*Asset Archiving\*\*: Finds and downloads linked assets (`<img>`, `<script>`, `<link>`) referenced across pages.

\- \*\*Smart File Path Handling\*\*: Automatically appends `index.html` to root and directory URLs to maintain valid local file trees.

\- \*\*Parser Fallback\*\*: Intelligently switches between `xml` and `html.parser` depending on `Content-Type` headers or `.xml` extensions.

\- \*\*Duplicate Skipping\*\*: Ignores already downloaded files and tracked URLs to avoid redundant requests.

\- \*\*Logging\*\*: Generates detailed records for downloaded assets (`crawl\_assets.txt`) and request failures (`crawl\_errors.txt`)\[cite: 1].



\---



\## Prerequisites



Ensure Python 3.x is installed on your system.



\### Required Dependencies



Install the required third-party libraries using `pip`:



```bash

pip install requests beautifulsoup4 tldextract lxml

