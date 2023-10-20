import logging

from responses import _recorder

from waifuc.source import SafebooruSource
from .testfile import get_testfile

logging.basicConfig(level=logging.DEBUG)


@_recorder.record(file_path=get_testfile('safebooru.yaml'))
def main():
    s1 = SafebooruSource(['1girl', 'solo'])
    items = list(s1[:10])


if __name__ == '__main__':
    main()
