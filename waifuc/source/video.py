import glob
import logging
import os
from typing import Iterator
from urllib.error import HTTPError

from tqdm.auto import tqdm

from .base import BaseDataSource, EmptySource
from ..model import ImageItem

try:
    import av
    import av.datasets
    from av.error import InvalidDataError
except (ImportError, ModuleNotFoundError):
    av = None


class VideoSource(BaseDataSource):
    def __init__(self, video_file):
        if av is None:
            raise ImportError(f'pyav not installed, {self.__class__.__name__} is unavailable. '
                              f'Please install this with `pip install waifuc[video]` to solve this problem.')
        self.video_file = video_file

    def _iter(self) -> Iterator[ImageItem]:
        try:
            content = av.datasets.curated(self.video_file)
        except HTTPError:
            logging.error(f'Video {self.video_file!r} is invalid, skipped')
            return

        try:
            with av.open(content) as container:
                stream = container.streams.video[0]
                stream.codec_context.skip_frame = "NONKEY"

                for i, frame in enumerate(tqdm(
                        container.decode(stream),
                        desc=f'Video Extracting - {os.path.basename(self.video_file)}')):
                    meta = {
                        'video_file': self.video_file,
                        'time': frame.time,
                        'index': i,
                    }
                    yield ImageItem(frame.to_image(), meta)
        except (InvalidDataError, av.error.ValueError) as err:
            logging.warning(f'Video extraction skipped due to error - {err!r}')

    @classmethod
    def from_directory(cls, directory: str, recursive: bool = True) -> BaseDataSource:
        if recursive:
            files = glob.glob(os.path.join(glob.escape(directory), '**', '*'), recursive=True)
        else:
            files = glob.glob(os.path.join(glob.escape(directory), '*'))

        source = EmptySource()
        for file in files:
            if os.path.isfile(file) and os.access(file, os.R_OK):
                source = source + cls(file)
        return source
