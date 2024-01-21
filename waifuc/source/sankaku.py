import datetime
import os
from enum import Enum
from typing import Optional, Iterator, List, Tuple, Union

from hbutils.system import urlsplit

from .web import NoURL, WebDataSource
from ..utils import get_requests_session, srequest


class Rating(str, Enum):
    SAFE = "s"
    QUESTIONABLE = "q"
    EXPLICIT = "e"


class PostOrder(Enum):
    POPULARITY = "popularity"
    DATE = "date"
    QUALITY = "quality"
    RANDOM = "random"
    RECENTLY_FAVORITED = "recently_favorited"
    RECENTLY_VOTED = "recently_voted"


class FileType(Enum):
    IMAGE = "image"  # jpeg, png, webp formats
    GIF = "animated_gif"  # gif format
    VIDEO = "video"  # mp4, webm formats


def _tags_by_kwargs(**kwargs):
    tags = []
    for k, v in kwargs.items():
        if v is None:
            pass
        elif k in {"order", "rating", "file_type"} and v is not FileType.IMAGE:  # noqa
            tags.append(f"{k}:{v.value}")
        elif k in {"threshold", "recommended_for", "voted"}:
            tags.append(f"{k}:{v}")
        elif k == "date":
            date = "..".join(d.strftime("%Y-%m-%dT%H:%M") for d in self.date)  # type: ignore[union-attr]
            tags.append(f"date:{date}")
        elif k == "added_by":
            for user in self.added_by:  # type: ignore[union-attr]
                tags.append(f"user:{user}")

    return tags


class SankakuSource(WebDataSource):
    def __init__(self, tags: List[str], order: Optional[PostOrder] = None,
                 rating: Optional[Rating] = None, file_type: Optional[FileType] = None,
                 date: Optional[Tuple[datetime.datetime, datetime.datetime]] = None,
                 username: Optional[str] = None, password: Optional[str] = None, access_token: Optional[str] = None,
                 min_size: Optional[int] = 800, download_silent: bool = True, group_name: str = 'sankaku', **kwargs):
        WebDataSource.__init__(self, group_name, get_requests_session(), download_silent)
        self.tags = tags + _tags_by_kwargs(order=order, rating=rating, file_type=file_type, date=date, **kwargs)
        self.username, self.password = username, password
        self.access_token = access_token

        self.min_size = min_size
        self.auth_session = get_requests_session(headers={
            'Content-Type': 'application/json; charset=utf-8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Host': 'capi-v2.sankakucomplex.com',
            'X-Requested-With': 'com.android.browser',
        })

    def _args(self):
        return [self.tags]

    _FILE_URLS = [
        ('sample_url', 'sample_width', 'sample_height'),
        ('preview_url', 'preview_width', 'preview_height'),
        ('file_url', 'width', 'height'),
    ]

    def _select_url(self, data):
        if self.min_size is not None:
            f_url, f_width, f_height = None, None, None
            for url_name, width_name, height_name in self._FILE_URLS:
                if url_name in data and width_name in data and height_name in data:
                    url, width, height = data[url_name], data[width_name], data[height_name]
                    if width and height and width >= self.min_size and height >= self.min_size:
                        if f_url is None or width < f_width:
                            f_url, f_width, f_height = url, width, height

            if f_url is not None:
                return f_url

        if 'file_url' in data and data['file_url']:
            return data['file_url']
        else:
            raise NoURL

    def _login(self):
        if self.access_token:
            self.auth_session.headers.update({
                "Authorization": f"Bearer {self.access_token}",
            })
        elif self.username and self.password:
            resp = srequest(self.auth_session, 'POST', 'https://login.sankakucomplex.com/auth/token',
                            json={"login": self.username, "password": self.password})
            resp.raise_for_status()
            login_data = resp.json()
            self.auth_session.headers.update({
                "Authorization": f"{login_data['token_type']} {login_data['access_token']}",
            })

    def _iter_data(self) -> Iterator[Tuple[Union[str, int], str, dict]]:
        self._login()

        page = 1
        while True:
            resp = srequest(self.auth_session, 'GET', 'https://capi-v2.sankakucomplex.com/posts', params={
                'lang': 'en',
                'page': str(page),
                'limit': '100',
                'tags': ' '.join(self.tags),
            })
            resp.raise_for_status()
            if not resp.json():
                break

            for data in resp.json():
                try:
                    url = self._select_url(data)
                except NoURL:
                    continue

                _, ext_name = os.path.splitext(urlsplit(url).filename)
                filename = f'{self.group_name}_{data["id"]}{ext_name}'
                meta = {
                    'sankaku': data,
                    'group_id': f'{self.group_name}_{data["id"]}',
                    'filename': filename,
                    'tags': {key: 1.0 for key in [t_item['name'] for t_item in data['tags']]}
                }
                yield data["id"], url, meta

            page += 1
