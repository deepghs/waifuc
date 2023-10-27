import pytest

from .datasources import mock_datasource_dir_from_hf


@pytest.fixture(scope='session')
def ccip_mudrock():
    with mock_datasource_dir_from_hf('ccip_mudrock') as dir_:
        yield dir_


@pytest.fixture(scope='session')
def ccip_simple():
    with mock_datasource_dir_from_hf('ccip_simple') as dir_:
        yield dir_


@pytest.fixture(scope='session')
def danbooru_20():
    with mock_datasource_dir_from_hf('danbooru_20') as dir_:
        yield dir_


@pytest.fixture(scope='session')
def danbooru_5():
    with mock_datasource_dir_from_hf('danbooru_5') as dir_:
        yield dir_


@pytest.fixture(scope='session')
def zerochan_20():
    with mock_datasource_dir_from_hf('zerochan_20') as dir_:
        yield dir_


@pytest.fixture(scope='session')
def zerochan_5():
    with mock_datasource_dir_from_hf('zerochan_5') as dir_:
        yield dir_
