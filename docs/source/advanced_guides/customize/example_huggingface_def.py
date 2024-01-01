import os.path
from typing import Iterator, Tuple, Union

from huggingface_hub import HfApi, HfFileSystem, hf_hub_url

from waifuc.source import WebDataSource


class HuggingfaceSource(WebDataSource):
    def __init__(self, repo_id: str, dir_in_repo: str):
        WebDataSource.__init__(self, group_name='huggingface')
        self.repo_id = repo_id
        self.dir_in_repo = dir_in_repo
        self.hf_fs = HfFileSystem()
        self.hf_client = HfApi()

    def _iter_data(self) -> Iterator[Tuple[Union[str, int], str, dict]]:
        files = self.hf_fs.glob(f'datasets/{self.repo_id}/{self.dir_in_repo}/**/*.png')
        for file in files:
            file_in_repo = os.path.relpath(file, f'datasets/{self.repo_id}')
            rel_file = os.path.relpath(file_in_repo, start=self.dir_in_repo)
            id_ = file_in_repo
            url = hf_hub_url(repo_id=self.repo_id, repo_type='dataset', filename=file_in_repo)
            yield id_, url, {
                'repo_id': self.repo_id,
                'dir_in_repo': self.dir_in_repo,
                'rel_file': rel_file,
                'filename': rel_file,
            }
