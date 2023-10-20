import pytest
import responses

from test.testings import get_testfile


@pytest.fixture(scope='session')
def danbooru():
    responses._add_from_file(get_testfile('danbooru.yaml'))
    try:
        yield
    finally:
        responses.reset()


@pytest.fixture(scope='session')
def safebooru():
    responses._add_from_file(get_testfile('safebooru.yaml'))
    try:
        yield
    finally:
        responses.reset()
