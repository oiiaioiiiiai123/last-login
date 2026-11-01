"""Negative cases for the asset checks; all damaged images exist only in memory."""
import importlib.util
from pathlib import Path
import unittest
from PIL import Image, ImageChops

root = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('asset_contract', root / 'scripts/asset-contract.py')
checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checks)


class AssetValidationTests(unittest.TestCase):
    def setUp(self):
        self.contract = checks.load_contract()
        self.images, self.ivy = checks.read_reveal(self.contract)

    def test_current_reveal_is_valid(self):
        checks.check_reveal(self.images, self.contract, self.ivy)

    def test_missing_photo_is_rejected(self):
        expected = self.contract['assets']
        actual = set(expected) - {'photos/train-selfie.png'}
        with self.assertRaisesRegex(AssertionError, 'missing='):
            checks.exact_inventory(expected, actual)

    def test_review_image_in_production_is_rejected(self):
        expected = self.contract['assets']
        with self.assertRaisesRegex(AssertionError, 'unexpected='):
            checks.exact_inventory(expected, set(expected) | {'photos/review-comparison.png'})

    def test_wrong_canvas_size_is_rejected(self):
        self.images['face'] = self.images['face'].crop((0, 0, 375, 426))
        with self.assertRaisesRegex(AssertionError, 'wrong reveal canvas'):
            checks.check_reveal(self.images, self.contract, self.ivy)

    def test_shifted_reveal_is_rejected(self):
        self.images['clothes'] = ImageChops.offset(self.images['clothes'], 1, 0)
        with self.assertRaisesRegex(AssertionError, 'alpha pixels'):
            checks.check_reveal(self.images, self.contract, self.ivy)

    def test_missing_lower_body_is_rejected(self):
        self.images['clothes'] = Image.new('RGBA', (376, 426))
        with self.assertRaisesRegex(AssertionError, 'alpha pixels'):
            checks.check_reveal(self.images, self.contract, self.ivy)

    def test_background_change_is_rejected(self):
        self.images['final'].putpixel((0, 0), (255, 0, 0))
        with self.assertRaisesRegex(AssertionError, 'background outside Nora'):
            checks.check_reveal(self.images, self.contract, self.ivy)

    def test_unapproved_full_nora_layer_is_rejected(self):
        self.images['source_layer'].putpixel((250, 180), (255, 0, 0, 255))
        with self.assertRaisesRegex(AssertionError, 'approved A / LIGHT master'):
            checks.check_reveal(self.images, self.contract, self.ivy)

    def test_approved_soft_alpha_cannot_be_replaced_by_hard_edges(self):
        layer = self.images['source_layer']
        layer.putalpha(layer.getchannel('A').point(lambda a:255 if a else 0))
        with self.assertRaisesRegex(AssertionError, 'approved LIGHT edge treatment'):
            checks.check_reveal(self.images, self.contract, self.ivy)


if __name__ == '__main__':
    unittest.main(verbosity=2)
