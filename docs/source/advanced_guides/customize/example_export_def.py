import csv
import os.path

from imgutils.tagging import tags_to_text

from waifuc.export import BaseExporter
from waifuc.model import ImageItem


class CsvExporter(BaseExporter):
    def __init__(self, dst_dir: str):
        BaseExporter.__init__(self, ignore_error_when_export=False)
        self.dst_dir = dst_dir
        self._tag_file = None
        self._tag_writer = None

    def pre_export(self):
        self._tag_file = open(os.path.join(self.dst_dir, 'tags.csv'), 'w')
        self._tag_writer = csv.writer(self._tag_file)
        self._tag_writer.writerow(['filename', 'tags'])

    def export_item(self, item: ImageItem):
        item.save(os.path.join(self.dst_dir, item.meta['filename']))
        self._tag_writer.writerow([item.meta['filename'], tags_to_text(item.meta['tags'])])

    def post_export(self):
        if self._tag_file is not None:
            self._tag_file.close()
            self.reset()

    def reset(self):
        self._tag_file = None
        self._tag_writer = None
