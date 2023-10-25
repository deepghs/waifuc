import os.path
from typing import Iterator

from hbutils.system import remove
from tqdm.auto import tqdm

from ..model import ImageItem
from ..utils import get_task_names


class BaseExporter:
    def pre_export(self):
        raise NotImplementedError  # pragma: no cover

    def export_item(self, item: ImageItem):
        raise NotImplementedError  # pragma: no cover

    def post_export(self):
        raise NotImplementedError  # pragma: no cover

    def export_from(self, items: Iterator[ImageItem]):
        self.pre_export()
        names = get_task_names()
        if names:
            desc = f'{self.__class__.__name__} - {".".join(names)}'
        else:
            desc = f'{self.__class__.__name__}'
        for item in tqdm(items, desc=desc):
            self.export_item(item)
        self.post_export()

    def reset(self):
        raise NotImplementedError  # pragma: no cover


class LocalDirectoryExporter(BaseExporter):
    def __init__(self, output_dir, clear: bool = False):
        self.output_dir = output_dir
        self.clear = clear

    def pre_export(self):
        if self.clear and os.path.exists(self.output_dir):
            remove(self.output_dir)

        os.makedirs(self.output_dir, exist_ok=True)

    def export_item(self, item: ImageItem):
        raise NotImplementedError  # pragma: no cover

    def post_export(self):
        pass

    def reset(self):
        raise NotImplementedError  # pragma: no cover


class SaveExporter(LocalDirectoryExporter):
    def __init__(self, output_dir, clear: bool = False, no_meta: bool = False,
                 skip_when_image_exist: bool = False):
        LocalDirectoryExporter.__init__(self, output_dir, clear)
        self.no_meta = no_meta
        self.untitles = 0
        self.skip_when_image_exist = skip_when_image_exist

    def export_item(self, item: ImageItem):
        if 'filename' in item.meta:
            filename = item.meta['filename']
        else:
            self.untitles += 1
            filename = f'untited_{self.untitles}.png'

        full_filename = os.path.join(self.output_dir, filename)
        full_directory = os.path.dirname(full_filename)
        if full_directory:
            os.makedirs(full_directory, exist_ok=True)
        item.save(full_filename, no_meta=self.no_meta, skip_when_image_exist=self.skip_when_image_exist)

    def reset(self):
        self.untitles = 0
