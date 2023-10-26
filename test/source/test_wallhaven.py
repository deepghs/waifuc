import pytest
import responses

from waifuc.source import WallHavenSource


@pytest.mark.unittest
class TestSourceWallhaven:
    @responses.activate
    def test_wallhaven(self, wallhaven_surtr, wallhaven_id_105577):
        source = WallHavenSource('surtr (arknights)')
        items = list(source[:20])
        assert len(items) == 20

        source = WallHavenSource('id:105577')
        items = list(source[:20])
        assert len(items) == 20
