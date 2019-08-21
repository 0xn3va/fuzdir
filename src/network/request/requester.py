import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry, disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from urllib3.util import parse_url, Url

from src.network.request.header_names import HeaderNames
from src.network.request.request_error import RequestError
from src.network.request.schemes import Schemes
from src.network.request.throttle.throttle import Throttle
from src.network.response.response import Response
from src.network.response.response_type import ResponseType
from src.utils.user_agents import UserAgents

disable_warnings(InsecureRequestWarning)


class Requester:
    headers = {
        HeaderNames.accept_lang: 'en-us',
        HeaderNames.cache_control: 'max-age=0',
    }

    def __init__(self, url: str, cookie: str = None, user_agent: str = None, timeout: int = 5,
                 allow_redirects: bool = False, throttling_period: float = None, proxy: str = None):

        def add_retry_adapter(session, retries: int = 3, backoff_factor: float = 0.3,
                              status_forcelist: list = (500, 502, 503, 504,)):
            retry = Retry(
                total=retries,
                read=retries,
                connect=retries,
                backoff_factor=backoff_factor,
                status_forcelist=status_forcelist,
            )
            adapter = HTTPAdapter(max_retries=retry)
            for s in Schemes.allowable:
                session.mount('%s://' % (s,), adapter)

        # url
        parsed_url = parse_url(url)

        scheme = parsed_url.scheme or Schemes.default
        if scheme not in Schemes.allowable:
            raise RequestError('Invalid scheme: %s' % (scheme,))
        host = parsed_url.host
        if host is None:
            raise RequestError('Invalid url: %s' % (url,))

        port = parsed_url.port or Schemes.ports[scheme]
        path = parsed_url.path or '/'
        if not path.endswith('/'):
            path = '%s/' % (path,)

        url = Url(scheme=scheme,
                  auth=parsed_url.auth,
                  host=host,
                  port=port,
                  path=path,
                  query=parsed_url.query,
                  fragment=parsed_url.fragment)

        self._url = url.url
        #
        self.headers[HeaderNames.host] = '%s:%d' % (host, port,) if port != Schemes.ports[scheme] else host
        #
        self._user_agent = user_agent
        self._timeout = timeout

        if cookie is not None:
            self.headers[HeaderNames.cookie] = cookie

        self._session = requests.Session()
        add_retry_adapter(self._session)

        self._allow_redirects = allow_redirects
        self._throttle = Throttle(period=throttling_period)
        self._proxies = None if proxy is None else {scheme: proxy}

    @property
    def url(self):
        return self._url

    def request(self, path: str):
        @self._throttle
        def get():
            return self._request('GET', path)
        return get()

    def _request(self, method, path: str):
        try:
            url = self._url + path
            headers = dict(self.headers)
            headers[HeaderNames.user_agent] = self._user_agent if self._user_agent is not None else UserAgents.random_ua()
            response = self._session.request(
                method=method,
                url=url,
                headers=headers,
                timeout=self._timeout,
                allow_redirects=self._allow_redirects,
                proxies=self._proxies,
                verify=False
            )
            return Response(ResponseType.response, response)
        except requests.exceptions.TooManyRedirects as e:
            raise RequestError('Too many redirects: %s' % (str(e),))
        except requests.exceptions.SSLError:
            raise RequestError('SSL error connection to server')
        except requests.exceptions.ConnectionError:
            raise RequestError('Failed to establish a connection with %s' % (self.url,))
        except requests.exceptions.RetryError as e:
            return Response(ResponseType.error, e)
        except Exception as e:
            raise RequestError(str(e))
