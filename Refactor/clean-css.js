const { PurgeCSS } = require('purgecss');
const fs = require('fs-extra');

async function runPurge() {
  const purgecssResults = await new PurgeCSS().purge({
    // Path to HTML files to check for used class names
    content: ['./**/*.html', './**/*.php'],
    // Path to CSS files to clean
    css: ['./**/*.css', './**/*.css'],
    // Safelist dynamic classes (e.g., active states, mobile menus)
    safelist: [/^active$/, /^is-open$/, /^wp-/]
  });

  for (const result of purgecssResults) {
    // Overwrite or save clean CSS files
    console.log(`Cleaned: ${result.file}`);
    await fs.writeFile(result.file, result.css);
  }
}

runPurge();