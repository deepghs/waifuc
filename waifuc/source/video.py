import glob
import logging
import os
from typing import Iterator, Optional
from urllib.error import HTTPError

from hbutils.scale import time_to_delta_str
from tqdm.auto import tqdm

from .base import EmptySource, NamedDataSource, BaseDataSource
from ..model import ImageItem
from ..utils import get_file_type

try:
    import av
    import av.datasets
    from av.error import InvalidDataError

    _VIDEO_EXTRACT_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    av = None
    _VIDEO_EXTRACT_AVAILABLE = False

_DEFAULT_MIN_FRAME_INTERVAL: float = 0.5


class VideoSource(NamedDataSource):
    def __init__(self, video_file, min_frame_interval: Optional[float] = _DEFAULT_MIN_FRAME_INTERVAL,
                 key_frames_only: bool = False):
        if not _VIDEO_EXTRACT_AVAILABLE:
            raise ImportError(f'pyav not installed, {self.__class__.__name__} is unavailable. '
                              f'Please install this with `pip install git+https://github.com/deepghs/waifuc.git@main#egg=waifuc[video]` to solve this problem.')
        self.video_file = os.path.abspath(video_file)
        self.min_frame_interval = min_frame_interval
        self.key_frames_only = key_frames_only

    def _args(self):
        return [self.video_file]

    def _iter(self) -> Iterator[ImageItem]:
        try:
            content = av.datasets.curated(self.video_file)
        except HTTPError as err:
            logging.error(f'Video {self.video_file!r} is invalid, skipped - {err!r}')
            return

        try:
            _last_frame_time = None
            with av.open(content) as container:
                stream = container.streams.video[0]
                if stream.time_base and stream.duration:
                    total_time = float(stream.time_base * stream.duration)
                else:
                    total_time = None
                stream.codec_context.skip_frame = "NONKEY" if self.key_frames_only else "DEFAULT"

                pg = tqdm(
                    total=int(total_time) if total_time is not None else None,
                    desc=f'Video Extracting - {os.path.basename(self.video_file)}'
                )
                for i, frame in enumerate(container.decode(stream), ):
                    if self.min_frame_interval is None or \
                            _last_frame_time is None or frame.time - _last_frame_time >= self.min_frame_interval:
                        filebody, _ = os.path.splitext(os.path.basename(self.video_file))
                        meta = {
                            'video_file': self.video_file,
                            'time': frame.time,
                            'index': i,
                            'filename': f'{filebody}_time_{frame.time:.3f}s.png',
                        }
                        yield ImageItem(frame.to_image(), meta)
                        pg.update(int(frame.time) - int(_last_frame_time or 0.0))
                        _last_frame_time = frame.time
                        if total_time is not None:
                            pg.set_description(f'Video Extracting - {os.path.basename(self.video_file)} - '
                                               f'{time_to_delta_str(int(frame.time))} / '
                                               f'{time_to_delta_str(int(total_time))}')
                        else:
                            pg.set_description(f'Video Extracting - {os.path.basename(self.video_file)} - '
                                               f'{time_to_delta_str(int(frame.time))}')
        except (InvalidDataError, av.error.ValueError, IndexError, UnicodeError) as err:
            logging.warning(f'Video extraction skipped due to error - {err!r}')

    @classmethod
    def from_directory(cls, directory: str, recursive: bool = True,
                       min_frame_interval: float = _DEFAULT_MIN_FRAME_INTERVAL,
                       key_frames_only: bool = False) -> BaseDataSource:
        if recursive:
            files = glob.glob(os.path.join(glob.escape(directory), '**', '*'), recursive=True)
        else:
            files = glob.glob(os.path.join(glob.escape(directory), '*'))

        source = EmptySource()
        for file in files:
            if os.path.isfile(file) and os.access(file, os.R_OK):
                file_type_ = get_file_type(file)
                if file_type_ and 'video' in file_type_:
                    source = source + cls(file, min_frame_interval=min_frame_interval, key_frames_only=key_frames_only)
        return source
