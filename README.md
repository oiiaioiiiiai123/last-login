# LAST LOGIN

**A Pixel Mystery on a Night Train**

一款像素风格的心理悬疑叙事游戏。Nora 在回家的夜间列车上打开一台二手电脑，开始浏览前任主人 Ivy 留下的照片、便签与聊天记录。

[公开试玩](https://oiiaioiiiiai123.github.io/last-login/) · [GitHub 仓库](https://github.com/oiiaioiiiiai123/last-login)

## 玩法

自由探索 Files、Notes、Messages、Photos、Browser 五款桌面软件，阅读旧资料、查看 18 张照片、检索保存在电脑中的网页。资料与环境可能随着探索发生变化；两种结局取决于你的调查。没有固定倒计时强制结束旅程，可通过桌面“收起电脑”准备到站。

- 鼠标单击软件图标；Files 双击文件或选中后按 Enter 打开。
- Photos 支持左右方向键和 Esc；程序窗口可拖动、最小化和关闭。
- MENU 或 Esc 可暂停，调整音量、文字大小和减少动态效果。
- Continue 恢复当前浏览器里的存档；New Game 重置当前旅程，保留已完成结局。

建议使用桌面 Chrome 或 Edge，并佩戴耳机。存档只保存在当前浏览器、当前网址的 localStorage 中；清除浏览器数据或更换网址/浏览器可能无法继续原进度。游戏只显示虚构的电脑文件，不读取玩家真实电脑上的私人文件。

## 本地运行

需要 Node.js 22.12+ 或兼容的受支持版本；部署工作流使用 Node.js 24 LTS。

```sh
npm ci
npm run dev
```

访问终端显示的本机网址，默认 `http://127.0.0.1:4173/`。

```sh
npm run typecheck
npm test
npm run build
npm run preview
```

默认构建生成独立单文件 `dist/index.html`，图片、字体、表情及广播均内嵌，可直接离线打开这个文件。请保留其完整内容，不需要后端、账号或在线搜索服务。

## 测试与素材校验

```sh
npm run test:e2e
PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify-assets.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify-character-style.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-asset-validation.py
```

浏览器测试优先寻找本机 Chrome，安装本机 Edge 时也会覆盖 Edge；其他环境可以设置 `CHROME_PATH`。没有浏览器时，将 Playwright 下载和临时目录放在项目内：

```sh
mkdir -p .cache/browsers .cache/tmp
PLAYWRIGHT_BROWSERS_PATH="$PWD/.cache/browsers" TMPDIR="$PWD/.cache/tmp" npx playwright install chromium
npm run test:e2e
```

Python 素材检查需要 Pillow、fontTools 和 Brotli，可在项目内虚拟环境安装。明确资源清单在 `scripts/asset-manifest.json`；角色基准及已确认的 A / LIGHT 完整人物、合照和显影母版在 `art/`。正常相册保持单人自拍，结局使用独立图层。不要运行历史生成工具替换已经确认的美术。

浏览器自动化和真实 UI 操作不等同真人首次体验；20–30 分钟自然游玩、真实 Safari 和真实手机仍未完成专门验收。

## GitHub Pages 部署

独立项目站点路径为 `/last-login/`，不使用个人主页仓库。`.github/workflows/deploy.yml` 在推送 `main` 或 Actions 手动运行时执行 `npm ci`、单元测试、生产构建和官方 Pages 部署。

仓库 Settings → Pages 的 Source 使用 **GitHub Actions**。后续修改后提交并推送到 `main`，即可自动重新部署；请在 Actions 确认部署成功后再检查公开网页。

工作流通过环境变量设置仓库名对应的 base，本地默认仍为 `./`，保持离线使用。手动检查相同子路径构建可执行：

```sh
VITE_BASE_PATH=/last-login/ npm run build
```

若仓库改名，工作流会按新仓库名设置 base；README 中的试玩链接也应同步更新。此游戏没有客户端多页路由，主页面刷新和 Continue 都从项目根入口进入。

## 技术栈与素材来源

React 19、TypeScript、Vite、Canvas、Web Audio、Vitest、Playwright。运行时资源通过 Vite 注册并内嵌，不依赖站点根目录下的 `/assets/` 文件。

人物与场景包含程序像素绘制、经确认的图像生成候选及本地像素处理/合成；不宣称全部为手工逐像素绘制。字体使用 Fusion Pixel zh-Hans（SIL OFL 1.1），聊天表情为 Google Noto Emoji（Apache 2.0），许可原文保存在 `docs/licenses/`。环境音与系统音由程序合成，中文到站广播为本地系统语音生成的 WAV。

[素材来源说明](docs/asset-sources.md)。原创游戏代码、文字与美术未另行指定开源许可证；公开访问及源码可见不代表额外授予再分发许可。第三方资源按各自许可证使用。
