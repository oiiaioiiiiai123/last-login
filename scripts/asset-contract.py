"""Shared, read-only production-art checks. Historical review files are inputs only."""
from pathlib import Path
import json
import hashlib
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]


def load_contract():
    return json.loads((ROOT / 'scripts/asset-manifest.json').read_text())


def exact_inventory(expected, actual):
    missing, unexpected = set(expected) - set(actual), set(actual) - set(expected)
    assert not missing and not unexpected, f'Asset inventory mismatch: missing={sorted(missing)}, unexpected={sorted(unexpected)}'


def pixel_difference(a, b):
    assert a.size == b.size, f'Canvas sizes differ: {a.size} / {b.size}'
    return ImageChops.difference(a.convert('RGB'), b.convert('RGB'))


def delta_mask(a, b):
    channels = pixel_difference(a, b).split()
    return ImageChops.lighter(ImageChops.lighter(channels[0], channels[1]), channels[2]).point(lambda v: 255 if v else 0)


def check_reveal(images, contract, ivy_mask):
    spec = contract['morrow']
    base, layer, final = (images[k] for k in ['base', 'source_layer', 'final'])
    size = tuple(spec['size'])
    for name, im in images.items():
        assert im.size == size, f'{name}: wrong reveal canvas {im.size}, expected {size}'
    assert layer.mode == 'RGBA', 'Nora source must have RGBA transparency'
    alpha = layer.getchannel('A')
    box = alpha.getbbox()
    assert box and box[0] >= spec['minimum_nora_x'], 'Nora is missing or outside the right-hand seat'
    assert alpha.getextrema() == (0, 255), 'Nora requires transparent background and an opaque interior'
    assert hashlib.sha256(alpha.tobytes()).hexdigest() == spec['approved_alpha_sha256'], 'Nora alpha differs from the approved LIGHT edge treatment'
    assert hashlib.sha256(layer.tobytes()).hexdigest() == spec['approved_layer_pixels_sha256'], 'Nora pixels differ from the approved A / LIGHT master'
    assert ivy_mask.size == (320, 426), 'Protected Ivy mask has wrong dimensions'
    assert ImageChops.multiply(alpha.crop((0, 0, 320, 426)), ivy_mask).getbbox() is None, 'Nora overlaps protected Ivy pixels'
    change = delta_mask(base, final)
    support = alpha.point(lambda a: 255 if a else 0)
    assert ImageChops.multiply(change, ImageChops.invert(support)).getbbox() is None, 'Final image changes the background outside Nora'
    assert ImageChops.multiply(change.crop((0, 0, 320, 426)), ivy_mask).getbbox() is None, 'Final image changes Ivy'
    assert pixel_difference(Image.alpha_composite(base.convert('RGBA'), layer), final).getbbox() is None, 'Authoritative Nora layer does not reproduce the final photo'
    for name in ['outline', 'clothes', 'face']:
        assert images[name].mode == 'RGBA', f'{name}: alpha channel missing'
    assert images['outline'].getchannel('A').tobytes() == alpha.tobytes(), 'Outline silhouette does not match Nora'
    outline = images['outline']
    data = iter(outline.tobytes())
    for rgba in zip(data, data, data, data):
        if rgba[3]:
            assert rgba[:3] == (32, 35, 54), 'Outline color differs from the established reveal'
    split = spec['face_boundary_y']
    for name, top, bottom in [('face', 0, split), ('clothes', split, size[1])]:
        expected_alpha = Image.new('L', size)
        expected_alpha.paste(alpha.crop((0, top, size[0], bottom)), (0, top))
        part = images[name]
        assert expected_alpha.getbbox(), f'{name}: source part is empty'
        assert part.getchannel('A').tobytes() == expected_alpha.tobytes(), f'{name}: shifted, missing or overlapping alpha pixels'
        assert ImageChops.multiply(delta_mask(part, layer), expected_alpha).getbbox() is None, f'{name}: colors differ from complete Nora layer'
    combined = Image.alpha_composite(images['clothes'], images['face'])
    assert combined.getchannel('A').tobytes() == alpha.tobytes(), 'Reveal parts do not cover the full Nora silhouette'
    assert ImageChops.multiply(delta_mask(combined, layer), alpha).getbbox() is None, 'Reveal parts are inconsistent with Nora source'
    developed = base.convert('RGBA')
    # The existing CSS fades outline to zero before the final image. With the
    # approved semitransparent LIGHT edge, a full-opacity outline underneath
    # would double the edge coverage; it is not a terminal animation state.
    for name in ['clothes', 'face']:
        developed = Image.alpha_composite(developed, images[name])
    assert pixel_difference(developed, final).getbbox() is None, 'Terminal reveal (outline faded) does not reproduce the final photo'
    return box


def read_reveal(contract):
    result = {}
    for key in ['base', 'final', 'outline', 'clothes', 'face', 'source_layer']:
        rel = contract['morrow'][key]
        path = ROOT / rel if key == 'source_layer' else ROOT / 'src/assets' / rel
        assert path.is_file(), f'Missing reveal input: {path.relative_to(ROOT)}'
        with Image.open(path) as im:
            im.load()
            result[key] = im.copy()
    mask_path = ROOT / contract['morrow']['ivy_mask']
    assert mask_path.is_file(), 'Protected Ivy mask missing'
    return result, Image.open(mask_path).convert('L')
