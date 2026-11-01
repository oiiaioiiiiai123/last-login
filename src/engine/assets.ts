/** Vite owns every runtime URL. Nothing is resolved against the current page path. */
const files = import.meta.glob<string>('/src/assets/**/*.{png,wav}', {
  eager: true, query: '?url', import: 'default',
});
const vectors = import.meta.glob<string>('/src/assets/**/*.svg', {
  eager: true, query: '?raw', import: 'default',
});
const registry: Record<string, string> = {};
for (const [key, url] of Object.entries(files)) registry[key.replace('/src/assets/', '')] = url;
for (const [key, xml] of Object.entries(vectors)) {
  const name = key.replace('/src/assets/', '');
  registry[name] = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(xml)}`;
}
export function asset(path: string): string {
  // Keep stable story identifiers while replacing the old editable SVG art with native pixels.
  const raster = path.replace(/\.svg$/, '.png');
  const url = registry[raster] ?? registry[path];
  if (!url) throw new Error(`Missing registered asset: ${path}`);
  return url;
}
export const imageAssets = Object.entries(registry)
  .filter(([key]) => /\.(png|svg)$/.test(key) && !(key.endsWith('.svg') && registry[key.replace(/\.svg$/, '.png')]))
  .map(([key, url]) => ({key, url}));
export const assetKeys = Object.keys(registry);
export async function preloadImages() {
  const results = await Promise.all(imageAssets.map(({key, url}) => new Promise<string|null>(resolve => {
    const image = new Image();
    image.onload = () => resolve(image.naturalWidth > 0 ? null : key);
    image.onerror = () => resolve(key);
    image.src = url;
  })));
  return results.filter((result): result is string => result !== null);
}
