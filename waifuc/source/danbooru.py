import os.path
import re
from typing import Optional, Iterator, List, Tuple, Union

from hbutils.system import urlsplit
from pybooru import Danbooru

from .web import NoURL, WebDataSource

try:
    from typing import Literal
except (ImportError, ModuleNotFoundError):
    from typing_extensions import Literal

_DanbooruSiteTyping = Literal['konachan', 'yandere', 'danbooru', 'safebooru', 'lolibooru']


class DanbooruSource(WebDataSource):
    def __init__(self, tags: List[str], random: bool = False,
                 min_size: Optional[int] = 800, download_silent: bool = True,
                 username: Optional[str] = None, api_key: Optional[str] = None,
                 site_name: _DanbooruSiteTyping = 'danbooru', site_url: Optional[str] = None,
                 group_name: Optional[str] = None):
        WebDataSource.__init__(self, group_name or site_name, None, download_silent)
        self.client = Danbooru(site_name, site_url or '', username or '', api_key or '')
        self.tags = tags
        self.random = random
        self.min_size = min_size

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

    def _iter_data(self) -> Iterator[Tuple[Union[str, int], str, dict]]:
        page = 1
        while True:
            page_items = self.client.post_list(tags=self.tags, random=self.random, page=page, limit=100)
            if not page_items:
                break

            for data in page_items:
                try:
                    url = self._select_url(data)
                except NoURL:
                    continue

                _, ext_name = os.path.splitext(urlsplit(url).filename)
                filename = f'{self.group_name}_{data["id"]}{ext_name}'
                meta = {
                    'danbooru': data,
                    'group_id': f'{self.group_name}_{data["id"]}',
                    'filename': filename,
                    'tags': {key: 1.0 for key in re.split(r'\s+', data["tag_string"])}
                }
                yield data['id'], url, meta

            page += 1


class SafebooruSource(DanbooruSource):
    def __init__(self, tags: List[str], random: bool = False,
                 min_size: Optional[int] = 800, download_silent: bool = True,
                 username: Optional[str] = None, api_key: Optional[str] = None,
                 group_name: Optional[str] = None):
        DanbooruSource.__init__(self, tags, random, min_size, download_silent, username, api_key,
                                'safebooru', 'https://safebooru.donmai.us', group_name)


class ATFBooruSource(DanbooruSource):
    def __init__(self, tags: List[str], random: bool = False,
                 min_size: Optional[int] = 800, download_silent: bool = True,
                 username: Optional[str] = None, api_key: Optional[str] = None,
                 group_name: Optional[str] = None):
        DanbooruSource.__init__(self, tags, random, min_size, download_silent, username, api_key,
                                'danbooru', 'https://booru.allthefallen.moe', group_name)
