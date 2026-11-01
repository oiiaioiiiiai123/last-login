"""Read-only checks for the protected Ivy master and Morrow artwork contract."""
from pathlib import Path
from PIL import Image, ImageChops
import hashlib, importlib.util
root=Path(__file__).resolve().parents[1]
module_spec=importlib.util.spec_from_file_location('asset_contract',root/'scripts/asset-contract.py')
contract_tools=importlib.util.module_from_spec(module_spec);module_spec.loader.exec_module(contract_tools)
contract=contract_tools.load_contract()
master=root/'art/character-style-reference/ivy-80.png'
hash_expected='698d220273b3459e2427b17cf8a6b6f7ec59d6f56ca34859853e99d385779de4'
assert hashlib.sha256(master.read_bytes()).hexdigest()==hash_expected
im=Image.open(master).convert('RGB');assert im.size==(80,80) and len(im.getcolors(6400))==48
for n in ['ivy','ivy-missing']:
 assert (root/f'src/assets/portraits/{n}.png').read_bytes()==master.read_bytes()
for n in ['maya','nora']:
 im=Image.open(root/f'src/assets/portraits/{n}.png').convert('RGB');assert im.size==(80,80)
 print(n, im.size, len(im.getcolors(6400)), 'colors')
base=Image.open(root/'src/assets/photos/train-selfie.png').convert('RGBA')
layer=Image.open(root/contract['morrow']['source_layer']).convert('RGBA')
result=Image.open(root/'src/assets/endings/train-selfie-nora.png').convert('RGBA')
assert base.size==layer.size==result.size==(376,426)
old=Image.open(root/contract['morrow']['original_selfie']).convert('RGB')
assert ImageChops.difference(base.crop((0,0,320,426)).convert('RGB'),old).getbbox() is None, 'Original selfie changed'
ivy=Image.open(root/contract['morrow']['ivy_mask']).convert('L')
assert ImageChops.multiply(layer.getchannel('A').crop((0,0,320,426)),ivy).getbbox() is None, 'Nora overlaps Ivy'

assert layer.getchannel('A').getbbox()[0]>=175
assert ImageChops.difference(Image.alpha_composite(base,layer).convert('RGB'),result.convert('RGB')).getbbox() is None
outside=ImageChops.invert(layer.getchannel('A').point(lambda a:255 if a else 0))
assert ImageChops.multiply(ImageChops.difference(base.convert('RGB'),result.convert('RGB')).convert('L'),outside).getbbox() is None
pixels=iter(layer.crop((175,0,376,240)).tobytes())
assert any(a and g>r*1.08 and g>b*1.05 for r,g,b,a in zip(pixels,pixels,pixels,pixels)), 'No green iris pixels in Nora head region'
images,mask=contract_tools.read_reveal(contract)
box=contract_tools.check_reveal(images,contract,mask)
for key in ['base','final','outline','clothes','face']:
    rel=contract['morrow'][key]
    assert (root/'art/curated'/rel).read_bytes()==(root/'src/assets'/rel).read_bytes(), f'Curated copy differs: {rel}'
ending=(root/'src/components/ending.tsx').read_text()
assert 'DATE: DEC 17, 2024' in ending and 'LOCATION: MORROW' in ending, 'Ending metadata changed'
photo_source=(root/'src/content/photos.ts').read_text()
assert 'train-selfie-nora' not in photo_source, 'Normal album references the Morrow alternate photo'
print(f'Authoritative Nora layer: {contract["morrow"]["source_layer"]}; alpha bounds: {box}')
print('PASS: approved Ivy 80x80 / 48 colors unchanged; original selfie and Ivy mask protected; complete Nora source, outline, complementary reveal parts, curated copies and final photo agree. This is structural verification, not artistic approval.')
