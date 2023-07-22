import os
import zipfile
from typing import Type, Optional, Mapping, Any

from hbutils.system import TemporaryDirectory
from huggingface_hub import HfApi

from .base import LocalDirectoryExporter, BaseExporter
from ..model import ImageItem


class HuggingFaceExporter(BaseExporter):
    def __init__(self, repository: str, file_in_repo: str,
                 cls: Type[LocalDirectoryExporter], args: tuple = (), kwargs: Optional[Mapping[str, Any]] = None,
                 repo_type: str = 'dataset', revision: str = 'main', hf_token: Optional[str] = None):
        self.repository = repository
        self.repo_type, self.revision = repo_type, revision
        self.file_in_repo = file_in_repo
        self.cls, self.args, self.kwargs = (cls, args, kwargs or {})
        self._tempdir: Optional[TemporaryDirectory] = None
        self._exporter: Optional[LocalDirectoryExporter] = None
        self.hf_token = hf_token or os.environ.get('HF_TOKEN')

    def pre_export(self):
        self._tempdir = TemporaryDirectory()
        self._exporter = self.cls(self._tempdir.name, *self.args, **self.kwargs)
        self._exporter.pre_export()

    def export_item(self, item: ImageItem):
        self._exporter.export_item(item)

    def post_export(self):
        self._exporter.post_export()

        # upload to huggingface
        hf_api = HfApi(token=self.hf_token)
        hf_api.create_repo(self.repository, repo_type=self.repo_type, exist_ok=True)
        with TemporaryDirectory() as td:
            zip_file = os.path.join(td, 'package.zip')
            with zipfile.ZipFile(zip_file, mode='w') as zf:
                for directory, _, files in os.walk(self._tempdir.name):
                    for file in files:
                        file_path = os.path.join(directory, file)
                        rel_file_path = os.path.relpath(file_path, self._tempdir.name)
                        zf.write(
                            file_path,
                            '/'.join(rel_file_path.split(os.sep))
                        )

            hf_api.upload_file(
                path_or_fileobj=zip_file,
                repo_id=self.repository,
                repo_type=self.repo_type,
                path_in_repo=self.file_in_repo,
                revision=self.revision,
                commit_message=f'Upload {self.file_in_repo} with waifuc'
            )

        self._exporter = None
        self._tempdir.cleanup()
        self._tempdir = None

    def reset(self):
        pass
