import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import {viteSingleFile} from 'vite-plugin-singlefile';
export default defineConfig({
  plugins: [react({include:/\/src\/.*\.[jt]sx?$/}), viteSingleFile({removeViteModuleLoader:true,overrideConfig:{base:process.env.VITE_BASE_PATH||'./'}})],
  build:{assetsInlineLimit:()=>true}, base: process.env.VITE_BASE_PATH || './', cacheDir: '.cache/vite',
  test: {include: ['tests/**/*.test.ts'], coverage: {reportsDirectory: './test-results/coverage'}},
  server: {host: '127.0.0.1', port: 4173, strictPort: true, watch:{ignored:['**/.cache/**','**/test-results/**','**/playwright-report/**']}},
});
