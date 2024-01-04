import os.path
from hashlib import sha256

import pytest
from hbutils.testing import disable_output

from waifuc.utils import download_file
from ..testings import isolated_to_testfile


@pytest.fixture(scope='session')
def url_to_game_character_skins():
    yield 'https://huggingface.co/datasets/deepghs/game_character_skins/resolve/main'


@pytest.mark.unittest
class TestUtilsDownload:
    @isolated_to_testfile()
    def test_download_file(self, url_to_game_character_skins):
        with disable_output():
            download_file(f'{url_to_game_character_skins}/arknights/NM01/乐逍遥.png', 'nian_skin.png')
            sha = sha256()
            with open('nian_skin.png', 'rb') as f:
                while True:
                    chunk = f.read(2048)
                    if not chunk:
                        break
                    sha.update(chunk)

            assert os.path.getsize('nian_skin.png') == 3832280
            assert sha.hexdigest() == '3333af134d03375958b54d88193dcddfad3a0dd3135bbfd3a6c0988938049073'
