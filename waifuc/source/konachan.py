import os
import re
from typing import Iterator, Tuple, Union, List, Optional

from hbutils.system import urlsplit

from .web import WebDataSource, NoURL
from ..utils import get_requests_session, srequest


class KonachanLikeSource(WebDataSource):
    def __init__(self, site_name: str, site_url: str,
                 tags: List[str], start_page: int = 1, min_size: Optional[int] = 800,
                 group_name: Optional[str] = None, download_silent: bool = True):
        WebDataSource.__init__(self, group_name or site_name, get_requests_session(), download_silent)
        self.site_name = site_name
        self.site_url = site_url
        self.start_page = start_page
        self.min_size = min_size
        self.tags: List[str] = tags

    def _select_url(self, data):
        if self.min_size is not None:
            url_names = [key for key in data.keys() if key.endswith('_url')]
            name_pairs = [
                *(
                    (name, f'{name[:-4]}_width', f'{name[:-4]}_height')
                    for name in url_names
                ),
                ('file_url', 'width', 'height'),
            ]

            f_url, f_width, f_height = None, None, None
            for url_name, width_name, height_name in name_pairs:
                if url_name in data and width_name in data and height_name in data:
                    url, width, height = data[url_name], data[width_name], data[height_name]
                    if width >= self.min_size and height >= self.min_size:
                        if f_url is None or width < f_width:
                            f_url, f_width, f_height = url, width, height

            if f_url is not None:
                return f_url

        if 'file_url' in data:
            return data['file_url']
        else:
            raise NoURL

    def _request(self, page):
        return srequest(self.session, 'GET', f'{self.site_url}/post.json', params={
            'tags': ' '.join(self.tags),
            'limit': '100',
            'page': str(page),
        })

    def _get_data_from_raw(self, raw):
        return raw

    def _iter_data(self) -> Iterator[Tuple[Union[str, int], str, dict]]:
        page = self.start_page
        while True:
            resp = self._request(page)
            resp.raise_for_status()

            if not resp.text.strip():
                break
            page_list = self._get_data_from_raw(resp.json())
            if not page_list:
                break

            for data in page_list:
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
                    'tags': {key: 1.0 for key in re.split(r'\s+', data['tags'])}
                }
                yield data["id"], url, meta

            page += 1


class YandeSource(KonachanLikeSource):
    def __init__(self, tags: List[str], min_size: Optional[int] = 800,
                 group_name: str = 'yande', download_silent: bool = True):
        KonachanLikeSource.__init__(self, 'yande', 'https://yande.re',
                                    tags, 1, min_size, group_name, download_silent)


class KonachanSource(KonachanLikeSource):
    def __init__(self, tags: List[str], min_size: Optional[int] = 800,
                 group_name: str = 'konachan', download_silent: bool = True):
        KonachanLikeSource.__init__(self, 'konachan', 'https://konachan.com',
                                    tags, 1, min_size, group_name, download_silent)


class KonachanNetSource(KonachanLikeSource):
    def __init__(self, tags: List[str], min_size: Optional[int] = 800,
                 group_name: str = 'konachan_net', download_silent: bool = True):
        KonachanLikeSource.__init__(self, 'konachan_net', 'https://konachan.net',
                                    tags, 1, min_size, group_name, download_silent)


class LolibooruSource(KonachanLikeSource):
    def __init__(self, tags: List[str], min_size: Optional[int] = 800,
                 group_name: str = 'lolibooru', download_silent: bool = True):
        KonachanLikeSource.__init__(self, 'lolibooru', 'https://lolibooru.moe',
                                    tags, 1, min_size, group_name, download_silent)

    def _request(self, page):
        return srequest(self.session, 'GET', f'{self.site_url}/post/index.json', params={
            'tags': ' '.join(self.tags),
            'limit': '100',
            'page': str(page),
        })


