import os.path
import re
from typing import Optional, Iterator, List, Tuple, Union, Literal

from hbutils.system import urlsplit

from .web import NoURL, WebDataSource, DynamicUAWebDataSource
from ..utils import srequest

_DanbooruSiteTyping = Literal['konachan', 'yandere', 'danbooru', 'safebooru', 'lolibooru']
_DanbooruTagDomainTyping = Literal['general', 'character', 'copyright', 'artist', 'meta']
_E621DomainTyping = Literal['artist', 'character', 'copyright', 'general', 'invalid', 'lore', 'meta', 'species']


class DanbooruLikeSource(DynamicUAWebDataSource):
    def __init__(self, tags: List[str], min_size: Optional[int] = 800, download_silent: bool = True,
                 username: Optional[str] = None, api_key: Optional[str] = None,
                 site_name: Optional[str] = 'danbooru', site_url: Optional[str] = 'https://danbooru.donmai.us/',
                 group_name: Optional[str] = None, tag_domains: Optional[List[str]] = None):
        WebDataSource.__init__(self, group_name or site_name, None, download_silent)
        self.session.headers.update({
            'Content-Type': 'application/json; charset=utf-8',
        })
        if username and api_key:
            self.auth = (username, api_key)
        else:
            self.auth = None
        self.site_name, self.site_url = site_name, site_url
        self.tags = tags
        self.min_size = min_size
        self.tag_domains = tag_domains

    def _check_session(self) -> bool:
        resp = srequest(self.session, 'GET', f'{self.site_url}/posts.json', params={
            "format": "json",
            "tags": '1girl',
        }, auth=self.auth, raise_for_status=False)
        return resp.status_code // 100 == 2

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
        if self.tag_domains is None:
            return re.split(r'\s+', data["tag_string"])
        else:
            tags = []
            for tag_domain in self.tag_domains:
                tags.extend(re.split(r'\s+', data[f'tag_string_{tag_domain}']))
            return tags

    def _iter_data(self) -> Iterator[Tuple[Union[str, int], str, dict]]:
        page = 1
        while True:
            resp = srequest(self.session, 'GET', f'{self.site_url}/posts.json', params={
                "format": "json",
                "limit": "200",
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
                 group_name: Optional[str] = None, tag_domains: Optional[List[_DanbooruTagDomainTyping]] = None):
        DanbooruLikeSource.__init__(self, tags, min_size, download_silent, username, api_key,
                                    'danbooru', 'https://danbooru.donmai.us/', group_name, tag_domains)


class SafebooruSource(DanbooruLikeSource):
    def __init__(self, tags: List[str],
                 min_size: Optional[int] = 800, download_silent: bool = True,
                 username: Optional[str] = None, api_key: Optional[str] = None,
                 group_name: Optional[str] = None, tag_domains: Optional[List[_DanbooruTagDomainTyping]] = None):
        DanbooruLikeSource.__init__(self, tags, min_size, download_silent, username, api_key,
                                    'safebooru', 'https://safebooru.donmai.us', group_name, tag_domains)


class ATFBooruSource(DanbooruLikeSource):
    def __init__(self, tags: List[str],
                 min_size: Optional[int] = 800, download_silent: bool = True,
                 username: Optional[str] = None, api_key: Optional[str] = None,
                 group_name: Optional[str] = None, tag_domains: Optional[List[_DanbooruTagDomainTyping]] = None):
        DanbooruLikeSource.__init__(self, tags, min_size, download_silent, username, api_key,
                                    'danbooru', 'https://booru.allthefallen.moe', group_name, tag_domains)


class E621LikeSource(DanbooruLikeSource):
    def __init__(self, tags: List[str],
                 min_size: Optional[int] = 800, download_silent: bool = True,
                 username: Optional[str] = None, api_key: Optional[str] = None,
                 site_name: Optional[str] = 'e621', site_url: Optional[str] = 'https://e621.net/',
                 group_name: Optional[str] = None, tag_domains: Optional[List[_E621DomainTyping]] = None):
        DanbooruLikeSource.__init__(self, tags, min_size, download_silent, username, api_key,
                                    site_name, site_url, group_name or site_name, tag_domains)

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
        if self.tag_domains is None:
            for value in data['tags'].values():
                tags.extend(value)
        else:
            for key, value in data['tags'].items():
                if key in self.tag_domains:
                    tags.extend(value)
        return tags


class E621Source(E621LikeSource):
    def __init__(self, tags: List[str],
                 min_size: Optional[int] = 800, download_silent: bool = True,
                 username: Optional[str] = None, api_key: Optional[str] = None,
                 group_name: Optional[str] = 'e621', tag_domains: Optional[List[_E621DomainTyping]] = None):
        E621LikeSource.__init__(self, tags, min_size, download_silent, username, api_key,
                                'e621', 'https://e621.net/', group_name, tag_domains)


class E926Source(E621LikeSource):
    def __init__(self, tags: List[str],
                 min_size: Optional[int] = 800, download_silent: bool = True,
                 username: Optional[str] = None, api_key: Optional[str] = None,
                 group_name: Optional[str] = 'e926', tag_domains: Optional[List[_E621DomainTyping]] = None):
        E621LikeSource.__init__(self, tags, min_size, download_silent, username, api_key,
                                'e926', 'https://e926.net/', group_name, tag_domains)
