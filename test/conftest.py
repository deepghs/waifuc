import glob
import os.path
import zipfile
from contextlib import contextmanager

import pytest
import responses
from hbutils.system import TemporaryDirectory
from huggingface_hub import hf_hub_download

from .responses.base import _REMOTE_REPOSITORY


@contextmanager
def _mock_with_hf_func(name):
    with TemporaryDirectory() as td:
        zip_file = hf_hub_download(_REMOTE_REPOSITORY, filename=f'responses/{name}.zip', repo_type='dataset')
        with zipfile.ZipFile(zip_file, 'r') as zf:
            zf.extractall(td)

        yaml_files = glob.glob(os.path.join(td, '*.yaml'))
        assert len(yaml_files) == 1
        responses._add_from_file(yaml_files[0])
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
