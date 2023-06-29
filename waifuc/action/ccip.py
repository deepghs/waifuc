from enum import IntEnum
from typing import Iterator, Optional, List, Tuple

from hbutils.testing import disable_output
from imgutils.metrics import ccip_extract_feature, ccip_default_threshold, ccip_clustering, ccip_batch_differences

from .base import BaseAction
from ..model import ImageItem


class CCIPStatus(IntEnum):
    INIT = 0x1
    APPROACH = 0x2
    EVAL = 0x3


class CCIPAction(BaseAction):
    def __init__(self, min_val_count: int = 15, step: int = 5,
                 ratio_threshold: float = 0.6, cmp_threshold: float = 0.5, min_rematched: int = 10,
                 eps: Optional[float] = None, min_samples: Optional[int] = None,
                 model='ccip-caformer-24-randaug-pruned', threshold: Optional[float] = None):
        self.min_val_count = min_val_count
        self.step = step
        self.ratio_threshold = ratio_threshold
        self.cmp_threshold = cmp_threshold
        self.min_rematched = min_rematched
        self.eps, self.min_samples = eps, min_samples
        self.model = model
        self.threshold = threshold or ccip_default_threshold(self.model)

        self.items = []
        self.item_matches = []
        self.item_released = []
        self.feats = []
        self.status = CCIPStatus.INIT

    def _extract_feature(self, item: ImageItem):
        return ccip_extract_feature(item.image, model=self.model)

    def _try_cluster(self) -> bool:
        with disable_output():
            clu_ids = ccip_clustering(self.feats, method='optics', model=self.model,
                                      eps=self.eps, min_samples=self.min_samples)
        clu_counts = {}
        for id_ in clu_ids:
            if id_ != -1:
                clu_counts[id_] = clu_counts.get(id_, 0) + 1

        chosen_id = None
        for id_, count in clu_counts.items():
            if count >= len(self.items) * self.ratio_threshold:
                chosen_id = id_
                break

        if chosen_id is not None:
            self.items = [item for i, item in enumerate(self.items) if clu_ids[i] == chosen_id]
            self.item_matches = [0] * len(self.items)
            self.item_released = [False] * len(self.items)
            self.feats = [feat for i, feat in enumerate(self.feats) if clu_ids[i] == chosen_id]
            return True
        else:
            return False

    def _compare_to_exists(self, feat) -> Tuple[bool, List[int]]:
        diffs = ccip_batch_differences([feat, *self.feats], model=self.model)[0, 1:]
        matches = diffs <= self.threshold
        yes = matches.astype(float).mean() >= self.cmp_threshold
        matched_item_ids = [i for i in range(len(self.items)) if matches[i]]
        return yes, matched_item_ids

    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        if self.status == CCIPStatus.INIT:
            self.items.append(item)
            self.feats.append(self._extract_feature(item))

            if len(self.items) >= self.min_val_count:
                if self._try_cluster():
                    self.status = CCIPStatus.EVAL
                else:
                    self.status = CCIPStatus.APPROACH

        elif self.status == CCIPStatus.APPROACH:
            self.items.append(item)
            self.feats.append(self._extract_feature(item))

            if (len(self.items) - self.min_val_count) % self.step == 0:
                if self._try_cluster():
                    self.status = CCIPStatus.EVAL

        elif self.status == CCIPStatus.EVAL:
            feat = self._extract_feature(item)
            yes, matched_ids = self._compare_to_exists(feat)
            if yes:
                self.feats.append(feat)
                yield item

                for id_ in matched_ids:
                    self.item_matches[id_] += 1

                for i in range(len(self.items)):
                    if not self.item_released[i] and self.item_matches[i] >= self.min_rematched:
                        yield self.items[i]
                        self.item_released[i] = True

        else:
            raise ValueError(f'Unknown status for {self.__class__.__name__} - {self.status!r}.')

    def reset(self):
        self.items.clear()
        self.item_matches.clear()
        self.item_released.clear()
        self.feats.clear()
        self.status = CCIPStatus.INIT
