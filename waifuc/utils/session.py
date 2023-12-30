import os
import time
import warnings
from typing import Optional, Dict

if os.environ.get('USE_REQUESTS'):
    import requests
    from requests import Session
    from requests.adapters import HTTPAdapter, Retry
    from requests.exceptions import RequestException

    USE_REQUESTS = True

else:
    from curl_cffi import requests
    from curl_cffi.requests import Session
    from curl_cffi.requests.errors import RequestsError as RequestException

    USE_REQUESTS = False

DEFAULT_TIMEOUT = 10  # seconds

if USE_REQUESTS:
    class TimeoutHTTPAdapter(HTTPAdapter):
        def __init__(self, *args, **kwargs):
            self.timeout = DEFAULT_TIMEOUT
            if "timeout" in kwargs:
                self.timeout = kwargs["timeout"]
                del kwargs["timeout"]
            super().__init__(*args, **kwargs)

        def send(self, request, **kwargs):
            timeout = kwargs.get("timeout")
            if timeout is None:
                kwargs["timeout"] = self.timeout
            return super().send(request, **kwargs)


def get_requests_session(max_retries: int = 5, timeout: int = DEFAULT_TIMEOUT,
                         headers: Optional[Dict[str, str]] = None, session: Optional[Session] = None) \
        -> Session:
    session = session or Session()
    if USE_REQUESTS:
        retries = Retry(
            total=max_retries, backoff_factor=1,
            status_forcelist=[413, 429, 500, 501, 502, 503, 504, 505, 506, 507, 509, 510, 511],
            allowed_methods=["HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS", "TRACE"],
        )
        adapter = TimeoutHTTPAdapter(max_retries=retries, timeout=timeout)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        **dict(headers or {}),
    })

    return session


def srequest(session: Session, method, url, *, max_retries: int = 5,
             sleep_time: float = 5.0, raise_for_status: bool = True, **kwargs) -> requests.Response:
    resp = None
    for _ in range(max_retries):
        try:
            resp = session.request(method, url, **kwargs)
        except RequestException as err:
            time.sleep(sleep_time)
            warnings.warn(f'Requests error: {err!r} ...')
        else:
            break

    assert resp is not None, f'Request failed for {max_retries} time(s) - [{method}] {url!r}.'
    if raise_for_status:
        resp.raise_for_status()

    return resp
