import logging
from enum import IntEnum
from typing import Iterator, Optional, List, Tuple

import numpy as np
from hbutils.string import plural_word
from hbutils.testing import disable_output
from imgutils.metrics import ccip_extract_feature, ccip_default_threshold, ccip_clustering, ccip_batch_differences

from .base import BaseAction
from ..model import ImageItem


class CCIPStatus(IntEnum):
    INIT = 0x1
    APPROACH = 0x2
    EVAL = 0x3
    INIT_WITH_SOURCE = 0x4


class CCIPAction(BaseAction):
    def __init__(self, init_source=None, *, min_val_count: int = 15, step: int = 5,
                 ratio_threshold: float = 0.6, min_clu_dump_ratio: float = 0.3, cmp_threshold: float = 0.5,
                 eps: Optional[float] = None, min_samples: Optional[int] = None,
                 model='ccip-caformer-24-randaug-pruned', threshold: Optional[float] = None):
        self.init_source = init_source

        self.min_val_count = min_val_count
        self.step = step
        self.ratio_threshold = ratio_threshold
        self.min_clu_dump_ratio = min_clu_dump_ratio
        self.cmp_threshold = cmp_threshold
        self.eps, self.min_samples = eps, min_samples
        self.model = model
        self.threshold = threshold or ccip_default_threshold(self.model)

        self.items = []
        self.item_released = []
        self.feats = []
        if self.init_source is not None:
            self.status = CCIPStatus.INIT_WITH_SOURCE
        else:
            self.status = CCIPStatus.INIT

    def _extract_feature(self, item: ImageItem):
        if 'ccip_feature' in item.meta:
            return item.meta['ccip_feature']
        else:
            return ccip_extract_feature(item.image, model=self.model)

    def _try_cluster(self) -> bool:
        with disable_output():
            clu_ids = ccip_clustering(self.feats, method='optics', model=self.model,
                                      eps=self.eps, min_samples=self.min_samples)
        clu_counts = {}
        for id_ in clu_ids:
            if id_ != -1:
                clu_counts[id_] = clu_counts.get(id_, 0) + 1

        clu_total = sum(clu_counts.values()) if clu_counts else 0
        chosen_id = None
        for id_, count in clu_counts.items():
            if count >= clu_total * self.ratio_threshold:
                chosen_id = id_
                break

        if chosen_id is not None:
            feats = [feat for i, feat in enumerate(self.feats) if clu_ids[i] == chosen_id]
            clu_dump_ratio = np.array([
                self._compare_to_exists(feat, base_set=feats)
                for feat in feats
            ]).astype(float).mean()

            if clu_dump_ratio >= self.min_clu_dump_ratio:
                self.items = [item for i, item in enumerate(self.items) if clu_ids[i] == chosen_id]
                self.item_released = [False] * len(self.items)
                self.feats = [feat for i, feat in enumerate(self.feats) if clu_ids[i] == chosen_id]
                return True
            else:
                return False
        else:
            return False

    def _compare_to_exists(self, feat, base_set=None) -> Tuple[bool, List[int]]:
        diffs = ccip_batch_differences([feat, *(base_set or self.feats)], model=self.model)[0, 1:]
        matches = diffs <= self.threshold
        return matches.astype(float).mean() >= self.cmp_threshold

    def _dump_items(self) -> Iterator[ImageItem]:
        for i in range(len(self.items)):
            if not self.item_released[i]:
                if self._compare_to_exists(self.feats[i]):
                    self.item_released[i] = True
                    yield self.items[i]

    def _eval_iter(self, item: ImageItem) -> Iterator[ImageItem]:
        feat = self._extract_feature(item)
        if self._compare_to_exists(feat):
            self.feats.append(feat)
            yield item

            if (len(self.feats) - len(self.items)) % self.step == 0:
                yield from self._dump_items()

    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        if self.status == CCIPStatus.INIT_WITH_SOURCE:
            cnt = 0
            logging.info('Existing anchor detected.')
            for item in self.init_source:
                self.feats.append(self._extract_feature(item))
                yield item
                cnt += 1
            logging.info(f'{plural_word(cnt, "items")} loaded from anchor.')

            self.status = CCIPStatus.EVAL
            yield from self._eval_iter(item)

        elif self.status == CCIPStatus.INIT:
            self.items.append(item)
            self.feats.append(self._extract_feature(item))

            if len(self.items) >= self.min_val_count:
                if self._try_cluster():
                    self.status = CCIPStatus.EVAL
                    yield from self._dump_items()
                else:
                    self.status = CCIPStatus.APPROACH

        elif self.status == CCIPStatus.APPROACH:
            self.items.append(item)
            self.feats.append(self._extract_feature(item))

            if (len(self.items) - self.min_val_count) % self.step == 0:
                if self._try_cluster():
                    self.status = CCIPStatus.EVAL
                    yield from self._dump_items()

        elif self.status == CCIPStatus.EVAL:
            yield from self._eval_iter(item)

        else:
            raise ValueError(f'Unknown status for {self.__class__.__name__} - {self.status!r}.')

    def reset(self):
        self.items.clear()
        self.item_released.clear()
        self.feats.clear()
        if self.init_source:
            self.status = CCIPStatus.INIT_WITH_SOURCE
        else:
            self.status = CCIPStatus.INIT
