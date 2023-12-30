import os
import warnings
from typing import Iterator, Tuple, Union

from PIL import UnidentifiedImageError, Image
from PIL.Image import DecompressionBombError
from hbutils.system import urlsplit, TemporaryDirectory

from .base import RootDataSource
from ..model import ImageItem
from ..utils import get_requests_session, download_file, USE_REQUESTS

if USE_REQUESTS:
    import requests
else:
    from curl_cffi import requests


class NoURL(Exception):
    pass


class WebDataSource(RootDataSource):
    def __init__(self, group_name: str, session: requests.Session = None, download_silent: bool = True):
        self.download_silent = download_silent
        self.session = session or get_requests_session()
        self.group_name = group_name

    def _iter_data(self) -> Iterator[Tuple[Union[str, int], str, dict]]:
        raise NotImplementedError  # pragma: no cover

    def _iter(self) -> Iterator[ImageItem]:
        for id_, url, meta in self._iter_data():
            with TemporaryDirectory(ignore_cleanup_errors=True) as td:
                _, ext_name = os.path.splitext(urlsplit(url).filename)
                filename = f'{self.group_name}_{id_}{ext_name}'
                td_file = os.path.join(td, filename)
                try:
                    download_file(
                        url, td_file, desc=filename,
                        session=self.session, silent=self.download_silent
                    )
                    image = Image.open(td_file)
                    image.load()
                except UnidentifiedImageError:
                    warnings.warn(f'{self.group_name.capitalize()} resource {id_} unidentified as image, skipped.')
                    continue
                except (IOError, DecompressionBombError) as err:
                    warnings.warn(f'Skipped due to error: {err!r}')
                    continue

                meta = {**meta, 'url': url}
                yield ImageItem(image, meta)
