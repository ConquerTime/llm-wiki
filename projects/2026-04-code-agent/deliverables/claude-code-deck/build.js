// build.js — Claude Code 源码设计讲解 deck
//
// 用法：
//   node build.js          → 检验所有 slide，全通过就写 pptx
//   node build.js --lint   → 只检验，不写 pptx
//   node build.js --strict → 第一个错误就中断

const fs = require('fs');
const path = require('path');
const pptxgen = require('pptxgenjs');
const html2pptx = require('./html2pptx');
const notesMap = require('./notes-map');

const META = {
  title: 'Claude Code 源码设计讲解',
  author: 'ZYD',
  subject: 'Internal Sharing',
};
const OUT_FILE = 'claude-code-deck.pptx';

const args = process.argv.slice(2);
const LINT_ONLY = args.includes('--lint');
const STRICT = args.includes('--strict');

async function build() {
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.title = META.title;
  pptx.author = META.author;
  pptx.subject = META.subject;

  const slidesDir = path.join(__dirname, 'slides');
  const files = fs.readdirSync(slidesDir)
    .filter(f => /^slide\d+\.html$/.test(f))
    .sort();

  if (files.length === 0) throw new Error(`No slides found in ${slidesDir}`);

  const failures = [];

  for (const file of files) {
    const m = file.match(/^slide(\d+)\.html$/);
    const num = parseInt(m[1], 10);
    process.stdout.write(`Checking ${file}... `);
    try {
      await html2pptx(path.join(slidesDir, file), pptx);
      const slide = pptx.slides[pptx.slides.length - 1];
      const notes = notesMap[num];
      if (notes) slide.addNotes(notes);
      console.log('OK');
    } catch (err) {
      console.log(`FAIL: ${err.message}`);
      failures.push({ file, error: err.message });
      if (STRICT) break;
    }
  }

  if (failures.length > 0) {
    console.error('\n===== BUILD FAILURES =====');
    failures.forEach(f => console.error(`  ${f.file}: ${f.error}`));
    process.exit(1);
  }

  if (!LINT_ONLY) {
    await pptx.writeFile({ fileName: OUT_FILE });
    console.log(`\nWrote ${OUT_FILE} (${files.length} slides)`);
  } else {
    console.log(`\nLint passed (${files.length} slides)`);
  }
}

build().catch(err => { console.error(err); process.exit(1); });
