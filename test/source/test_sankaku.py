import pytest

from waifuc.source import SankakuSource, PostOrder, FileType


@pytest.mark.ignore
class TestSourceSankaku:

    def test_sankaku(self, sankaku_surtr, sankaku_2dogs, sankaku_texas_yuri):
        source = SankakuSource(
            ['surtr_(arknights)', 'solo'],
            order=PostOrder.QUALITY, file_type=FileType.IMAGE,
            username='yourusername', password='yourpassword'
        )
        items = list(source[:20])
        assert len(items) == 20
        for item in items:
            assert 'surtr_(arknights)' in item.meta['tags']
            assert 'solo' in item.meta['tags']

        source = SankakuSource(
            ['texas_(arknights)', 'lappland_(arknights)', '2girls', '-comic', '-monochrome'],
            order=PostOrder.QUALITY, file_type=FileType.IMAGE,
            username='yourusername', password='yourpassword'
        )
        items = list(source[:20])
        assert len(items) == 20
        for item in items:
            assert 'texas_(arknights)' in item.meta['tags']
            assert 'lappland_(arknights)' in item.meta['tags']
            assert '2girls' in item.meta['tags']
            assert 'comic' not in item.meta['tags']
            assert 'monochrome' not in item.meta['tags']

        source = SankakuSource(
            ['texas_(arknights)', '2girls', '-lappland_(arknights)', '-exusiai_(arknights)'],
            order=PostOrder.QUALITY, file_type=FileType.IMAGE,
            username='yourusername', password='yourpassword'
        )
        items = list(source[:20])
        assert len(items) == 20
        for item in items:
            assert 'texas_(arknights)' in item.meta['tags']
            assert '2girls' in item.meta['tags']
            assert 'lappland_(arknights)' not in item.meta['tags']
            assert 'exusiai_(arknights)' not in item.meta['tags']
