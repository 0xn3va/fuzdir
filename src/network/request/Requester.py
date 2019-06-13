import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry, disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from urllib3.util import parse_url, Url

from src.network.RequestError import RequestError
from src.network.Throttle import Throttle
from src.network.utils import Headers, Schemes
from src.network.Response import Response, ResponseType
from src.utils.UserAgents import UserAgents

disable_warnings(InsecureRequestWarning)


class Requester:
    headers = {
        Headers.accept_lang: 'en-us',
        Headers.cache_control: 'max-age=0',
    }

    def __init__(self, url: str, cookie: str = None, user_agent: str = None, timeout: int = 5,
                 allow_redirects: bool = False):

        def add_retry_adapter(session, retries: int = 3, backoff_factor: float = 0.3,
                              status_forcelist: list = (502, 504,)):
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
        self.headers[Headers.host] = '%s:%d' % (host, port,) if port != Schemes.ports[scheme] else host
        #
        self._user_agent = user_agent
        self._timeout = timeout

        if cookie is not None:
            self.headers[Headers.cookie] = cookie

        self._session = requests.Session()
        add_retry_adapter(self._session)

        self._allow_redirects = allow_redirects

        self._throttle = Throttle(period=0.25 * 1e+6)

    @property
    def url(self):
        return self._url

    def request(self, path: str):
        self._throttle.delay()
        message = self._request(path)
        if message.type == ResponseType.response:
            self._throttle.update(message.body.elapsed)
        return message

    def _request(self, path: str):
        try:
            headers = dict(self.headers)
            url = self._url + path

            headers[Headers.user_agent] = self._user_agent if self._user_agent is not None else UserAgents.random_ua()

            response = self._session.get(
                url=url,
                headers=headers,
                timeout=self._timeout,
                allow_redirects=self._allow_redirects,
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
