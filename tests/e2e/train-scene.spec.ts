import {test,expect} from '@playwright/test';
import {readFile} from 'node:fs/promises';

test('first-frame-hidden-window-and-return',async({page})=>{
 await page.goto('/');await page.getByRole('button',{name:/New Game/}).click();
 await expect(page.locator('.train-world-forward canvas')).toHaveAttribute('data-scene','exterior');
 await expect(page.getByRole('button',{name:/look up|抬头|看窗外/i})).toHaveCount(0);
 await page.locator('.train-world-forward canvas').click({position:{x:35,y:140}});
 await expect(page.getByRole('button',{name:'笔记本电脑',exact:true})).toBeVisible();
 await expect(page.getByTestId('game')).toHaveClass(/looking-up/);
 await expect(page.locator('.train-world-left')).toHaveCSS('opacity','1');
 await page.getByRole('button',{name:'笔记本电脑',exact:true}).click();
 await expect(page.getByTestId('game')).not.toHaveClass(/looking-up/);
 for(let i=0;i<4;i++)await page.getByRole('button',{name:/继续 ↵/}).click();
 await expect(page.getByTestId('laptop')).toBeVisible();
 await page.locator('.train-world-forward canvas').click({position:{x:35,y:140}});
 await expect(page.getByRole('button',{name:'笔记本电脑',exact:true})).toBeVisible();
 await page.getByRole('button',{name:'笔记本电脑',exact:true}).click();
 await expect(page.getByRole('button',{name:'打开 Browser',exact:true})).toBeVisible();
});

test('confirmed-save-does-not-end-before-player-finishes-exploring',async({page})=>{
 const raw=await readFile('tests/fixtures/confirmed-investigation.json','utf8');
 await page.clock.install();await page.addInitScript(value=>localStorage.setItem('last-login.save.v1',value),raw);
 await page.goto('/');await page.getByRole('button',{name:/Continue/}).click();
 await page.clock.fastForward(31*60*1000);
 const state=await page.evaluate(()=>JSON.parse(localStorage.getItem('last-login.save.v1')!));
 expect(state.morrowConfirmed).toBe(true);expect(state.ending).toBeNull();
 await expect(page.getByTestId('morrow-approach')).toHaveCount(0);
 await page.getByRole('button',{name:'打开 Notes',exact:true}).click();
 await expect(page.getByRole('dialog',{name:'Notes',exact:true})).toBeVisible();
});


test('new-game-resets-saved-investigation-after-confirmation',async({page})=>{
 const raw=await readFile('tests/fixtures/confirmed-investigation.json','utf8');
 await page.addInitScript(value=>localStorage.setItem('last-login.save.v1',value),raw);
 await page.goto('/');await page.getByRole('button',{name:/Continue/}).click();
 await page.getByRole('button',{name:'暂停与设置'}).click();await page.getByRole('button',{name:'保存并回到主菜单'}).click();
 await page.getByRole('button',{name:/New Game/}).click();await page.getByRole('dialog',{name:'新旅程'}).getByRole('button',{name:'开始新旅程'}).click();
 await expect.poll(async()=>page.evaluate(()=>JSON.parse(localStorage.getItem('last-login.save.v1')!).morrowSearchCount)).toBe(0);
 const state=await page.evaluate(()=>JSON.parse(localStorage.getItem('last-login.save.v1')!));
 expect(state.changedSources).toEqual([]);expect(state.morrowConfirmed).toBe(false);expect(state.ending).toBeNull();
});

test('window-landscape-moves-naturally',async({page})=>{
 await page.goto('/');await page.getByRole('button',{name:/New Game/}).click();
 await page.locator('.train-world-forward canvas').click({position:{x:35,y:140}});
 await expect(page.locator('.train-world-left')).toHaveCSS('opacity','1');
 const canvas=page.locator('.train-world-left canvas');const before=await canvas.screenshot();
 await page.waitForTimeout(1200);const after=await canvas.screenshot();
 expect(before.equals(after)).toBe(false);
});
