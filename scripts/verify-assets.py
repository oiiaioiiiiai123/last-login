"""Read-only validation of current art, font coverage, licenses, audio and offline build."""
from pathlib import Path
import base64, hashlib, importlib.util, re, wave, sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'.cache/python'))
from PIL import Image, ImageChops
from fontTools.ttLib import TTFont
root=Path(__file__).resolve().parents[1]
module_spec=importlib.util.spec_from_file_location('asset_contract',root/'scripts/asset-contract.py')
contract_tools=importlib.util.module_from_spec(module_spec);module_spec.loader.exec_module(contract_tools)
contract=contract_tools.load_contract()
assets=root/'src/assets'
actual={str(p.relative_to(assets)):p for p in assets.rglob('*') if p.is_file()}
contract_tools.exact_inventory(contract['assets'],actual)
photos=sorted((assets/'photos').glob('*.png'))
assert len(photos)==18
assert len({hashlib.sha256(p.read_bytes()).hexdigest() for p in photos})==18
images=[p for rel,p in actual.items() if contract['assets'][rel]['kind']=='png']
assert len(images)==51, 'Update the explicit manifest and this reviewed PNG total together'
for rel,p in actual.items():
    expected=contract['assets'][rel]
    if 'sha256' in expected:
        assert hashlib.sha256(p.read_bytes()).hexdigest()==expected['sha256'], f'Protected asset bytes changed: {rel}'
for p in images:
    expected=contract['assets'][str(p.relative_to(assets))]
    with Image.open(p) as image:
        image.load()
        assert image.size==tuple(expected['size']), f'Wrong asset dimensions: {p.name}'
        assert image.mode==expected['mode'], f'Wrong asset mode: {p.name}'
        if p.parent.name in ['sprites','icons']:assert image.mode=='RGBA' and image.getextrema()[3][0]==0
reveal,ivy_mask=contract_tools.read_reveal(contract)
box=contract_tools.check_reveal(reveal,contract,ivy_mask)
source_files=[p for p in (root/'src').rglob('*') if p.suffix in ['.tsx','.ts','.css']]
for p in source_files:
    for rel in re.findall(r"['\"]((?:photos|icons|portraits|sprites|endings|scenes|scenery|audio|emoji|fonts)/[a-z0-9_.-]+\.(?:png|svg|wav|woff2))['\"]",p.read_text()):
        registered=rel[:-4]+'.png' if rel.endswith('.svg') and rel[:-4]+'.png' in actual else rel
        assert registered in actual, f'Unregistered asset path in {p.relative_to(root)}: {rel}'
photo_ids=re.findall(r"\{id:'([^']+)'",(root/'src/content/photos.ts').read_text())
assert len(photo_ids)==18 and {f'photos/{name}.png' for name in photo_ids}=={str(p.relative_to(assets)) for p in photos}, 'Dynamic photo paths and production inventory disagree'
for p in (assets/'emoji').glob('*.svg'):
    import xml.etree.ElementTree as ET
    assert ET.parse(p).getroot().tag.endswith('svg'), f'Invalid SVG: {p.name}'
source=''.join(p.read_text() for p in (root/'src').rglob('*') if p.suffix in ['.tsx','.ts','.css'])
chinese={ord(c) for c in source if '\u4e00'<=c<='\u9fff'}
for p in (assets/'fonts').glob('*.woff2'):
    font=TTFont(p);cmap=font.getBestCmap();missing=chinese-set(cmap)
    assert not missing,f'{p.name} missing: {"".join(map(chr,missing))}'
    print(f'{p.name}: {len(chinese)} Chinese codepoints covered')
for name in ['fusion-pixel-ofl.txt','noto-emoji-apache.txt']:
    assert (root/'docs/licenses'/name).stat().st_size>1000
for destination in ['morrow','larkfield']:
    with wave.open(str(assets/f'audio/{destination}-arrival.wav'),'rb') as wav:
        duration=wav.getnframes()/wav.getframerate();assert duration>3
        print(f'{destination} broadcast: {duration:.2f}s')
html=(root/'dist/index.html').read_text()
for rel,p in actual.items():
    if p.suffix in {'.png','.wav','.woff2'}:
        assert base64.b64encode(p.read_bytes()).decode() in html, f'Current resource bytes missing from dist (rebuild required): {rel}'
    elif p.suffix=='.svg':
        assert rel in html, f'Emoji registry key missing from dist: {rel}'
assert not re.search(r'<script[^>]+\bsrc=',html),'Production scripts must be inline'
assert not re.search(r'<link[^>]+href="(?!data:)',html),'Production CSS/favicon must be inline'
assert not re.search(r'url\(["\']?(?!data:)[./]',html),'Runtime CSS assets must be embedded'
assert 'SIL OPEN FONT LICENSE' in html and 'Apache License' in html
retained=[key for key,value in contract['assets'].items() if value['usage']=='preloaded-only']
print(f'Inventory: {len(actual)} production resources in src/assets; {len(retained)} retained/preloaded-only PNGs; historical and review directories excluded.')
print(f'PASS: {len(images)} PNGs; 18 unique photos; exact inventory/dimensions/protected hashes; current reveal {box}; six emoji; three fonts; all current binary assets embedded in standalone HTML {len(html.encode()):,} bytes.')
