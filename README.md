<div align="center">

<h1>Site Mirroring &amp; Refactor + Recovery Pipeline</h1>

<p>An end-to-end toolchain for mirroring a website and refactoring its static HTML into dynamic modular PHP templates, optimizing CSS via Node.js/PurgeCSS, and recovering missing assets from backup files.</p>

<p>
  <img src="https://img.shields.io/badge/Python-v3.x-blue.svg" alt="Python Version" />
  <img src="https://img.shields.io/badge/Node.js-v18%2B-green.svg" alt="Node.js" />
  <img src="https://img.shields.io/badge/PurgeCSS-v5.0-red.svg" alt="PurgeCSS" />
  <img src="https://img.shields.io/badge/PHP-Local%20Host-777BB4.svg" alt="PHP Localhost" />
</p>

</div>

<hr />

<h2>Pipeline Architecture</h2>

<pre><code>[ Remote Website ] ──&gt; [ Site_Mirror-v3.0.py ] ──&gt; [ Local HTML/Assets ]
                                                        │
┌───────────────────────────────────────────────────────┘
│
├──&gt; [ Phase 1: Modular PHP Refactoring ]
│    └── refactor_mirror.v1.py
│        ├── Extracts #masthead, #colophon, &lt;head&gt;, &amp; &lt;script&gt; into /template-parts/
│        └── Converts .html pages into dynamic .php with relative includes
│
├──&gt; [ Phase 2: CSS Purging &amp; Optimization ]
│    └── PowerShell / NPX PurgeCSS OR clean-css.js (Node.js)
│        ├── Scans .html &amp; .php for used CSS classes (with WP safelists)
│        ├── Overwrites stylesheets to trim unused rules
│        └── Generates .bak original backup files
│
└──&gt; [ Phase 3: Asset Recovery &amp; Audit ]
     ├── reportmissing.py (Dry-run audit scanning .bak for missing 404 links)
     └── retrieve_missing_files.v3.py (Downloads missing 404 assets to disk)</code></pre>

<hr />

<h2>Prerequisites</h2>

<h3>1. Python 3.x Dependencies</h3>

<pre><code>pip install requests beautifulsoup4 tldextract lxml</code></pre>

<h3>2. Node.js &amp; NPX Setup</h3>
<p><b>NPX</b> (Node Package Execute) is bundled with <b>Node.js</b> and allows running npm CLI tools without global installations.</p>

<ol>
  <li>Download Node.js from <a href="https://nodejs.org/">nodejs.org</a>.</li>
  <li>Verify installation in PowerShell:</li>
</ol>

<pre><code>node -v
npm -v
npx -v</code></pre>

<ol start="3">
  <li>Install local dependencies for the CSS optimizer:</li>
</ol>

<pre><code>npm install purgecss fs-extra</code></pre>

<hr />

<h2>Execution Workflow</h2>

<h3>Step 1: Mirror Remote Site</h3>
<p>Crawl the target site to build an initial local static snapshot with index handling[cite: 1]:</p>

<pre><code>python Site_Mirror-v3.0.py</code></pre>

<h3>Step 2: Refactor HTML into PHP Templates</h3>
<p>Automatically decompose static HTML files into modular PHP components (`header.php`, `footer.php`, `head-resources.php`, `footer-scripts.php`) stored in <code>template-parts/</code>[cite: 11]:</p>

<pre><code>python refactor_mirror.v1.py</code></pre>

<h3>Step 3: Purge Unused CSS</h3>
<p>Run PurgeCSS via PowerShell or Node.js to trim redundant stylesheet bloat while preserving WordPress dynamic classes (`wp-`, `active`, `is-open`)[cite: 10]:</p>

<pre><code># Option A: PowerShell via NPX
npx purgecss --css ./css/*.css --content ./**/*.html ./**/*.php --output ./css/ --rejected

# Option B: Programmatic Node.js Script
node clean-css.js</code></pre>

<h3>Step 4: Audit Missing Assets</h3>
<p>Scan <code>.bak</code> files left behind by purge steps to identify unresolved 404 remote links[cite: 12]:</p>

<pre><code>python reportmissing.py</code></pre>

<h3>Step 5: Recover &amp; Download Missing 404 Assets</h3>
<p>Scrape missing URLs from <code>.bak</code> files, sanitize Windows file paths, and fetch missing files into local directory trees[cite: 13]:</p>

<pre><code>python retrieve_missing_files.v3.py</code></pre>

<h3>Step 6: Remove *.html files from localhost root dir.</h3>
<p>run refact.clean.py or proform manual deletions.</p>
<hr />

<h2>Script Reference Matrix</h2>

<table>
  <thead>
    <tr>
      <th>Script</th>
      <th>Runtime</th>
      <th>Primary Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>Site_Mirror-v3.0.py</code></td>
      <td>Python</td>
      <td>Recursive site crawler with directory index handling and XML fallback[cite: 1].</td>
    </tr>
    <tr>
      <td><code>refactor_mirror.v1.py</code></td>
      <td>Python</td>
      <td>Extracts shared UI components into PHP includes and outputs <code>.php</code> pages[cite: 11].</td>
    </tr>
    <tr>
      <td><code>clean-css.js</code></td>
      <td>Node.js</td>
      <td>Programmatic PurgeCSS engine with dynamic safelists for WordPress[cite: 10].</td>
    </tr>
    <tr>
      <td><code>reportmissing.py</code></td>
      <td>Python</td>
      <td>Dry-run scanner checking local disk against URLs found in <code>.bak</code> files[cite: 12].</td>
    </tr>
    <tr>
      <td><code>retrieve_missing_files.v3.py</code></td>
      <td>Python</td>
      <td>Active recovery engine fetching missing 404 assets from backup logs[cite: 13].</td>
    </tr>
        <tr>
      <td><code>refact.clean.py</code></td>
      <td>Python</td>
      <td>Removes *.html recursively from @ROOT level of Mirror once PHP has been established</td>
    </tr>
  </tbody>
</table>
