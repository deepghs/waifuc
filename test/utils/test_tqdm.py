import pytest
from hbutils.testing import capture_output

from waifuc.utils import tqdm


@pytest.mark.unittest
class TestUtilsTqdm:
    def test_tqdm(self):
        with capture_output() as co:
            values = []
            for i in tqdm(range(10), desc='this is desc'):
                values.append(i)

            assert values == list(range(10))

        assert not co.stdout.strip()
        assert co.stderr.strip()
        assert 'this is desc' in co.stderr

    def test_tqdm_silent(self):
        with capture_output() as co:
            values = []
            for i in tqdm(range(10), desc='this is desc', silent=True):
                values.append(i)

            assert values == list(range(10))

        assert not co.stdout.strip()
        assert not co.stderr.strip()
