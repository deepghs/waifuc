import pytest

from waifuc.source import WebDataSource

pytest_plugins = [
    'test.c_responses',
    'test.c_datasources',
]


@pytest.fixture(scope='session', autouse=True)
def no_websource_cd():
    origin_value = WebDataSource.__download_rate_interval__
    try:
        WebDataSource.__download_rate_interval__ = 0.01
        yield
    finally:
        WebDataSource.__download_rate_interval__ = origin_value
