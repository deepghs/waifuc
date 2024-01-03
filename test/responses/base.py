import os.path
from functools import wraps
from typing import Optional

from hbutils.system import TemporaryDirectory
from hfutils.operate import upload_directory_as_archive
from huggingface_hub import HfApi
from pytest_httpx_recorder.recorder import ResRecorder

_KNOWN_RECORDERS = {}
_REMOTE_REPOSITORY = 'deepghs/waifuc_unittest'
hf_client = HfApi(token=os.environ.get('HF_TOKEN'))


def resp_recorder(name: Optional[str] = None):
    def _decorator(func):
        _name = name or func.__name__

        @wraps(func)
        def _new_func(*args, **kwargs):
            with TemporaryDirectory() as td:
                recorder = ResRecorder()
                with recorder.record():
                    retval = func(*args, **kwargs)

                recorder.to_resset().save(td)
                upload_directory_as_archive(
                    local_directory=td,
                    repo_id=_REMOTE_REPOSITORY,
                    repo_type='dataset',
                    archive_in_repo=f'responses_httpx/{_name}.zip',
                )

            return retval

        _KNOWN_RECORDERS[_name] = _new_func
        return _new_func

    return _decorator


def record_site(name: str):
    return _KNOWN_RECORDERS[name]()
