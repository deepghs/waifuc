from functools import reduce
from operator import __or__
from typing import Iterator, Tuple, Optional, List, Mapping

from ditk import logging
from gchar.games.base import Character
from hbutils.string import plural_word

from .anime_pictures import AnimePicturesSource
from .base import BaseDataSource
from .danbooru import ATFBooruSource, DanbooruSource
from .konachan import KonachanSource, KonachanNetSource, HypnoHubSource, LolibooruSource, XbooruSource, YandeSource, \
    Rule34Source, KonachanLikeSource
from .pixiv import PixivSearchSource
from .sankaku import SankakuSource
from .wallhaven import WallHavenSource
from .zerochan import ZerochanSource
from ..model import ImageItem

_PRESET_SITES = ('zerochan', 'anime_pictures')
_REGISTERED_SITE_SOURCES = {
    'anime_pictures': AnimePicturesSource,
    'atfbooru': ATFBooruSource,
    # 'sankaku': SankakuSource,  # still something wrong with sankaku source
    'danbooru': DanbooruSource,
    'hypnohub': HypnoHubSource,
    'konachan': KonachanSource,
    'konachan_net': KonachanNetSource,
    'lolibooru': LolibooruSource,
    'rule34': Rule34Source,
    # 'safebooru': SafebooruSource,
    'xbooru': XbooruSource,
    'yande': YandeSource,
    'zerochan': ZerochanSource,
    'wallhaven': WallHavenSource,
    'pixiv': PixivSearchSource,
}


class GcharAutoSource(BaseDataSource):
    def __init__(self, ch, allow_fuzzy: bool = False, fuzzy_threshold: int = 80, contains_extra: bool = True,
                 sure_only: bool = True, preset_sites: Tuple[str, ...] = _PRESET_SITES,
                 max_preset_limit: Optional[int] = None, main_sources_count: int = 3,
                 blacklist_sites: Tuple[str, ...] = (), pixiv_refresh_token: Optional[str] = None,
                 extra_cfg: Optional[Mapping[str, dict]] = None):
        from gchar.games import get_character

        if isinstance(ch, Character):
            self.ch = ch
        else:
            self.ch = get_character(ch, allow_fuzzy, fuzzy_threshold, contains_extra)
        if not self.ch:
            raise ValueError(f'Character {ch!r} not found.')
        logging.info(f'Character {self.ch!r} found in gchar.')

        self.sure_only = sure_only
        self.pixiv_refresh_token = pixiv_refresh_token
        self.extra_cfg = dict(extra_cfg or {})

        for site in preset_sites:
            assert site in _REGISTERED_SITE_SOURCES, f'Preset site {site!r} not available.'
        self.preset_sites = sorted(preset_sites)
        self.max_preset_limit = max_preset_limit
        if 'pixiv' in self.preset_sites and not self.pixiv_refresh_token:
            raise ValueError('Pixiv refresh token not given for presetting pixiv source!')
        self.main_sources_count = main_sources_count

        self.blacklist_sites = blacklist_sites

    def _select_keyword_for_site(self, site) -> Tuple[Optional[str], Optional[int]]:
        from gchar.resources.sites import list_site_tags
        from gchar.resources.pixiv import get_pixiv_keywords, get_pixiv_posts

        if site == 'pixiv':
            keyword = get_pixiv_keywords(self.ch)
            cnt = get_pixiv_posts(self.ch)
            count = 0 if cnt is None else cnt[0]
            return keyword, count

        else:
            tags: List[Tuple[str, int]] = list_site_tags(self.ch, site, sure_only=self.sure_only, with_posts=True)
            tags = sorted(tags, key=lambda x: (-x[1], x[0]))
            if tags:
                return tags[0]
            else:
                return None, None

    def _build_source_on_site(self, site) -> Optional[BaseDataSource]:
        site_class = _REGISTERED_SITE_SOURCES[site]
        keyword, count = self._select_keyword_for_site(site)
        if keyword is not None:
            extra_cfg = dict(self.extra_cfg.get(site, None) or {})
            logging.info(f'Recommended keyword for site {site!r} is {keyword!r}, '
                         f'with {plural_word(count, "known post")}.')
            if issubclass(site_class, (DanbooruSource, AnimePicturesSource)):
                return site_class([keyword, 'solo'], **extra_cfg)
            elif issubclass(site_class, (KonachanLikeSource, SankakuSource)):
                return site_class([keyword], **extra_cfg)
            elif issubclass(site_class, ZerochanSource):
                return ZerochanSource(keyword, strict=True, **extra_cfg)
            elif issubclass(site_class, WallHavenSource):
                return site_class(keyword, **extra_cfg)
            elif issubclass(site_class, (PixivSearchSource,)):
                return site_class(keyword, refresh_token=self.pixiv_refresh_token, **extra_cfg)
            else:
                raise TypeError(f'Unknown class {site_class!r} for keyword {keyword!r}.')  # pragma: no cover
        else:
            logging.info(f'No keyword recommendation for site {site!r}.')
            return None

    def _build_preset_source(self) -> Optional[BaseDataSource]:
        logging.info('Building preset sites sources ...')
        sources = [
            self._build_source_on_site(site)
            for site in self.preset_sites
        ]
        sources = [source for source in sources if source is not None]
        if sources:
            retval = reduce(__or__, sources)
            if self.max_preset_limit is not None:
                retval = retval[:self.max_preset_limit]
            return retval
        else:
            return None

    def _build_main_source(self) -> Optional[BaseDataSource]:
        _all_sites = set(_REGISTERED_SITE_SOURCES.keys())
        if not self.pixiv_refresh_token:
            _all_sites.remove('pixiv')
        _all_sites = sorted(_all_sites - set(self.preset_sites) - set(self.blacklist_sites))
        logging.info(f'Available sites for main sources: {_all_sites!r}.')

        site_pairs = []
        for site in _all_sites:
            keyword, count = self._select_keyword_for_site(site)
            if keyword is not None:
                site_pairs.append((site, keyword, count))
        site_pairs = sorted(site_pairs, key=lambda x: -x[2])[:self.main_sources_count]
        logging.info(f'Selected main sites: {site_pairs!r}')

        sources = [
            self._build_source_on_site(site)
            for site, _, _ in site_pairs
        ]
        sources = [source for source in sources if source is not None]
        if sources:
            return reduce(__or__, sources)
        else:
            return None

    def _build_source(self) -> Optional[BaseDataSource]:
        preset_source = self._build_preset_source()
        main_source = self._build_main_source()
        if preset_source and main_source:
            return preset_source + main_source
        elif preset_source:
            return preset_source
        elif main_source:
            return main_source
        else:
            return None

    def _iter(self) -> Iterator[ImageItem]:
        source = self._build_source()
        if source is not None:
            yield from source._iter()
