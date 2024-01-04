from contextlib import contextmanager

from hbutils.system import TemporaryDirectory
from hfutils.archive import archive_unpack
from huggingface_hub import hf_hub_download
from pytest_httpx_recorder.recorder import ResSet

from .base import _REMOTE_REPOSITORY


@contextmanager
def mock_responses_from_hf(name, httpx_mock):
    with TemporaryDirectory() as td:
        archive_unpack(hf_hub_download(
            repo_id=_REMOTE_REPOSITORY,
            repo_type='dataset',
            filename=f'responses_httpx/{name}.zip'
        ), td, silent=True)

        resset = ResSet.load(td)
        with resset.mock_context(httpx_mock):
            yield
