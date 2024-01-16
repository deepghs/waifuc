import logging
import os
import warnings
import zipfile
from typing import Iterator, Optional, Union, Tuple, Literal

import httpx
from PIL import Image, UnidentifiedImageError
from PIL.Image import DecompressionBombError
from hbutils.system import urlsplit, TemporaryDirectory
from pixivpy3 import AppPixivAPI
from pixivpy3.utils import JsonDict

from .web import WebDataSource
from ..utils import get_requests_session, download_file

_FilterTyping = Literal["for_ios", ""]
_TypeTyping = Literal["illust", "manga", ""]
_RestrictTyping = Literal["public", "private", ""]
_ContentTypeTyping = Literal["illust", "manga", ""]
_ModeTyping = Literal[
    "day",
    "week",
    "month",
    "day_male",
    "day_female",
    "week_original",
    "week_rookie",
    "day_manga",
    "day_r18",
    "day_male_r18",
    "day_female_r18",
    "week_r18",
    "week_r18g",
    "",
]
_SearchTargetTyping = Literal[
    "partial_match_for_tags", "exact_match_for_tags", "title_and_caption", "keyword", ""
]
_SortTyping = Literal["date_desc", "date_asc", "popular_desc", ""]
_DurationTyping = Literal[
    "within_last_day", "within_last_week", "within_last_month", "", None
]
_BoolTyping = Literal["true", "false"]
_SelectTyping = Literal['square_medium', 'medium', 'large', 'original']


class _UgoiraSkip(Exception):
    pass


def _remove_pixiv_json(obj):
    if isinstance(obj, (list, tuple)):
        return type(obj)([_remove_pixiv_json(item) for item in obj])
    elif isinstance(obj, (dict, JsonDict)):
        return {key: _remove_pixiv_json(value) for key, value in obj.items()}
    else:
        return obj


class BasePixivSource(WebDataSource):
    def __init__(self, group_name: str = 'pixiv', select: _SelectTyping = 'large',
                 no_ai: bool = False, refresh_token: Optional[str] = None, download_silent: bool = True):
        self.select = select
        self.no_ai = no_ai
        self.refresh_token = refresh_token
        self.client = AppPixivAPI()
        self.client.requests = get_requests_session(session=self.client.requests)
        self.client.requests.headers.update({"Referer": "https://app-api.pixiv.net/"})
        WebDataSource.__init__(self, group_name, self.client.requests, download_silent)

    def _iter_illustration(self) -> Iterator[dict]:
        raise NotImplementedError  # pragma: no cover

    def _make_gif_for_ugoira(self, frames_info: list, zip_url: str):
        with TemporaryDirectory() as td:
            filename = urlsplit(zip_url).filename
            frame_zip = os.path.join(td, filename)
            try:
                self._rate_limiter().try_acquire(filename)
                download_file(
                    zip_url, frame_zip, desc=filename,
                    session=self.session, silent=self.download_silent
                )
            except httpx.HTTPError as err:
                warnings.warn(f'Skipped due to download error: {err!r}')
                raise _UgoiraSkip

            with zipfile.ZipFile(frame_zip, 'r') as zf:
                zf.extractall(td)
                all_frames, all_durations = [], []
                for frame in frames_info:
                    dst_file = os.path.join(td, frame['file'])

                    try:
                        frame_img = Image.open(dst_file)
                        frame_img.load()
                    except UnidentifiedImageError:
                        warnings.warn(f'Image {dst_file!r} in package {filename!r} unidentified as image, skipped.')
                        raise _UgoiraSkip
                    except (IOError, DecompressionBombError) as err:
                        warnings.warn(f'Skipped due to IO error in {filename!r}: {err!r}')
                        raise _UgoiraSkip

                    all_frames.append(frame_img)
                    all_durations.append(frame['delay'])

            gif_file = os.path.join(td, os.path.splitext(filename)[0] + '.gif')
            all_frames[0].save(
                gif_file,
                save_all=True,
                append_images=all_frames[1:],
                duration=all_durations,
                loop=0,
            )

            gif_img = Image.open(gif_file)
            return gif_img

    def _iter_data(self) -> Iterator[Tuple[Union[str, int], str, dict]]:
        if self.refresh_token:
            self.client.auth(refresh_token=self.refresh_token)

        for illust in self._iter_illustration():
            illust = _remove_pixiv_json(illust)

            if self.no_ai and illust['illust_ai_type'] == 2:
                logging.info(f'Work {illust["id"]} skipped due to AI-filtering policy.')
                continue

            if illust['type'] in {'illust', 'manga'}:
                if illust['page_count'] == 1:
                    if self.select != 'original':
                        urls = [illust['image_urls'][self.select]]
                    else:
                        urls = [illust['meta_single_page']['original_image_url']]

                else:
                    urls = [page['image_urls'][self.select] for page in illust['meta_pages']]

                for i, url in enumerate(urls):
                    _, ext_name = os.path.splitext(urlsplit(url).filename)
                    filename = f'{self.group_name}_{illust["id"]}_{i}{ext_name}'
                    meta = {
                        'pixiv': illust,
                        'group_id': f'{self.group_name}_{illust["id"]}',
                        'instance_id': f'{self.group_name}_{illust["id"]}_{i}',
                        'filename': filename,
                    }
                    yield f'{illust["id"]}_{i}', url, meta

            elif illust['type'] == 'ugoira':
                metadata = _remove_pixiv_json(self.client.ugoira_metadata(illust_id=illust['id'])['ugoira_metadata'])
                frame_infos = metadata['frames']
                zip_urls = metadata['zip_urls']
                for scale in [self.select, 'original', 'large', 'medium']:
                    if scale in zip_urls:
                        zip_url = zip_urls[scale]
                        break
                else:
                    logging.info(f'No selectable url found in work {illust["id"]} '
                                 f'in urls {zip_urls!r}, skipped.')
                    continue

                try:
                    gif_image = self._make_gif_for_ugoira(frame_infos, zip_url)
                    gif_image.load()
                except _UgoiraSkip:
                    continue
                filename = f'{self.group_name}_{illust["id"]}.gif'
                meta = {
                    'pixiv': illust,
                    'ugoira': metadata,
                    'group_id': f'{self.group_name}_{illust["id"]}',
                    'instance_id': f'{self.group_name}_{illust["id"]}',
                    'filename': filename,
                    'url': zip_url,
                }
                yield f'{illust["id"]}', gif_image, meta

            else:
                logging.info(f'Work {illust["id"]} skipped due to it is a {illust["type"]}.')
                continue