class Rule34LikeSource(KonachanLikeSource):
    def __init__(self, site_name: str, site_url: str,
                 tags: List[str], min_size: Optional[int] = 800,
                 group_name: Optional[str] = None, download_silent: bool = True):
        KonachanLikeSource.__init__(self, site_name, site_url, tags, 0, min_size, group_name, download_silent)

    def _request(self, page):
        return srequest(self.session, 'GET', f'{self.site_url}/index.php', params={
            'page': 'dapi',
            's': 'post',
            'q': 'index',
            'tags': ' '.join(self.tags),
            'json': '1',
            'limit': '100',
            'pid': str(page),
        })


class Rule34Source(Rule34LikeSource):
    def __init__(self, tags: List[str], min_size: Optional[int] = 800,
                 group_name: str = 'rule34', download_silent: bool = True):
        Rule34LikeSource.__init__(self, 'rule34', 'https://rule34.xxx',
                                  tags, min_size, group_name, download_silent)


class HypnoHubSource(Rule34LikeSource):
    def __init__(self, tags: List[str], min_size: Optional[int] = 800,
                 group_name: str = 'hypnohub', download_silent: bool = True):
        Rule34LikeSource.__init__(self, 'hypnohub', 'https://hypnohub.net',
                                  tags, min_size, group_name, download_silent)


class GelbooruSource(Rule34LikeSource):
    def __init__(self, tags: List[str], min_size: Optional[int] = 800,
                 group_name: str = 'gelbooru', download_silent: bool = True):
        Rule34LikeSource.__init__(self, 'gelbooru', 'https://gelbooru.com',
                                  tags, min_size, group_name, download_silent)

    def _get_data_from_raw(self, raw):
        return raw['post']


class XbooruLikeSource(Rule34LikeSource):
    def __init__(self, site_name: str, site_url: str, img_site_url: str,
                 tags: List[str], min_size: Optional[int] = 800,
                 group_name: Optional[str] = None, download_silent: bool = True):
        Rule34LikeSource.__init__(self, site_name, site_url, tags, min_size, group_name, download_silent)
        self.img_site_url = img_site_url

    def _select_url(self, data):
        name, _ = os.path.splitext(data['image'])
        urls = [(f'{self.img_site_url}/images/{data["directory"]}/{data["image"]}', data['width'], data['height'])]
        if data['sample']:
            urls.append((
                f'{self.img_site_url}/samples/{data["directory"]}/sample_{name}.jpg?{data["id"]}',
                data['sample_width'], data['sample_height'],
            ))

        if self.min_size is not None:
            f_url, f_width, f_height = None, None, None
            for url, width, height in urls:
                if width >= self.min_size and height >= self.min_size:
                    if f_url is None or width < f_width:
                        f_url, f_width, f_height = url, width, height

            if f_url is not None:
                return f_url

        return urls[0][0]


class XbooruSource(XbooruLikeSource):
    def __init__(self, tags: List[str], min_size: Optional[int] = 800,
                 group_name: str = 'xbooru', download_silent: bool = True):
        XbooruLikeSource.__init__(
            self, 'xbooru', 'https://xbooru.com', 'https://img.xbooru.com',
            tags, min_size, group_name, download_silent,
        )


class SafebooruOrgSource(XbooruLikeSource):
    def __init__(self, tags: List[str], min_size: Optional[int] = 800,
                 group_name: str = 'safebooru_org', download_silent: bool = True):
        XbooruLikeSource.__init__(
            self, 'safebooru_org', 'https://safebooru.org', 'https://safebooru.org',
            tags, min_size, group_name, download_silent,
        )


class TBIBSource(XbooruLikeSource):
    def __init__(self, tags: List[str], min_size: Optional[int] = 800,
                 group_name: str = 'tbib', download_silent: bool = True):
        XbooruLikeSource.__init__(
            self, 'tbib', 'https://tbib.org', 'https://tbib.org',
            tags, min_size, group_name, download_silent,
        )
