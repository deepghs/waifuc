from dataclasses import dataclass

from PIL import Image


@dataclass
class ImageItem:
    image: Image.Image
    meta: dict
