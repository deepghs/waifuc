import os.path
from contextlib import contextmanager

from hbutils.testing import isolated_directory

TESTFILE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'testfile'))


@contextmanager
def isolated_to_testfile():
    items = os.listdir(TESTFILE_DIR)
    with isolated_directory({item: os.path.join(TESTFILE_DIR, item) for item in items}):
        yield


def get_testfile(filename, *segs):
    return os.path.normpath(os.path.join(TESTFILE_DIR, filename, *segs))
