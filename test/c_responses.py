import pytest

from .responses import mock_responses_from_hf


@pytest.fixture(scope='session')
def anime_pictures_2girls():
    with mock_responses_from_hf('anime_pictures_2girls'):
        yield


@pytest.fixture(scope='session')
def anime_pictures_surtr():
    with mock_responses_from_hf('anime_pictures_surtr'):
        yield


@pytest.fixture(scope='session')
def atfbooru():
    with mock_responses_from_hf('atfbooru'):
        yield


@pytest.fixture(scope='session')
def danbooru():
    with mock_responses_from_hf('danbooru'):
        yield


@pytest.fixture(scope='session')
def duitang_nian():
    with mock_responses_from_hf('duitang_nian'):
        yield


@pytest.fixture(scope='session')
def duitang_nian_non_strict():
    with mock_responses_from_hf('duitang_nian_non_strict'):
        yield


@pytest.fixture(scope='session')
def e621_amiya():
    with mock_responses_from_hf('e621_amiya'):
        yield


@pytest.fixture(scope='session')
def e621_surtr():
    with mock_responses_from_hf('e621_surtr'):
        yield


@pytest.fixture(scope='session')
def e926_amiya():
    with mock_responses_from_hf('e926_amiya'):
        yield


@pytest.fixture(scope='session')
def e926_surtr():
    with mock_responses_from_hf('e926_surtr'):
        yield


@pytest.fixture(scope='session')
def huashi6_nian():
    with mock_responses_from_hf('huashi6_nian'):
        yield


@pytest.fixture(scope='session')
def konachan_2dogs():
    with mock_responses_from_hf('konachan_2dogs'):
        yield


@pytest.fixture(scope='session')
def konachan_net_2dogs():
    with mock_responses_from_hf('konachan_net_2dogs'):
        yield


@pytest.fixture(scope='session')
def konachan_net_surtr():
    with mock_responses_from_hf('konachan_net_surtr'):
        yield


@pytest.fixture(scope='session')
def konachan_surtr():
    with mock_responses_from_hf('konachan_surtr'):
        yield


@pytest.fixture(scope='session')
def pixiv_search_surtr():
    with mock_responses_from_hf('pixiv_search_surtr'):
        yield


@pytest.fixture(scope='session')
def safebooru():
    with mock_responses_from_hf('safebooru'):
        yield


@pytest.fixture(scope='session')
def yande_2dogs():
    with mock_responses_from_hf('yande_2dogs'):
        yield


@pytest.fixture(scope='session')
def yande_surtr():
    with mock_responses_from_hf('yande_surtr'):
        yield


@pytest.fixture(scope='session')
def zerochan_surtr():
    with mock_responses_from_hf('zerochan_surtr'):
        yield


@pytest.fixture(scope='session')
def zerochan_surtr_full():
    with mock_responses_from_hf('zerochan_surtr_full'):
        yield


@pytest.fixture(scope='session')
def zerochan_surtr_strict():
    with mock_responses_from_hf('zerochan_surtr_strict'):
        yield
