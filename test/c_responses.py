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
def safebooru():
    with mock_responses_from_hf('safebooru'):
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
