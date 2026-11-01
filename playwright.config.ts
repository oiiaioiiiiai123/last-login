import {defineConfig,devices} from '@playwright/test';
import {existsSync,mkdirSync} from 'node:fs';
import path from 'node:path';
process.env.TMPDIR=path.resolve('.cache/tmp');
process.env.PLAYWRIGHT_BROWSERS_PATH=path.resolve('.cache/browsers');
mkdirSync(process.env.TMPDIR,{recursive:true});
const chrome='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const executablePath=process.env.CHROME_PATH||(existsSync(chrome)?chrome:undefined);
export default defineConfig({
  testDir:'./tests/e2e',outputDir:'./test-results/playwright',timeout:60000,fullyParallel:false,workers:1,
  reporter:[['list'],['html',{outputFolder:'playwright-report',open:'never'}]],
  use:{baseURL:'http://127.0.0.1:4173',viewport:{width:1440,height:900},screenshot:'only-on-failure',trace:'retain-on-failure',launchOptions:{executablePath,args:['--disable-crash-reporter','--disable-breakpad']}},
  projects:[{name:'chromium',use:{...devices['Desktop Chrome'],viewport:{width:1440,height:900}}},...(existsSync('/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge')?[{name:'edge',use:{...devices['Desktop Edge'],viewport:{width:1280,height:720},launchOptions:{executablePath:'/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',args:['--disable-crash-reporter','--disable-breakpad']}}}]:[])],
  webServer:{command:'npm run dev',url:'http://127.0.0.1:4173',reuseExistingServer:true,timeout:30000},
});
