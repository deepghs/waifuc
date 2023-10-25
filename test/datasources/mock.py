import zipfile
from contextlib import contextmanager

import responses
from hbutils.system import TemporaryDirectory
from huggingface_hub import hf_hub_download

from .base import _REMOTE_REPOSITORY


@contextmanager
def mock_datasource_dir_from_hf(name):
    with TemporaryDirectory() as td:
        zip_file = hf_hub_download(_REMOTE_REPOSITORY, filename=f'datasources/{name}.zip', repo_type='dataset')
        with zipfile.ZipFile(zip_file, 'r') as zf:
            zf.extractall(td)

        try:
            yield td
        finally:
            responses.reset()
