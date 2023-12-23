from typing import Iterator

from imgutils.detect import detect_heads, detect_faces
from imgutils.operate import censor_areas
from imgutils.pose import dwpose_estimate

from .base import ProcessAction, BaseAction
from ..model import ImageItem


class HeadCutOutAction(BaseAction):
    def __init__(self, kp_threshold: float = 0.3, level: str = 's', version: str = 'v1.4', max_infer_size=640,
                 conf_threshold: float = 0.25, iou_threshold: float = 0.7):
        self.kp_threshold = kp_threshold
        self.level = level
        self.version = version
        self.max_infer_size = max_infer_size
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold

    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        poses = dwpose_estimate(item.image)
        if len(poses) > 0:
            pose = poses[0]
            points = pose.body

            faces = detect_faces(item.image, self.level, self.version, self.max_infer_size,
                                 self.conf_threshold, self.iou_threshold)
            if not faces:
                return
            (x0, y0, x1, y1), _, _ = faces[0]
            crop_areas = [
                (0, 0, x0, item.image.height),
                (0, 0, item.image.width, y0),
                (x1, 0, item.image.width, item.image.height),
                (0, y1, item.image.width, item.image.height),
            ]

            maxi, maxcnt = None, None
            for i in range(len(crop_areas)):
                cx0, cy0, cx1, cy1 = crop_areas[i]
                cnt = sum([
                    1 for x, y, score in points
                    if score >= self.kp_threshold and cx0 <= x <= cx1 and cy0 <= y <= cy1
                ])
                if maxcnt is None or cnt > maxcnt:
                    maxi, maxcnt = i, cnt

            if maxcnt > 0:
                yield ImageItem(item.image.crop(crop_areas[maxi]), item.meta)

    def reset(self):
        pass


class HeadCoverAction(ProcessAction):
    def __init__(self, color: str = 'black', scale: float = 1.2, level: str = 's', max_infer_size=640,
                 conf_threshold: float = 0.3, iou_threshold: float = 0.7):
        self.color = color
        self.scale = scale
        self.level = level
        self.max_infer_size = max_infer_size
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold

    def process(self, item: ImageItem) -> ImageItem:
        head_areas = []
        for (x0, y0, x1, y1), _, _ in \
                detect_heads(item.image, self.level, self.max_infer_size, self.conf_threshold, self.iou_threshold):
            width, height = x1 - x0, y1 - y0
            xc, yc = (x0 + x1) / 2, (y0 + y1) / 2
            width, height = width * self.scale, height * self.scale
            x0, x1 = xc - width / 2, xc + width / 2
            y0, y1 = yc - height / 2, yc + height / 2
            head_areas.append((x0, y0, x1, y1))

        image = censor_areas(item.image, 'color', head_areas, color=self.color)
        return ImageItem(image, item.meta)
