from typing import Optional

import filetype


def get_file_type(file) -> Optional[str]:
    guess = filetype.guess(file)
    if guess:
        return guess.mime.split('/', maxsplit=1)[0]
    else:
        return None
