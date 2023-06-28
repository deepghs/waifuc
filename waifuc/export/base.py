import os.path
from typing import Iterator

from hbutils.system import remove
from tqdm.auto import tqdm

from ..model import ImageItem


class BaseExporter:
    def init(self):
        raise NotImplementedError

    def export(self, item: ImageItem):
        raise NotImplementedError

    def export_from(self, items: Iterator[ImageItem]):
        self.init()
        for item in tqdm(items):
            self.export(item)

    def reset(self):
        raise NotImplementedError


class SaveExporter(BaseExporter):
    def __init__(self, output_dir, clear: bool = False, no_meta: bool = False):
        self.output_dir = output_dir
        self.clear = clear
        self.no_meta = no_meta
        self.untitles = 0

    def init(self):
        if self.clear and os.path.exists(self.output_dir):
            remove(self.output_dir)

        os.makedirs(self.output_dir, exist_ok=True)

    def export(self, item: ImageItem):
        if 'filename' in item.meta:
            filename = item.meta['filename']
        else:
            self.untitles += 1
            filename = f'untited_{self.untitles}.png'

        full_filename = os.path.join(self.output_dir, filename)
        full_directory = os.path.dirname(full_filename)
        if full_directory:
            os.makedirs(full_directory, exist_ok=True)
        item.save(full_filename, no_meta=self.no_meta)

    def reset(self):
        self.untitles = 0
