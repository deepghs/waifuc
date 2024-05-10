import os.path
import random
from typing import Iterator, Optional, Tuple, List

from PIL import ImageOps, Image
from hbutils.random import random_sha1
from imgutils.data import load_image
from imgutils.detect import detect_heads, detect_person, detect_halfbody
from imgutils.operate import squeeze_with_transparency
from imgutils.resource import BackgroundImageSet

from .base import BaseAction
from ..model import ImageItem


class BaseRandomAction(BaseAction):
    def __init__(self, seed=None):
        self.seed = seed
        self.random = random.Random(self.seed)

    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        raise NotImplementedError  # pragma: no cover

    def reset(self):
        self.random = random.Random(self.seed)


class RandomChoiceAction(BaseRandomAction):
    def __init__(self, p=0.5, seed=None):
        BaseRandomAction.__init__(self, seed)
        self.p = p

    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        if self.random.random() <= self.p:
            yield item


class RandomFilenameAction(BaseRandomAction):
    def __init__(self, ext: Optional[str] = '.png', seed=None):
        BaseRandomAction.__init__(self, seed)
        self.ext = ext

    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        if 'filename' in item.meta:
            ext = self.ext or os.path.splitext(os.path.basename(item.meta['filename']))[0]
        else:
            if self.ext:
                ext = self.ext
            else:
                raise NameError(f'Extension (ext) must be specified '
                                f'when filename not in metadata of image item - {item!r}.')

        filename = random_sha1(rnd=self.random) + ext
        yield ImageItem(item.image, {**item.meta, 'filename': filename})


class MirrorAction(BaseAction):
    def __init__(self, names: Tuple[str, str] = ('origin', 'mirror')):
        self.origin_name, self.mirror_name = names

    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        if 'filename' in item.meta:
            filebody, ext = os.path.splitext(item.meta['filename'])
            yield ImageItem(item.image, {**item.meta, 'filename': f'{filebody}_{self.origin_name}{ext}'})
            yield ImageItem(ImageOps.mirror(item.image),
                            {**item.meta, 'filename': f'{filebody}_{self.mirror_name}{ext}'})
        else:
            yield ImageItem(item.image, item.meta)
            yield ImageItem(ImageOps.mirror(item.image), item.meta)

    def reset(self):
        pass


_ENHANCE_MODES = ['person', 'halfbody', 'head']
_DEFAULT_ENHANCE_MODES = ['halfbody', 'head']


class CharacterEnhanceAction(BaseAction):
    def __init__(self, repeats: int = 10, modes: Optional[List[str]] = None,
                 head_ratio: float = 1.2, body_ratio: float = 1.05, halfbody_ratio: float = 1.1,
                 degree_range: Tuple[float, float] = (-30, 30)):
        if modes is None:
            modes = _DEFAULT_ENHANCE_MODES
        self.repeats = repeats
        self.modes = list(modes)
        self.head_ratio = head_ratio
        self.body_ratio = body_ratio
        self.halfbody_ratio = halfbody_ratio
        self.degree_range = degree_range

    def _image_take(self, item: ImageItem):
        image = item.image
        if self.degree_range:
            min_degree, max_degree = self.degree_range
            degree = random.random() * (max_degree - min_degree) + min_degree
            image = squeeze_with_transparency(image.rotate(degree, expand=True, resample=Image.BILINEAR))
        else:
            degree = None

        origin_image = image.convert('RGBA')
        image = load_image(origin_image, mode='RGB', force_background='white')

        a_modes = list(self.modes).copy()
        random.shuffle(a_modes)
        detection: Optional[Tuple[int, int, int, int]] = None
        last_mode: Optional[str] = None
        for mode in a_modes:
            detection = self._auto_detect(image, mode)
            if detection is not None:
                x0, y0, x1, y1 = detection
                cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
                wx, wy = abs(x1 - x0), abs(y1 - y0)
                if mode == 'head':
                    r = self.head_ratio
                elif mode == 'body':
                    r = self.body_ratio
                elif mode == 'halfbody':
                    r = self.halfbody_ratio
                else:
                    r = 1.0
                r = r * (random.random() * 0.12 + 0.98)
                x0, y0 = int(cx - wx * r / 2), int(cy - wy * r / 2)
                x1, y1 = int(cx + wx * r / 2), int(cy + wy * r / 2)
                detection = (x0, y0, x1, y1)
                last_mode = mode
                break

        if detection is None:
            raise ValueError(f'No {self.modes!r} available.')

        dx0, dy0, dx1, dy1 = detection
        cropped = origin_image.crop(detection)
        image_set = BackgroundImageSet(min_resolution=min(1700, (cropped.width * cropped.height) ** 0.5))
        bg_image = image_set.random_image()
        if bg_image.width < cropped.width or bg_image.height < cropped.height:
            rx = max(cropped.width / bg_image.width, cropped.height / bg_image.height)
            bg_image = bg_image.resize((int(bg_image.width * rx), int(bg_image.height * rx)))

        max_width, max_height = cropped.width * 1.8, cropped.height * 1.8
        if bg_image.width >= max_width and bg_image.height >= max_height:
            rx = max(max_width / bg_image.width, max_height / bg_image.height)
            bg_image = bg_image.resize((int(bg_image.width * rx), int(bg_image.height * rx)))

        px0 = random.randint(0, max(bg_image.width - cropped.width, 1))
        py0 = random.randint(0, max(bg_image.height - cropped.height, 1))

        x0, y0 = px0 - dx0, py0 - dy0
        x1, y1 = x0 + origin_image.width, y0 + origin_image.height
        retval = bg_image.convert('RGBA')
        retval.paste(origin_image, (x0, y0, x1, y1), mask=origin_image)

        return ImageItem(
            image=retval,
            meta={
                **item.meta,
                'enhance': {
                    'degree': degree,
                    'position_x': px0,
                    'position_y': py0,
                    'mode': last_mode,
                }
            },
        )

    def iter(self, item: ImageItem) -> Iterator[ImageItem]:
        for i in range(self.repeats):
            new_item = self._image_take(item)
            if 'filename' in new_item.meta:
                body, ext = os.path.splitext(new_item.meta['filename'])
                new_item.meta['filename'] = f'{body}_e{i}{ext}'
            yield new_item

    @classmethod
    def _auto_detect(cls, image: Image.Image, mode: str = 'person'):
        if mode == 'head':
            detection = detect_heads(image)
        elif mode == 'person':
            detection = detect_person(image)
        elif mode == 'halfbody':
            detection = detect_halfbody(image)
        else:
            raise ValueError(f'Unknow mode - {mode!r}')

        if detection:
            return detection[0][0]
        else:
            return None

    def reset(self):
        pass
