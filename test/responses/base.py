import os.path
import zipfile
from functools import wraps
from typing import Optional

from hbutils.system import TemporaryDirectory
from huggingface_hub import HfApi
from responses import _recorder

_KNOWN_RECORDERS = {}
_REMOTE_REPOSITORY = 'deepghs/waifuc_responses'
hf_client = HfApi(token=os.environ.get('HF_TOKEN'))


def resp_recorder(name: Optional[str] = None):
    def _decorator(func):
        _name = name or func.__name__

        @wraps(func)
        def _new_func(*args, **kwargs):
            with TemporaryDirectory() as td:
                file_path = os.path.join(td, f'{_name}.yaml')
                f = _recorder.record(file_path=file_path)(func)
                retval = f(*args, **kwargs)

                with TemporaryDirectory() as ztd:
                    zip_file = os.path.join(ztd, f'{_name}.zip')
                    with zipfile.ZipFile(zip_file, 'w') as zf:
                        for root, dirs, files in os.walk(td):
                            for file in files:
                                filepath = os.path.join(td, root, file)
                                zf.write(filepath, os.path.relpath(filepath, td))

                    hf_client.upload_file(
                        path_or_fileobj=zip_file,
                        path_in_repo=f'{_name}.zip',
                        repo_id=_REMOTE_REPOSITORY,
                        repo_type='dataset'
                    )

            return retval

        _KNOWN_RECORDERS[_name] = _new_func
        return _new_func

    return _decorator


def record_site(name: str):
    return _KNOWN_RECORDERS[name]()
