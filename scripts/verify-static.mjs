/** Verify the built single-file game and an HTTP repository subpath. */
import {createServer} from 'node:http';
import {readFile,mkdir,writeFile,access} from 'node:fs/promises';
import {resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
import assert from 'node:assert/strict';
process.env.TMPDIR=resolve('.cache/tmp');process.env.PLAYWRIGHT_BROWSERS_PATH=resolve('.cache/browsers');
await mkdir(process.env.TMPDIR,{recursive:true});await mkdir('test-results/production',{recursive:true});
const {chromium,webkit}=await import('@playwright/test');
const html=await readFile('dist/index.html');
const server=createServer((req,res)=>{if(req.url==='/last-login/'||req.url==='/last-login/index.html'){res.writeHead(200,{'Content-Type':'text/html'});res.end(html);}else{res.writeHead(404);res.end();}});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));const report={checks:[]};
async function check(name,browser,url,location){const context=await browser.newContext({viewport:{width:1280,height:720}});const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('requestfailed',r=>errors.push(r.failure()?.errorText));page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`);});
  try{await page.goto(url);await page.getByRole('button',{name:/New Game/}).click();for(let i=0;i<4;i++)await page.getByRole('button',{name:/继续 ↵/}).click();await page.getByRole('button',{name:'打开 Photos',exact:true}).click();const p=page.getByRole('dialog',{name:'Photos',exact:true});assert.equal(await p.locator('.photo-tile').count(),18);await page.waitForFunction(()=>[...document.images].every(i=>i.complete&&i.naturalWidth>0));await p.locator('.photo-tile').nth(15).click();assert.equal(await p.locator('.full-photo').evaluate(i=>i.naturalHeight),426);await p.getByRole('button',{name:'← 相册'}).click();await page.getByRole('button',{name:'关闭 Photos',exact:true}).click();await page.getByRole('button',{name:'打开 Browser',exact:true}).click();const b=page.getByRole('dialog',{name:'Browser',exact:true});for(let i=0;i<2;i++){await b.getByRole('textbox',{name:'搜索关键词'}).fill('Morrow');await b.getByRole('button',{name:'搜索',exact:true}).click();if(i===0)assert(await b.getByText('没有找到与Morrow对应的火车站。').isVisible());}assert(await b.getByRole('button',{name:'Morrow Railway Station',exact:true}).isVisible());assert.deepEqual(errors,[]);await page.screenshot({path:`test-results/production/${name}-${location}.png`,animations:'disabled'});report.checks.push({browser:name,location,photos:18,secondSearch:true,errors});}finally{await context.close();}}
let browser;
try{browser=await chromium.launch({executablePath:process.env.CHROME_PATH||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--disable-crash-reporter','--disable-breakpad']});await check('chrome',browser,pathToFileURL(resolve('dist/index.html')).href,'file');await check('chrome',browser,`http://127.0.0.1:${server.address().port}/last-login/`,'subpath');await browser.close();browser=undefined;
  const available=await access(webkit.executablePath()).then(()=>true,()=>false);if(available){browser=await webkit.launch();await check('webkit',browser,pathToFileURL(resolve('dist/index.html')).href,'file');await browser.close();browser=undefined;}else report.webkit='not installed: optional check skipped';
  await writeFile('test-results/production/report.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report));
}finally{await browser?.close();await new Promise(resolve=>server.close(resolve));}
