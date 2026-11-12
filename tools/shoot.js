// Usage: node shoot.js <dir-with-post-XX.html>  -> writes post-XX.png next to each
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const dir = process.argv[2];
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
  const p = await b.newPage({ viewport: { width: 1200, height: 1200 } });
  for (const f of fs.readdirSync(dir).filter(x => /^post-\d+\.html$/.test(x)).sort()) {
    await p.goto('file://' + path.join(dir, f));
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(150);
    const overflow = await p.evaluate(() => {
      const m = document.querySelector('.main'); const w = document.querySelector('.wrap');
      return { main: m ? m.scrollHeight > m.clientHeight + 2 : false, page: document.body.scrollHeight > 1200 };
    });
    await p.screenshot({ path: path.join(dir, f.replace('.html', '.png')) });
    console.log(f, JSON.stringify(overflow));
  }
  await b.close();
})();
