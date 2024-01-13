import time
import warnings
from functools import lru_cache
from typing import Optional, Dict

import httpx
import requests
from random_user_agent.params import SoftwareName, OperatingSystem
from random_user_agent.user_agent import UserAgent
from requests.adapters import HTTPAdapter, Retry

DEFAULT_TIMEOUT = 10  # seconds


class TimeoutHTTPAdapter(HTTPAdapter):
    """
    Custom HTTP adapter that sets a default timeout for requests.

    Inherits from `HTTPAdapter`.

    Usage:
    - Create an instance of `TimeoutHTTPAdapter` and pass it to a `requests.Session` object's `mount` method.

    Example:
    ```python
    session = requests.Session()
    adapter = TimeoutHTTPAdapter(timeout=10)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    ```

    :param timeout: The default timeout value in seconds. (default: 10)
    :type timeout: int
    """

    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        """
        Sends a request with the provided timeout value.

        :param request: The request to send.
        :type request: PreparedRequest
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :returns: The response from the request.
        :rtype: Response
        """
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


def get_requests_session(max_retries: int = 5, timeout: int = DEFAULT_TIMEOUT,
                         headers: Optional[Dict[str, str]] = None,
                         session: Optional[httpx.Client] = None) -> httpx.Client:
    session = session or httpx.Client(http2=True, timeout=timeout, follow_redirects=True)
    if isinstance(session, requests.Session):
        retries = Retry(
            total=max_retries, backoff_factor=1,
            status_forcelist=[408, 413, 429, 500, 501, 502, 503, 504, 505, 506, 507, 509, 510, 511],
            allowed_methods=["HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS", "TRACE"],
        )
        adapter = TimeoutHTTPAdapter(max_retries=retries, timeout=timeout, pool_connections=32, pool_maxsize=32)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        **dict(headers or {}),
    })

    return session


RETRY_ALLOWED_METHODS = ["HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS", "TRACE"]
RETRY_STATUS_FORCELIST = [413, 429, 500, 501, 502, 503, 504, 505, 506, 507, 509, 510, 511]


def _should_retry(response: httpx.Response) -> bool:
    return response.request.method in RETRY_ALLOWED_METHODS and \
        response.status_code in RETRY_STATUS_FORCELIST


def srequest(session: httpx.Client, method, url, *, max_retries: int = 5,
             backoff_factor: float = 1.0, raise_for_status: bool = True, **kwargs) -> httpx.Response:
    resp = None
    for i in range(max_retries):
        sleep_time = backoff_factor * (2 ** i)
        try:
            resp = session.request(method, url, **kwargs)
            if raise_for_status:
                resp.raise_for_status()
        except (httpx.TooManyRedirects,):
            raise
        except httpx.HTTPStatusError as err:
            if _should_retry(err.response):
                warnings.warn(f'Requests {err.response.status_code} ({i + 1}/{max_retries}), '
                              f'sleep for {sleep_time!r}s ...')
                time.sleep(sleep_time)
            else:
                raise
        except httpx.HTTPError as err:
            warnings.warn(f'Requests error ({i + 1}/{max_retries}): {err!r}, '
                          f'sleep for {sleep_time!r}s ...')
            time.sleep(sleep_time)
        else:
            break

    assert resp is not None, f'Request failed for {max_retries} time(s) - {method} {url!r}.'
    if raise_for_status:
        resp.raise_for_status()

    return resp


@lru_cache()
def _ua_pool():
    software_names = [SoftwareName.CHROME.value, SoftwareName.FIREFOX.value, SoftwareName.EDGE.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.MACOS.value]

    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=1000)
    return user_agent_rotator


def get_random_ua():
    return _ua_pool().get_random_user_agent()
