import pytest

from waifuc.source import AnimePicturesSource


@pytest.mark.ignore
class TestSourceAnimePictures:

    def test_anime_pictures(self, anime_pictures_surtr, anime_pictures_2girls):
        s1 = AnimePicturesSource(['surtr (arknights)', 'solo'])
        items = list(s1[:10])
        assert len(items) == 10
        for item in items:
            assert 'surtr_(arknights)' in item.meta['tags']

        s1 = AnimePicturesSource(
            ['texas (arknights)', '2girls'],
            denied_tags=['exusiai (arknights)', 'lappland (arknights)']
        )
        items = list(s1[:10])
        assert len(items) == 2
        for item in items:
            assert 'texas_(arknights)' in item.meta['tags']
            assert '2_girls' in item.meta['tags']
            assert 'exusiai_(arknights)' not in item.meta['tags']
            assert 'lappland_(arknights)' not in item.meta['tags']
