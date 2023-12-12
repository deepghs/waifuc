import json
import logging
import os.path
import pickle
from dataclasses import dataclass
from typing import Optional, Mapping, Any

from PIL import Image
from hbutils.encoding import base64_decode, base64_encode
from hbutils.reflection import quick_import_object

NoneType = type(None)

_TYPE_META = '__type'
_BASE64_META = 'base64'


def load_meta(data, path=()):
    if isinstance(data, (int, float, str, NoneType)):
        return data
    elif isinstance(data, list):
        return [load_meta(item, (*path, i)) for i, item in enumerate(data)]
    elif isinstance(data, dict):
        if _TYPE_META not in data:
            return {key: load_meta(value, (*path, key)) for key, value in data.items()}
        else:
            cls, _, _ = quick_import_object(data[_TYPE_META])
            binary = base64_decode(data[_BASE64_META])
            obj = pickle.loads(binary)
            if isinstance(obj, cls):
                return obj
            else:
                raise TypeError(f'{cls!r} expected but {obj!r} found at {path!r}.')
    else:
        raise TypeError(f'Unknown type {data!r} at {path!r}.')


def dump_meta(data, path=()):
    if isinstance(data, (int, float, str, NoneType)):
        return data
    elif isinstance(data, list):
        return [dump_meta(item, (*path, i)) for i, item in enumerate(data)]
    elif isinstance(data, dict):
        return {key: dump_meta(value, (*path, key)) for key, value in data.items()}
    else:
        cls = type(data)
        type_str = f'{cls.__module__}.{cls.__name__}' if hasattr(cls, '__module__') else cls.__name__
        base64_str = base64_encode(pickle.dumps(data))
        return {
            _TYPE_META: type_str,
            _BASE64_META: base64_str
        }


@dataclass
class ImageItem:
    image: Image.Image
    meta: dict

    def __init__(self, image: Image.Image, meta: Optional[dict] = None):
        self.image = image
        self.meta = meta or {}

    @classmethod
    def _image_file_to_meta_file(cls, image_file):
        directory, filename = os.path.split(image_file)
        filebody, _ = os.path.splitext(filename)
        meta_file = os.path.join(directory, f'.{filebody}_meta.json')
        return meta_file

    @classmethod
    def load_from_image(cls, image_file):
        image = Image.open(image_file)
        meta_file = cls._image_file_to_meta_file(image_file)

        if os.path.exists(meta_file):
            with open(meta_file, 'r', encoding='utf-8') as f:
                meta = load_meta(json.load(f))
        else:
            meta = {}

        return cls(image, meta)

    def save(self, image_file, no_meta: bool = False, skip_when_image_exist: bool = False,
             save_params: Optional[Mapping[str, Any]] = None):
        if not skip_when_image_exist or not os.path.exists(image_file):
            logging.debug(f'Saving image to {image_file!r}, params: {save_params or {}!r} ...')
            self.image.save(image_file, **(save_params or {}))
        if not no_meta and self.meta:
            meta_file = self._image_file_to_meta_file(image_file)
            logging.debug(f'Saving metadata file for image {image_file!r} to {meta_file!r} ...')
            with open(meta_file, 'w', encoding='utf-8') as f:
                json.dump(dump_meta(self.meta), f)

    def __repr__(self):
        values = {'size': self.image.size}
        for key, value in self.meta.items():
            if isinstance(value, (int, float, str)):
                values[key] = value

        content = ', '.join(f'{key}: {values[key]!r}' for key in sorted(values.keys()))
        return f'<{self.__class__.__name__} {content}>'
