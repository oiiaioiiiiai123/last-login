"""Restore the approved A / LIGHT reveal from its immutable local masters.

Only four ending images are written. No other photo, scene or story is rebuilt.
"""
from pathlib import Path
import hashlib
import json
import shutil
from PIL import Image, ImageChops

r=Path(__file__).resolve().parents[1]
master=r/'art/morrow-selfie'
approval=json.loads((master/'approved-a-light.json').read_text())
base=Image.open(r/'src/assets/photos/train-selfie.png').convert('RGBA')
layer=Image.open(master/'nora-a-light.png').convert('RGBA')
assert hashlib.sha256((master/'nora-a-light.png').read_bytes()).hexdigest()==approval['files']['nora.png']
assert hashlib.sha256((r/'src/assets/photos/train-selfie.png').read_bytes()).hexdigest()==approval['base_sha256']
final=Image.open(master/'final-a-light.png').convert('RGB')
assert ImageChops.difference(Image.alpha_composite(base,layer).convert('RGB'),final).getbbox() is None
for name,top,bottom in [('reveal-face',0,265),('reveal-clothes',265,426)]:
    expected_alpha=Image.new('L',base.size)
    expected_alpha.paste(layer.getchannel('A').crop((0,top,376,bottom)),(0,top))
    part=Image.open(master/(name+'.png')).convert('RGBA')
    assert part.getchannel('A').tobytes()==expected_alpha.tobytes()
    difference=ImageChops.difference(part.convert('RGB'),layer.convert('RGB'))
    assert ImageChops.multiply(difference.convert('L'),expected_alpha).getbbox() is None
for source,target,key in [('final-a-light.png','train-selfie-nora.png','final.png'),('reveal-outline.png','reveal-outline.png','reveal-outline.png'),('reveal-clothes.png','reveal-clothes.png','reveal-clothes.png'),('reveal-face.png','reveal-face.png','reveal-face.png')]:
    assert hashlib.sha256((master/source).read_bytes()).hexdigest()==approval['files'][key]
    for folder in ['src/assets/endings','art/curated/endings']:
        shutil.copyfile(master/source,r/folder/target)
print('Restored exact approved A / LIGHT files; original Ivy selfie and all other assets untouched.')
