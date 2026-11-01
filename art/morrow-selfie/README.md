# Approved selfie artwork

The project owner selected **A / LIGHT** on 2026-11-01. These are the full-size approved artwork files, not review-sheet thumbnails.

- `nora-a-light.png`: complete independent Nora layer, including its approved lightly softened alpha edges.
- `final-a-light.png`: exact approved composite on the unchanged Ivy selfie.
- `reveal-outline.png`, `reveal-clothes.png`, `reveal-face.png`: matching reveal layers.
- `ivy-protection-mask.png`, `ivy-original-320.png`: small preservation inputs used by the read-only validators.
- `approved-a-light.json`: exact approved image and alpha signatures.

The existing single-person photo stays in `src/assets/photos/train-selfie.png`. Run `python3 scripts/build-nora-reveal.py` only to restore the four approved ending files to the runtime and curated copies. It does not redraw or replace any other scene.

The outline fades out before the terminal image. The clothes and face layers combine to the approved full Nora layer; keeping a full-opacity outline underneath a partially transparent LIGHT edge would change its coverage and is not the actual animation's final state.
