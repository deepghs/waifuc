import numpy as np
from imgutils.metrics import lpips_difference, lpips_extract_feature

from .base import BaseAction
from ..model import ImageItem

try:
    from typing import Literal, Dict, Iterator
except (ImportError, ModuleNotFoundError):
    from typing_extensions import Literal


class FeatureBucket:
    def __init__(self, threshold: float = 0.45, rtol=1.e-5, atol=1.e-8):
        self.threshold = threshold
        self.rtol, self.atol = rtol, atol
        self.features = []
        self.ratios = np.array([], dtype=float)

    def check_duplicate(self, feat, ratio: float):
        for id_ in np.where(np.isclose(self.ratios, ratio, rtol=self.rtol, atol=self.atol))[0]:
            exist_feat = self.features[id_.item()]
            if lpips_difference(exist_feat, feat) <= self.threshold:
                return True

        return False

    def add(self, feat, ratio: float):
        self.features.append(feat)
        self.ratios = np.append(self.ratios, ratio)


FilterSimilarModeTyping = Literal['all', 'group']


class FilterSimilarAction(BaseAction):
    def __init__(self, mode: FilterSimilarModeTyping, threshold: float = 0.45, rtol=1.e-5, atol=1.e-8):
        self.mode = mode
        self.buckets: Dict[str, FeatureBucket] = {}
        self.global_bucket = FeatureBucket()

    def _get_bin(self, group_id):
        if self.mode == 'all':
            return self.global_bucket
        elif self.mode == 'group':
            if group_id not in self.buckets:
                self.buckets[group_id] = FeatureBucket()

            return self.buckets[group_id]
        else:
            raise ValueError(f'Unknown mode for filter similar action - {self.mode!r}.')

    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        image = item.image
        ratio = image.height * 1.0 / image.width
        feat = lpips_extract_feature(image)
        bucket = self._get_bin(image.meta.get('group_id'))

        if not bucket.check_duplicate(feat, ratio):
            bucket.add(feat, ratio)
            yield item
