import os
from contextlib import contextmanager
from typing import Union

import httpx
import requests
from tqdm.auto import tqdm

from .session import get_requests_session
from .tqdm_ import tqdm


@contextmanager
def _get_stream(session: Union[httpx.Client, requests.Session], url, **kwargs):
    if isinstance(session, httpx.Client):
        with session.stream('GET', url, **kwargs) as response:
            yield response
    else:
        response = session.get(url, **kwargs, stream=True)
        yield response


def download_file(url, filename, expected_size: int = None, desc=None, session=None, silent: bool = False, **kwargs):
    session = session or get_requests_session()
    with _get_stream(session, url, **kwargs) as response:
        response: Union[httpx.Response, requests.Response]
        expected_size = expected_size or response.headers.get('Content-Length', None)
        expected_size = int(expected_size) if expected_size is not None else expected_size

        desc = desc or os.path.basename(filename)
        directory = os.path.dirname(filename)
        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(filename, 'wb') as f:
            with tqdm(total=expected_size, unit='B', unit_scale=True,
                      unit_divisor=1024, desc=desc, silent=silent) as pbar:
                if isinstance(response, httpx.Response):
                    for chunk in response.iter_bytes(chunk_size=1024):
                        f.write(chunk)
                        pbar.update(len(chunk))
                else:
                    for chunk in response.iter_content(chunk_size=1024):
                        f.write(chunk)
                        pbar.update(len(chunk))

        actual_size = os.path.getsize(filename)
        if expected_size is not None and actual_size != expected_size:
            os.remove(filename)
            raise httpx.HTTPError(f"Downloaded file is not of expected size, "
                                  f"{expected_size} expected but {actual_size} found.")

        return filename
