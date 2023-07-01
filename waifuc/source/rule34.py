from typing import List, Optional

from .yande import YandeLikeSource
from ..utils import srequest


class Rule34LikeSource(YandeLikeSource):
    def __init__(self, site_name: str, site_url: str,
                 tags: List[str], min_size: Optional[int] = 800,
                 group_name: Optional[str] = None, download_silent: bool = True):
        YandeLikeSource.__init__(self, site_name, site_url, tags, 0, min_size, group_name, download_silent)

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


class HypnoHubSource(Rule34Source):
    def __init__(self, tags: List[str], min_size: Optional[int] = 800,
                 group_name: str = 'hypnohub', download_silent: bool = True):
        Rule34LikeSource.__init__(self, 'hypnohub', 'https://hypnohub.net',
                                  tags, min_size, group_name, download_silent)


class GelbooruSource(Rule34Source):
    def __init__(self, tags: List[str], min_size: Optional[int] = 800,
                 group_name: str = 'gelbooru', download_silent: bool = True):
        Rule34LikeSource.__init__(self, 'gelbooru', 'https://gelbooru.com/',
                                  tags, min_size, group_name, download_silent)

    def _get_data_from_raw(self, raw):
        return raw['post']
