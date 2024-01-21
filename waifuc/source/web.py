import logging
import math
import os
import warnings
from typing import Iterator, Tuple, Union

import httpx
from PIL import UnidentifiedImageError, Image
from PIL.Image import DecompressionBombError
from hbutils.system import urlsplit, TemporaryDirectory
from pyrate_limiter import Rate, Duration, Limiter

from .base import NamedDataSource
from ..model import ImageItem
from ..utils import get_requests_session, download_file, get_random_ua, get_file_type


class NoURL(Exception):
    pass


class WebDataSource(NamedDataSource):
    __download_rate_limit__: int = 1
    __download_rate_interval__: float = 1

    def __init__(self, group_name: str, session: httpx.Client = None, download_silent: bool = True):
        self.download_silent = download_silent
        self.session = session or get_requests_session()
        self.group_name = group_name

    @classmethod
    def _rate_limiter(cls) -> Limiter:
        if not hasattr(cls, '_rate_limit'):
            if not os.environ.get('SHOW_RATE_LIMIT_LOG'):
                logger = logging.getLogger("pyrate_limiter")
                logger.disabled = True

            rate = Rate(cls.__download_rate_limit__, int(math.ceil(Duration.SECOND * cls.__download_rate_interval__)))
            limiter = Limiter(rate, max_delay=1 << 32)
            setattr(cls, '_rate_limit', limiter)

        return getattr(cls, '_rate_limit')

    def _iter_data(self) -> Iterator[Tuple[Union[str, int], Union[str, Image.Image], dict]]:
        raise NotImplementedError  # pragma: no cover

    def _iter(self) -> Iterator[ImageItem]:
        for id_, url, meta in self._iter_data():
            if isinstance(url, Image.Image):
                meta = dict(meta)
                if 'url' not in meta:
                    meta = {**meta, 'url': None}
                yield ImageItem(url, meta)

            else:
                with TemporaryDirectory(ignore_cleanup_errors=True) as td:
                    _, ext_name = os.path.splitext(urlsplit(url).filename)
                    filename = f'{self.group_name}_{id_}{ext_name}'
                    td_file = os.path.join(td, filename)

                    try:
                        self._rate_limiter().try_acquire(filename)
                        download_file(
                            url, td_file, desc=filename,
                            session=self.session, silent=self.download_silent
                        )
                    except httpx.HTTPError as err:
                        warnings.warn(f'Skipped due to download error: {err!r}')
                        continue

                    file_type = get_file_type(td_file)
                    if file_type == 'image':
                        try:
                            image = Image.open(td_file)
                            image.load()
                        except UnidentifiedImageError:
                            warnings.warn(
                                f'{self.group_name.capitalize()} resource {id_} unidentified as image, skipped.')
                            continue
                        except (IOError, DecompressionBombError) as err:
                            warnings.warn(f'Skipped due to IO error: {err!r}')
                            continue

                        meta = {**meta, 'url': url}
                        yield ImageItem(image, meta)

                    elif file_type == 'video':
                        from .video import _VIDEO_EXTRACT_AVAILABLE, VideoSource
                        if _VIDEO_EXTRACT_AVAILABLE:
                            logging.info(f'{self.group_name.capitalize()} resource {id_} '
                                         f'file {filename!r}\'s type is a {file_type} file, '
                                         f'extracting images from it.')
                            for item in VideoSource(td_file):
                                v_time = item.meta['time']
                                v_index = item.meta['index']
                                i_meta = {**meta, 'time': v_time, 'index': v_index, 'url': url}
                                if 'filename' in i_meta:
                                    fn, fext = os.path.splitext(i_meta['filename'])
                                    i_meta['filename'] = f'{fn}_keyframe_{v_index}.png'
                                yield ImageItem(item.image, i_meta)

                        else:
                            warnings.warn(f'{self.group_name.capitalize()} resource {id_} '
                                          f'file {filename!r}\'s type is a {file_type} file, '
                                          f'but video file is not supported for pyav library is not yet installed, '
                                          f'skipped.')

                    elif file_type:
                        warnings.warn(f'{self.group_name.capitalize()} resource {id_} '
                                      f'file {filename!r}\'s type is a {file_type} file, skipped.')

                    else:
                        warnings.warn(f'{self.group_name.capitalize()} resource {id_} '
                                      f'file {filename!r}\'s type is unknown, skipped.')


class WebPlusDataSource(WebDataSource):
    def _check_session(self) -> bool:
        raise NotImplementedError  # pragma: no cover

    def _refresh_session(self):
        raise NotImplementedError  # pragma: no cover

    def _prune_session(self):
        while True:
            self._rate_limiter().try_acquire('_prune_session_')
            self._refresh_session()
            if self._check_session():
                return

    def _iter_data(self) -> Iterator[Tuple[Union[str, int], str, dict]]:
        raise NotImplementedError  # pragma: no cover

    def _iter(self) -> Iterator[ImageItem]:
        self._prune_session()
        yield from WebDataSource._iter(self)


class DynamicUAWebDataSource(WebPlusDataSource):
    def _check_session(self) -> bool:
        raise NotImplementedError  # pragma: no cover

    def _refresh_session(self):
        user_agent = get_random_ua()
        self.session.headers.update({
            'User-Agent': user_agent,
        })
        logging.info(f'Trying use UA: {user_agent!r} ...')
