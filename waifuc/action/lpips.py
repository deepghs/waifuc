from typing import Dict, Iterator, Literal

import numpy as np
from imgutils.metrics import lpips_difference, lpips_extract_feature

from .base import BaseAction
from ..model import ImageItem


class FeatureBucket:
    def __init__(self, threshold: float = 0.45, capacity: int = 500, rtol=1.e-5, atol=1.e-8):
        self.threshold = threshold
        self.rtol, self.atol = rtol, atol
        self.features = []
        self.ratios = np.array([], dtype=float)
        self.capacity = capacity

    def check_duplicate(self, feat, ratio: float):
        for id_ in np.where(np.isclose(self.ratios, ratio, rtol=self.rtol, atol=self.atol))[0]:
            exist_feat = self.features[id_.item()]
            if lpips_difference(exist_feat, feat) <= self.threshold:
                return True

        return False

    def add(self, feat, ratio: float):
        self.features.append(feat)
        self.ratios = np.append(self.ratios, ratio)
        if len(self.features) >= self.capacity * 2:
            self.features = self.features[-self.capacity:]
            self.ratios = self.ratios[-self.capacity:]


FilterSimilarModeTyping = Literal['all', 'group']


class FilterSimilarAction(BaseAction):
    def __init__(self, mode: FilterSimilarModeTyping = 'all', threshold: float = 0.45,
                 capacity: int = 500, rtol=5.e-2, atol=2.e-2):
        self.mode = mode
        self.threshold, self.rtol, self.atol = threshold, rtol, atol
        self.capacity = capacity
        self.buckets: Dict[str, FeatureBucket] = {}
        self.global_bucket = FeatureBucket(threshold, self.capacity, rtol, atol)

    def _get_bin(self, group_id):
        if self.mode == 'all':
            return self.global_bucket
        elif self.mode == 'group':
            if group_id not in self.buckets:
                self.buckets[group_id] = FeatureBucket(self.threshold, self.capacity, self.rtol, self.atol)

            return self.buckets[group_id]
        else:
            raise ValueError(f'Unknown mode for filter similar action - {self.mode!r}.')

    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        image = item.image
        ratio = image.height * 1.0 / image.width
        feat = lpips_extract_feature(image)
        bucket = self._get_bin(item.meta.get('group_id'))

        if not bucket.check_duplicate(feat, ratio):
            bucket.add(feat, ratio)
            yield item

    def reset(self):
        self.buckets.clear()
        self.global_bucket = FeatureBucket(self.threshold, self.capacity, self.rtol, self.atol)
