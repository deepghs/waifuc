import os.path
import zipfile
from functools import wraps
from typing import Optional

from hbutils.system import TemporaryDirectory
from huggingface_hub import HfApi

from waifuc.export import SaveExporter
from waifuc.source import BaseDataSource

_KNOWN_DATASOURCES = {}
_REMOTE_REPOSITORY = 'deepghs/waifuc_unittest'
hf_client = HfApi(token=os.environ.get('HF_TOKEN'))


def register_datasource(name: Optional[str] = None):
    def _decorator(func):
        _name = name or func.__name__

        if _name in _KNOWN_DATASOURCES:
            raise NameError(f'Unittest datasource already registered - {_name!r}.')

        @wraps(func)
        def _new_func(*args, **kwargs):
            source: BaseDataSource = func(*args, **kwargs)
            with TemporaryDirectory() as td:
                origin_dir = os.path.join(td, 'origin')
                os.makedirs(origin_dir, exist_ok=True)
                source.export(SaveExporter(origin_dir))

                zip_file = os.path.join(td, f'{_name}.zip')
                with zipfile.ZipFile(zip_file, 'w') as zf:
                    for root, dirs, files in os.walk(origin_dir):
                        for file in files:
                            filepath = os.path.join(origin_dir, root, file)
                            zf.write(filepath, os.path.relpath(filepath, origin_dir))

                hf_client.upload_file(
                    path_or_fileobj=zip_file,
                    path_in_repo=f'datasources/{_name}.zip',
                    repo_id=_REMOTE_REPOSITORY,
                    repo_type='dataset'
                )

        _KNOWN_DATASOURCES[_name] = _new_func
        return _new_func

    return _decorator


def record_datasource(name: str):
    return _KNOWN_DATASOURCES[name]()
