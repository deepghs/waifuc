import os.path
import re
import warnings
from typing import Optional, Iterator, List

from PIL import UnidentifiedImageError, Image
from hbutils.system import TemporaryDirectory
from hbutils.system import urlsplit
from pybooru import Danbooru

from .base import BaseDataSource
from ..model import ImageItem
from ..utils import download_file, get_requests_session

try:
    from typing import Literal
except (ImportError, ModuleNotFoundError):
    from typing_extensions import Literal

_DanbooruSiteTyping = Literal['konachan', 'yandere', 'danbooru', 'safebooru', 'lolibooru']


class NoURL(Exception):
    pass


class DanbooruSource(BaseDataSource):
    def __init__(self, tags: List[str], random: bool = False,
                 min_size: Optional[int] = 800, download_silent: bool = True,
                 username: Optional[str] = None, api_key: Optional[str] = None,
                 site_name: _DanbooruSiteTyping = 'danbooru', site_url: Optional[str] = None,
                 group_name: Optional[str] = None):
        self.client = Danbooru(site_name, site_url or '', username or '', api_key or '')
        self.tags = tags
        self.random = random
        self.min_size = min_size
        self.download_silent = download_silent
        self.session = get_requests_session()
        self.group_name = group_name or site_name

    def _select_url(self, data):
        if self.min_size is not None and "media_asset" in data and "variants" in data["media_asset"]:
            variants = data["media_asset"]["variants"]
            width, height, url = None, None, None
            for item in variants:
                if 'width' in item and 'height' in item and \
                        item['width'] >= self.min_size and item['height'] >= self.min_size:
                    if url is None or item['width'] < width:
                        width, height, url = item['width'], item['height'], item['url']

            if url is not None:
                return url

        if 'file_url' not in data:
            raise NoURL

        return data['file_url']

    def _iter(self) -> Iterator[ImageItem]:
        page = 1
        while True:
            for data in self.client.post_list(tags=self.tags, random=self.random, page=page, limit=100):
                try:
                    url = self._select_url(data)
                except NoURL:
                    continue

                with TemporaryDirectory() as td:
                    _, ext_name = os.path.splitext(urlsplit(url).filename)
                    filename = f'{self.group_name}_{data["id"]}{ext_name}'
                    td_file = os.path.join(td, filename)
                    try:
                        download_file(
                            url, td_file, desc=filename,
                            session=self.session, silent=self.download_silent
                        )
                        image = Image.open(td_file)
                        image.load()
                    except UnidentifiedImageError:
                        warnings.warn(f'Resource {data["id"]} unidentified as image, skipped.')
                        continue

                    meta = {
                        'danbooru': data,
                        'group_id': f'{self.group_name}_{data["id"]}',
                        'filename': filename,
                        'tags': {key: 1.0 for key in re.split(r'\s+', data["tag_string"])}
                    }
                    yield ImageItem(image, meta)

            page += 1
