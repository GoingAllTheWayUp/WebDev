<div align="center">

<h1>Site Asset Recovery & PurgeCSS Toolkit</h1>

<p>A post-processing and recovery pipeline to optimize static assets using PurgeCSS in PowerShell, and automatically backfill missing site assets using Python.</p>

<p>
  <img src="https://img.shields.io/badge/Node.js-NPX-brightgreen.svg" alt="Node.js NPX" />
  <img src="https://img.shields.io/badge/PowerShell-v5.1+-blue.svg" alt="PowerShell" />
  <img src="https://img.shields.io/badge/Python-3.x-yellow.svg" alt="Python Version" />
</p>

</div>

<hr />

<h2>Workflow Architecture</h2>

<p>When running CSS optimization tools like <b>PurgeCSS</b>, original source files are preserved as <code>.bak</code> copies. This toolkit uses those backup files as a reference index to detect, audit, and re-download missing remote assets to ensure local mirrors remain complete.</p>

<pre><code>[Mirrored Site Directory]
         │
         ├──> 1. Run PurgeCSS (Node.js/PowerShell) ──> Creates .bak files
         │
         ├──> 2. Run reportmissing.py ──> Scans .bak files & reports missing local paths
         │
         └──> 3. Run retrieve_missing_files.v3.py ──> Fetches & backfills 404s to disk
</code></pre>

<hr />

<h2>Step 1: Prerequisites & Prerequisites Setup</h2>

<h3>What is NPX?</h3>
<p><b>NPX</b> (Node Package eXecutor) is a CLI tool bundled with <b>Node.js / NPM</b>. It allows you to execute npm packages (like <code>purgecss</code>) directly without needing to install them globally on your system.</p>

<h3>Installing Node.js & NPX</h3>
<ol>
  <li>Download and run the LTS installer from the official <a href="https://nodejs.org/">Node.js Website</a>.</li>
  <li>Verify installation in <b>PowerShell</b>:
    <pre><code>node -v
npm -v
npx -v</code></pre>
  </li>
</ol>

<h3>Python Dependencies</h3>
<p>Ensure Python 3.x is installed along with the <code>requests</code> package:</p>
<pre><code>pip install requests</code></pre>

<hr />

<h2>Step 2: Purging CSS in PowerShell</h2>

<p>To analyze HTML/PHP templates and strip out unused CSS rules, run PurgeCSS inside your target site root using PowerShell. This process outputs modified CSS and preserves backup target states in <code>.bak</code> files.</p>

<h3>PowerShell Command</h3>
<pre><code>npx purgecss --css ./css/*.css --content ./**/*.html ./**/*.php --output ./css/ --rejected</code></pre>

<p><b>Command Options:</b></p>
<ul>
  <li><code>--css</code>: Specifies the stylesheet files to optimize.</li>
  <li><code>--content</code>: Scans all HTML and PHP files for active class names.</li>
  <li><code>--output</code>: Defines where processed CSS should be saved.</li>
  <li><code>--rejected</code>: Generates a log/backup reference of removed selectors and assets.</li>
</ul>

<hr />

<h2>Step 3: Auditing Missing Assets (<code>reportmissing.py</code>)</h2>

<p>This script walks through all <code>.bak</code> files generated during purging, extracts absolute site URLs via regex, and checks if they exist in your local directory layout.</p>

<h3>Configuration & Usage</h3>
<ol>
  <li>Open <code>reportmissing.py</code> and set your target directory path:
    <pre><code>ROOT = r"X:\Local\Host\ROOT\example.com"</code></pre>
  </li>
  <li>Run the dry-run audit in PowerShell:
    <pre><code>python reportmissing.py</code></pre>
  </li>
  <li><b>Output:</b> Prints a list of missing absolute URLs that are referenced in <code>.bak</code> files but missing from your disk.</li>
</ol>

<hr />

<h2>Step 4: Auto-Downloading Missing Files (<code>retrieve_missing_files.v3.py</code>)</h2>

<p>This script automates missing file recovery by scanning <code>.bak</code> files, resolving Windows path sanitization issues, creating target parent folders, and fetching remote files via HTTP requests.</p>

<h3>Features</h3>
<ul>
  <li><b>Path Cleaning:</b> Strips invalid Windows characters (<code>&lt;&gt;:"|?*</code>) from URL paths.</li>
  <li><b>Directory Handling:</b> Automatically generates nested subdirectories as needed.</li>
  <li><b>Index Fallback:</b> Appends <code>index.html</code> to directory endpoints.</li>
</ul>

<h3>Execution</h3>
<ol>
  <li>Set your target root path in <code>retrieve_missing_files.v3.py</code>:
    <pre><code>ROOT = r"X:\Local\Host\ROOT\example.com"</code></pre>
  </li>
  <li>Execute the download recovery process:
    <pre><code>python retrieve_missing_files.v3.py</code></pre>
  </li>
</ol>

<hr />

<h2>Script Comparison</h2>

<table>
  <thead>
    <tr>
      <th>Feature</th>
      <th><code>reportmissing.py</code></th>
      <th><code>retrieve_missing_files.v3.py</code></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Primary Goal</b></td>
      <td>Audit & report missing assets</td>
      <td>Fetch & save missing assets to disk</td>
    </tr>
    <tr>
      <td><b>Disk Writes</b></td>
      <td>Read-only</td>
      <td>Creates directories & downloads files</td>
    </tr>
    <tr>
      <td><b>Network Requests</b></td>
      <td>None</td>
      <td>HTTP GET requests with custom User-Agent</td>
    </tr>
    <tr>
      <td><b>Windows Path Fixes</b></td>
      <td>Basic</td>
      <td>Full regex sanitization for Windows OS</td>
    </tr>
  </tbody>
</table>