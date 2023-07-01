import os.path
from typing import List, Optional

from .rule34 import Rule34LikeSource


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
