import os.path
import re
from typing import Optional, Iterator, List, Tuple, Union, Literal

from hbutils.system import urlsplit
from requests.auth import HTTPBasicAuth

from .web import NoURL, WebDataSource
from ..config.meta import __TITLE__, __VERSION__
from ..utils import get_requests_session, srequest

_DanbooruSiteTyping = Literal['konachan', 'yandere', 'danbooru', 'safebooru', 'lolibooru']


class DanbooruLikeSource(WebDataSource):
    def __init__(self, tags: List[str], min_size: Optional[int] = 800, download_silent: bool = True,
                 username: Optional[str] = None, api_key: Optional[str] = None,
                 site_name: Optional[str] = 'danbooru', site_url: Optional[str] = 'https://danbooru.donmai.us/',
                 group_name: Optional[str] = None):
        WebDataSource.__init__(self, group_name or site_name, None, download_silent)
        self.session = get_requests_session(headers={
            "User-Agent": f"{__TITLE__}/{__VERSION__}",
            'Content-Type': 'application/json; charset=utf-8',
        })
        self.auth = HTTPBasicAuth(username, api_key) if username and api_key else None
        self.site_name, self.site_url = site_name, site_url
        self.tags = tags
        self.min_size = min_size

    def _args(self):
        return [self.tags]

    def _get_data_from_raw(self, raw):
        return raw

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

    def _get_tags(self, data):
        return re.split(r'\s+', data["tag_string"])

    def _iter_data(self) -> Iterator[Tuple[Union[str, int], str, dict]]:
        page = 1
        while True:
            resp = srequest(self.session, 'GET', f'{self.site_url}/posts.json', params={
                "format": "json",
                "limit": "100",
                "page": str(page),
                "tags": ' '.join(self.tags),
            }, auth=self.auth)
            resp.raise_for_status()
            page_items = self._get_data_from_raw(resp.json())
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
                    self.site_name: data,
                    'group_id': f'{self.group_name}_{data["id"]}',
                    'filename': filename,
                    'tags': {key: 1.0 for key in self._get_tags(data)}
                }
                yield data['id'], url, meta

            page += 1


class DanbooruSource(DanbooruLikeSource):
    def __init__(self, tags: List[str],
                 min_size: Optional[int] = 800, download_silent: bool = True,
                 username: Optional[str] = None, api_key: Optional[str] = None,
                 group_name: Optional[str] = None):
        DanbooruLikeSource.__init__(self, tags, min_size, download_silent, username, api_key,
                                    'danbooru', 'https://danbooru.donmai.us/', group_name)


class SafebooruSource(DanbooruLikeSource):
    def __init__(self, tags: List[str],
                 min_size: Optional[int] = 800, download_silent: bool = True,
                 username: Optional[str] = None, api_key: Optional[str] = None,
                 group_name: Optional[str] = None):
        DanbooruLikeSource.__init__(self, tags, min_size, download_silent, username, api_key,
                                    'safebooru', 'https://safebooru.donmai.us', group_name)


class ATFBooruSource(DanbooruLikeSource):
    def __init__(self, tags: List[str],
                 min_size: Optional[int] = 800, download_silent: bool = True,
                 username: Optional[str] = None, api_key: Optional[str] = None,
                 group_name: Optional[str] = None):
        DanbooruLikeSource.__init__(self, tags, min_size, download_silent, username, api_key,
                                    'danbooru', 'https://booru.allthefallen.moe', group_name)


class E621LikeSource(DanbooruLikeSource):
    def __init__(self, tags: List[str],
                 min_size: Optional[int] = 800, download_silent: bool = True,
                 username: Optional[str] = None, api_key: Optional[str] = None,
                 site_name: Optional[str] = 'e621', site_url: Optional[str] = 'https://e621.net/',
                 group_name: Optional[str] = None):
        DanbooruLikeSource.__init__(self, tags, min_size, download_silent, username, api_key,
                                    site_name, site_url, group_name or site_name)

    def _get_data_from_raw(self, raw):
        return raw['posts']

    def _select_url(self, data):
        urls = []
        urls.append((data['file']['url'], data['file']['width'], data['file']['height']))
        urls.append((data['preview']['url'], data['preview']['width'], data['preview']['height']))
        if 'sample' in data and data['sample']['has']:
            urls.append((data['sample']['url'], data['sample']['width'], data['sample']['height']))

        if self.min_size is not None:
            f_url, f_width, f_height = None, None, None
            for url, width, height in urls:
                if width >= self.min_size and height >= self.min_size:
                    if f_url is None or width < f_width:
                        f_url, f_width, f_height = url, width, height

            if f_url is not None:
                return f_url

        return urls[0][0]

    def _get_tags(self, data):
        tags = []
        for value in data['tags'].values():
            tags.extend(value)
        return tags


class E621Source(E621LikeSource):
    def __init__(self, tags: List[str],
                 min_size: Optional[int] = 800, download_silent: bool = True,
                 username: Optional[str] = None, api_key: Optional[str] = None,
                 group_name: Optional[str] = 'e621'):
        E621LikeSource.__init__(self, tags, min_size, download_silent, username, api_key,
                                'e621', 'https://e621.net/', group_name)


class E926Source(E621LikeSource):
    def __init__(self, tags: List[str],
                 min_size: Optional[int] = 800, download_silent: bool = True,
                 username: Optional[str] = None, api_key: Optional[str] = None,
                 group_name: Optional[str] = 'e926'):
        E621LikeSource.__init__(self, tags, min_size, download_silent, username, api_key,
                                'e926', 'https://e926.net/', group_name)
