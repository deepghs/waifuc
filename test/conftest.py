from contextlib import contextmanager

import pytest
import responses
from huggingface_hub import hf_hub_download

from .responses.base import _REMOTE_REPOSITORY


@contextmanager
def _mock_with_hf_func(name):
    yaml_file = hf_hub_download(_REMOTE_REPOSITORY, filename=f'{name}.yaml', repo_type='dataset')
    responses._add_from_file(yaml_file)
    try:
        yield
    finally:
        responses.reset()


@pytest.fixture(scope='session')
def danbooru():
    with _mock_with_hf_func('danbooru'):
        yield


@pytest.fixture(scope='session')
def safebooru():
    with _mock_with_hf_func('safebooru'):
        yield
