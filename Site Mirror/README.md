<div align="center">

<h1>Site Mirror v3.0</h1>

<p>A recursive Python web crawler and site archiving tool designed to mirror target websites locally.</p>

<p>
  <img src="https://img.shields.io/badge/python-v3.x-blue.svg" alt="Python Version" />
  <img src="https://img.shields.io/badge/dependencies-requests%20%7C%20bs4%20%7C%20tldextract-orange.svg" alt="Dependencies" />
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License" />
</p>

</div>

<hr />

<h2>Overview</h2>

<p><b>Site Mirror v3.0</b> automatically extracts HTML pages, captures linked static assets (images, scripts, and stylesheets), preserves nested directory structures, and logs execution details during traversal[cite: 1].</p>

<h3>Key Features</h3>

<ul>
  <li><b>Domain-Bounded Crawling:</b> Restricts recursive link discovery strictly to the target root domain using <code>tldextract</code>[cite: 1].</li>
  <li><b>Asset Archiving:</b> Downloads linked assets (<code>&lt;img&gt;</code>, <code>&lt;script&gt;</code>, <code>&lt;link&gt;</code>) referenced across all crawled pages[cite: 1].</li>
  <li><b>Smart File Pathing:</b> Appends <code>index.html</code> to root and directory URLs to preserve valid local file structures[cite: 1].</li>
  <li><b>Parser Fallback:</b> Automatically selects between <code>xml</code> and <code>html.parser</code> depending on <code>Content-Type</code> headers or <code>.xml</code> file extensions[cite: 1].</li>
  <li><b>Duplicate Skipping:</b> Bypasses existing files and tracked URLs to avoid duplicate downloads[cite: 1].</li>
  <li><b>Execution Logs:</b> Generates detailed text logs tracking downloaded assets and request failures[cite: 1].</li>
</ul>

<hr />

<h2>Installation &amp; Prerequisites</h2>

<p>Make sure Python 3.x is installed, then install the required dependencies:</p>

<pre><code>pip install requests beautifulsoup4 tldextract lxml</code></pre>

<hr />

<h2>Usage</h2>

<ol>
  <li>Open <code>Site_Mirror-v3.0.py</code>[cite: 1].</li>
  <li>Configure your <code>start_url</code> and <code>output_dir</code> at the bottom of the file[cite: 1]:</li>
</ol>

<pre><code>if __name__ == "__main__":
    start_url = "https://example.com"
    output_dir = "./site_mirror"

    mirror_site(start_url, output_dir)
</code></pre>

<ol start="3">
  <li>Execute the script:</li>
</ol>

<pre><code>python Site_Mirror-v3.0.py</code></pre>

<hr />

<h2>Output Directory Structure</h2>

<table>
  <thead>
    <tr>
      <th>File / Directory</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>index.html</code></td>
      <td>Mirrored home page of the target site[cite: 1].</td>
    </tr>
    <tr>
      <td><code>assets/</code></td>
      <td>Folder containing local copies of images, CSS, and JS files[cite: 1].</td>
    </tr>
    <tr>
      <td><code>crawl_assets.txt</code></td>
      <td>Log mapping downloaded assets to their referrer page and local storage path[cite: 1].</td>
    </tr>
    <tr>
      <td><code>crawl_errors.txt</code></td>
      <td>Log detailing HTTP status failures and network exceptions[cite: 1].</td>
    </tr>
  </tbody>
</table>

<hr />

<h2>Technical Architecture</h2>

<details>
  <summary><b>Click to expand script logic workflow</b></summary>
  <br />
  <pre><code>[Start Mirror] ──&gt; [Crawl Page] ──&gt; [Parse HTML/XML]
                            │                │
                            ├──&gt; [Extract &lt;a&gt; Links] ──&gt; (If same domain) ──&gt; Recurse
                            │
                            └──&gt; [Extract Assets] ──&gt; [Save to local dir] ──&gt; [Log Asset]</code></pre>
</details>
