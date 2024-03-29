import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry, disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from urllib3.util import parse_url, Url

from src.network.network_utils import NetworkUtils
from src.network.requester.requester_error import RequesterError
from src.network.requester.utils.header_names import HeaderNames
from src.network.requester.utils.schemes import Schemes
from src.network.requester.throttle.throttle import Throttle

disable_warnings(InsecureRequestWarning)


class Requester:
    default_timeout = 5
    default_retries = 3
    default_status_list = frozenset([502, 503, 504])
    default_http_method = 'GET'
    _min_retries = 0
    _max_retries = 5

    _back_off_factor = 0.3

    def __init__(self,
                 url: str,
                 method: str = default_http_method,
                 user_agent: str = None,
                 cookie: str = None,
                 headers: dict = None,
                 allow_redirect: bool = False,
                 timeout: int = default_timeout,
                 retries: int = default_retries,
                 status_forcelist: set = default_status_list,
                 raise_on_status: bool = True,
                 throttling_period: float = None,
                 proxy: str = None):
        self.method = method
        parsed_url = parse_url(url)
        scheme = parsed_url.scheme or Schemes.default
        if scheme not in Schemes.allowable:
            raise RequesterError(f'Invalid scheme: {scheme}')
        host = parsed_url.host
        if host is None:
            raise RequesterError(f'Invalid url: {url}')
        port = parsed_url.port or Schemes.ports[scheme]
        path = parsed_url.path or '/'
        if not path.endswith('/'):
            path = f'{path}/'
        url = Url(scheme=scheme, auth=parsed_url.auth, host=host, port=port if port != Schemes.ports[scheme] else None,
                  path=path, query=parsed_url.query, fragment=parsed_url.fragment)
        self._url = url.url
        self._user_agent = user_agent

        self._headers = dict([
            (HeaderNames.accept_lang, 'en-us'),
            (HeaderNames.cache_control, 'max-age=0'),
            (HeaderNames.host, f'{host}:{port}' if port != Schemes.ports[scheme] else host)
        ])
        if cookie is not None:
            self._headers[HeaderNames.cookie] = cookie
        if headers is not None:
            self._headers.update(headers)
        self._allow_redirect = allow_redirect
        self._timeout = timeout
        if retries < self._min_retries or retries > self._max_retries:
            raise RequesterError(f'Invalid value of retries: {retries}, allowable values from {self._min_retries} to {self._max_retries} inclusive')
        self._session = requests.Session()
        adapter = HTTPAdapter(
            max_retries=Retry(total=retries, read=retries, connect=retries, backoff_factor=self._back_off_factor,
                              status_forcelist=status_forcelist, raise_on_status=raise_on_status))
        for s in Schemes.allowable:
            self._session.mount(f'{s}://', adapter)
        self._throttle = Throttle(period=throttling_period)
        self._proxies = None if proxy is None else {scheme: proxy}

    @property
    def url(self):
        return self._url

    def request(self, path: str):
        throttle = self._throttle

        @throttle
        def get(func, *args):
            return func(*args)

        return get(self._request, path)

    def _request(self, path: str):
        headers = dict(self._headers)
        headers[HeaderNames.user_agent] = self._user_agent or NetworkUtils.random_ua()
        return self._session.request(method=self.method,
                                     url=f'{self._url}{path}',
                                     headers=headers,
                                     timeout=self._timeout,
                                     allow_redirects=self._allow_redirect,
                                     proxies=self._proxies,
                                     verify=False)
