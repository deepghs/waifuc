import os

from imgutils.tagging import tags_to_text

from .base import LocalDirectoryExporter
from ..model import ImageItem


class TextualInversionExporter(LocalDirectoryExporter):
    def __init__(self, output_dir: str, clear: bool = False,
                 use_spaces: bool = False, use_escape: bool = True,
                 include_score: bool = False, score_descend: bool = True,
                 skip_when_image_exist: bool = False):
        LocalDirectoryExporter.__init__(self, output_dir, clear)
        self.use_spaces = use_spaces
        self.use_escape = use_escape
        self.include_score = include_score
        self.score_descend = score_descend
        self.untitles = 0
        self.skip_when_image_exist = skip_when_image_exist

    def export_item(self, item: ImageItem):
        if 'filename' in item.meta:
            filename = item.meta['filename']
        else:
            self.untitles += 1
            filename = f'untited_{self.untitles}.png'

        tags = item.meta.get('tags', None) or {}

        full_filename = os.path.join(self.output_dir, filename)
        full_tagname = os.path.join(self.output_dir, os.path.splitext(filename)[0] + '.txt')
        full_directory = os.path.dirname(full_filename)
        if full_directory:
            os.makedirs(full_directory, exist_ok=True)

        if not self.skip_when_image_exist or not os.path.exists(full_filename):
            item.image.save(full_filename)
        with open(full_tagname, 'w', encoding='utf-8') as f:
            f.write(tags_to_text(tags, self.use_spaces, self.use_escape, self.include_score, self.score_descend))

    def reset(self):
        self.untitles = 0