class PixivSearchSource(BasePixivSource):
    def __init__(self, word: str, search_target: _SearchTargetTyping = "partial_match_for_tags",
                 sort: _SortTyping = "date_desc", duration: _DurationTyping = None, start_date: Optional[str] = None,
                 end_date: Optional[str] = None, filter: _FilterTyping = "for_ios", req_auth: bool = True,
                 group_name: str = 'pixiv', select: _SelectTyping = 'large',
                 no_ai: bool = False, refresh_token: Optional[str] = None, download_silent: bool = True):
        BasePixivSource.__init__(self, group_name, select, no_ai, refresh_token, download_silent)
        self.word = word
        self.search_target = search_target
        self.sort = sort
        self.duration = duration
        self.start_date = start_date
        self.end_date = end_date
        self.filter = filter
        self.req_auth = req_auth

    def _args(self):
        return [self.word]

    def _iter_illustration(self) -> Iterator[dict]:
        offset = 0
        while True:
            data = self.client.search_illust(self.word, self.search_target, self.sort, self.duration,
                                             self.start_date, self.end_date, self.filter, offset, self.req_auth)
            if 'illusts' not in data:
                logging.warning(f'Illusts not found in page (offset: {offset!r}), skipped: {data!r}.')
                break
            illustrations = data['illusts']
            yield from illustrations

            offset += len(illustrations)
            if not illustrations:
                break


class PixivUserSource(BasePixivSource):
    def __init__(self, user_id: Union[int, str], type: _TypeTyping = "illust",
                 filter: _FilterTyping = "for_ios", req_auth: bool = True,
                 group_name: str = 'pixiv', select: _SelectTyping = 'large',
                 no_ai: bool = False, refresh_token: Optional[str] = None, download_silent: bool = True):
        BasePixivSource.__init__(self, group_name, select, no_ai, refresh_token, download_silent)
        self.user_id = user_id
        self.type = type
        self.filter = filter
        self.req_auth = req_auth

    def _args(self):
        return [self.user_id]

    def _iter_illustration(self) -> Iterator[dict]:
        offset = 0
        while True:
            data = self.client.user_illusts(self.user_id, self.type, self.filter, offset, self.req_auth)
            if 'illusts' not in data:
                logging.warning(f'Illusts not found in page (offset: {offset!r}), skipped: {data!r}.')
                break
            illustrations = data['illusts']
            yield from illustrations

            offset += len(illustrations)
            if not illustrations:
                break


class PixivRankingSource(BasePixivSource):
    def __init__(self, mode: _ModeTyping = "day", filter: _FilterTyping = "for_ios",
                 date: Optional[str] = None, req_auth: bool = True,
                 group_name: str = 'pixiv', select: _SelectTyping = 'large',
                 no_ai: bool = False, refresh_token: Optional[str] = None, download_silent: bool = True):
        BasePixivSource.__init__(self, group_name, select, no_ai, refresh_token, download_silent)
        self.mode = mode
        self.filter = filter
        self.date = date
        self.req_auth = req_auth

    def _args(self):
        return [self.mode]

    def _iter_illustration(self) -> Iterator[dict]:
        offset = 0
        while True:
            data = self.client.illust_ranking(self.mode, self.filter, self.date, offset, self.req_auth)
            if 'illusts' not in data:
                logging.warning(f'Illusts not found in page (offset: {offset!r}), skipped: {data!r}.')
                break
            illustrations = data['illusts']
            yield from illustrations

            offset += len(illustrations)
            if not illustrations:
                break
