import os
import os
import warnings
from threading import Thread
from typing import Iterator, Tuple, Union, Optional

import requests
from PIL import UnidentifiedImageError, Image
from PIL.Image import DecompressionBombError
from hbutils.system import urlsplit, TemporaryDirectory

from .base import RootDataSource
from ..model import ImageItem
from ..utils import get_requests_session, download_file, SerializableParallelModule, NonSerializableParallelModule, \
    Stopped


class NoURL(Exception):
    pass


class BaseWebDataSource(RootDataSource):
    def __init__(self, group_name: str, session: requests.Session = None, download_silent: bool = True):
        self.download_silent = download_silent
        self.session = session or get_requests_session()
        self.group_name = group_name

    def _iter_data(self) -> Iterator[Tuple[Union[str, int], str, dict]]:
        raise NotImplementedError  # pragma: no cover

    def _get_item(self, id_, url, meta) -> Optional[ImageItem]:
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
                return None
            except (IOError, DecompressionBombError) as err:
                warnings.warn(f'Skipped due to error: {err!r}')
                return None

            meta = {**meta, 'url': url}
            return ImageItem(image, meta)

    def _iter(self) -> Iterator[ImageItem]:
        raise NotImplementedError  # pragma: no cover


class WebDataSource(BaseWebDataSource):
    def _iter_data(self) -> Iterator[Tuple[Union[str, int], str, dict]]:
        raise NotImplementedError  # pragma: no cover

    def _iter(self) -> Iterator[ImageItem]:
        for id_, url, meta in self._iter_data():
            item = self._get_item(id_, url, meta)
            if item is not None:
                yield item


class ParallelWebDataSource(BaseWebDataSource):
    def __init__(self, group_name: str, session: requests.Session = None, download_silent: bool = True,
                 max_workers: Optional[int] = None, serializable: bool = True):
        BaseWebDataSource.__init__(self, group_name, session, download_silent)
        if serializable:
            self._parallel = SerializableParallelModule(max_workers=max_workers)
        else:
            self._parallel = NonSerializableParallelModule(max_workers=max_workers)
        self._thread = Thread(target=self._fn_item_load)

    def _fn_item_load(self):
        for id_, url, meta in self._iter_data():
            try:
                self._parallel.submit_task(self._get_item, id_, url, meta)
            except Stopped:
                break

        self._parallel.shutdown()

    def cleanup(self):
        self._parallel.shutdown()
        self._parallel.join()
        self._thread.join()

    def _iter_data(self) -> Iterator[Tuple[Union[str, int], str, dict]]:
        raise NotImplementedError  # pragma: no cover

    def _iter(self) -> Iterator[ImageItem]:
        self._thread.start()
        while True:
            try:
                item = self._parallel.next_value()
            except Stopped:
                break
            else:
                if item is not None:
                    yield item
