import os
from typing import Iterator, Optional

from imgutils.detect import detect_person, detect_heads, detect_halfbody, detect_eyes

from .base import BaseAction
from ..model import ImageItem


class PersonSplitAction(BaseAction):
    def __init__(self, keep_original: bool = False, level: str = 'm', version: str = 'v1.1',
                 conf_threshold: float = 0.3, iou_threshold: float = 0.5, keep_origin_tags: bool = False):
        self.keep_original = keep_original
        self.level = level
        self.version = version
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        self.keep_origin_tags = keep_origin_tags

    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        detection = detect_person(item.image, self.level, self.version,
                                  conf_threshold=self.conf_threshold, iou_threshold=self.iou_threshold)

        if 'filename' in item.meta:
            filename = item.meta['filename']
            filebody, ext = os.path.splitext(filename)
        else:
            filebody, ext = None, None

        if self.keep_original:
            yield item

        for i, (area, type_, score) in enumerate(detection):
            new_meta = {
                **item.meta,
                'crop': {'type': type_, 'score': score},
            }
            if 'tags' in new_meta and not self.keep_origin_tags:
                del new_meta['tags']
            if filebody is not None:
                new_meta['filename'] = f'{filebody}_person{i}{ext}'
            yield ImageItem(item.image.crop(area), new_meta)

    def reset(self):
        pass


class ThreeStageSplitAction(BaseAction):
    def __init__(self, person_conf: Optional[dict] = None, halfbody_conf: Optional[dict] = None,
                 head_conf: Optional[dict] = None, head_scale: float = 1.5,
                 split_eyes: bool = False, eye_conf: Optional[dict] = None, eye_scale: float = 2.4,
                 split_person: bool = True, keep_origin_tags: bool = False):
        self.person_conf = dict(person_conf or {})
        self.halfbody_conf = dict(halfbody_conf or {})
        self.head_conf = dict(head_conf or {})
        self.eye_conf = dict(eye_conf or {})
        self.head_scale = head_scale
        self.eye_scale = eye_scale
        self.split_eyes = split_eyes
        self.split_person = split_person
        self.keep_origin_tags = keep_origin_tags

    def _split_person(self, item: ImageItem, filebody, ext):
        if self.split_person:
            for i, (px, type_, score) in enumerate(detect_person(item.image, **self.person_conf), start=1):
                person_image = item.image.crop(px)
                person_meta = {
                    **item.meta,
                    'crop': {'type': type_, 'score': score},
                }
                if 'tags' in person_meta and not self.keep_origin_tags:
                    del person_meta['tags']
                if filebody is not None:
                    person_meta['filename'] = f'{filebody}_person{i}{ext}'
                yield i, ImageItem(person_image, person_meta)

        else:
            yield 1, item

    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        if 'filename' in item.meta:
            filename = item.meta['filename']
            filebody, ext = os.path.splitext(filename)
        else:
            filebody, ext = None, None

        for i, person_item in self._split_person(item, filebody, ext):
            person_image = person_item.image
            yield person_item

            half_detects = detect_halfbody(person_image, **self.halfbody_conf)
            if half_detects:
                halfbody_area, halfbody_type, halfbody_score = half_detects[0]
                halfbody_image = person_image.crop(halfbody_area)
                halfbody_meta = {
                    **item.meta,
                    'crop': {'type': halfbody_type, 'score': halfbody_score},
                }
                if 'tags' in halfbody_meta and not self.keep_origin_tags:
                    del halfbody_meta['tags']
                if filebody is not None:
                    halfbody_meta['filename'] = f'{filebody}_person{i}_halfbody{ext}'
                yield ImageItem(halfbody_image, halfbody_meta)

            head_detects = detect_heads(person_image, **self.head_conf)
            if head_detects:
                (hx0, hy0, hx1, hy1), head_type, head_score = head_detects[0]
                cx, cy = (hx0 + hx1) / 2, (hy0 + hy1) / 2
                width, height = hx1 - hx0, hy1 - hy0
                width = height = max(width, height) * self.head_scale
                x0, y0 = int(max(cx - width / 2, 0)), int(max(cy - height / 2, 0))
                x1, y1 = int(min(cx + width / 2, person_image.width)), int(min(cy + height / 2, person_image.height))
                head_image = person_image.crop((x0, y0, x1, y1))
                head_meta = {
                    **item.meta,
                    'crop': {'type': head_type, 'score': head_score},
                }
                if 'tags' in head_meta and not self.keep_origin_tags:
                    del head_meta['tags']
                if filebody is not None:
                    head_meta['filename'] = f'{filebody}_person{i}_head{ext}'
                yield ImageItem(head_image, head_meta)

                if self.split_eyes:
                    eye_detects = detect_eyes(head_image, **self.eye_conf)
                    for j, ((ex0, ey0, ex1, ey1), eye_type, eye_score) in enumerate(eye_detects):
                        cx, cy = (ex0 + ex1) / 2, (ey0 + ey1) / 2
                        width, height = ex1 - ex0, ey1 - ey0
                        width = height = max(width, height) * self.eye_scale
                        x0, y0 = int(max(cx - width / 2, 0)), int(max(cy - height / 2, 0))
                        x1, y1 = int(min(cx + width / 2, head_image.width)), \
                            int(min(cy + height / 2, head_image.height))
                        eye_image = head_image.crop((x0, y0, x1, y1))
                        eye_meta = {
                            **item.meta,
                            'crop': {'type': eye_type, 'score': eye_score},
                        }
                        if 'tags' in eye_meta and not self.keep_origin_tags:
                            del eye_meta['tags']
                        if filebody is not None:
                            eye_meta['filename'] = f'{filebody}_person{i}_head_eye{j}{ext}'
                        yield ImageItem(eye_image, eye_meta)

    def reset(self):
        pass
