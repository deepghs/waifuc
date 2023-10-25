import glob
import os.path
import zipfile
from contextlib import contextmanager

import responses
from hbutils.system import TemporaryDirectory
from huggingface_hub import hf_hub_download

from .base import _REMOTE_REPOSITORY


@contextmanager
def mock_responses_from_hf(name):
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
