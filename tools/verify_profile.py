#!/usr/bin/python3
"""Validate local image/document contracts without network calls."""
from pathlib import Path
import re
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / 'README.md').read_text()
for name in ['hero', 'workflow', 'systems']:
    animated = ROOT / 'assets' / (name+'.gif');still = ROOT / 'assets' / (name+'-static.png')
    with Image.open(animated) as im:
        assert im.n_frames == 48
        assert im.info['loop'] == 0 and im.info['duration'] == 100
        assert im.width == 1200 and im.height <= 400
        first = im.convert('RGB').copy();im.seek(20)
        assert first.tobytes() != im.convert('RGB').tobytes(), name
        for frame in range(im.n_frames):
            im.seek(frame)
            assert im.size == (1200, first.height)
            assert im.info.get('duration') == 100
            assert im.convert('RGB').getbbox(), (name, frame)
    with Image.open(still) as im:assert im.width == 1200
    assert animated.stat().st_size < 1_000_000
    assert f'src="./assets/{name}.gif"' in text and f'srcset="./assets/{name}-static.png"' in text
assert text.count('prefers-reduced-motion: reduce') == 3
for path in re.findall(r'(?:src|srcset)="(\./[^\"]+)"', text):assert (ROOT / path).is_file(), path
assert not re.search(r'<script|<iframe|javascript:|komarev|github-readme-stats|dribbble', text, re.I)
assert 'kaleab-taye.dev' in text and 'mailto:kaleabtaye@gmail.com' in text
assert len(re.findall(r'alt="[^\"]+"', text)) == 3
print('PASS: original 48-frame animations, reduced-motion images, bounds, links and script-free README')
