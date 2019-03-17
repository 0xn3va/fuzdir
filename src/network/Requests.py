import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from urllib3.util import parse_url, Url

from src.network.utils import Headers, Schemes
from src.utils.UserAgents import UserAgents


class Requests:
    headers = {
        Headers.accept_lang: 'en-us',
        Headers.cache_control: 'max-age=0',
    }

    def __init__(self, url: str, cookie: str = None, user_agent: str = None, timeout: int = 5):

        def add_retry_adapter(session,
                              retries: int = 3,
                              backoff_factor: float = 0.3,
                              status_forcelist: list = (500, 502, 504)):
            retry = Retry(
                total=retries,
                read=retries,
                connect=retries,
                backoff_factor=backoff_factor,
                status_forcelist=status_forcelist,
            )
            adapter = HTTPAdapter(max_retries=retry)
            # todo('Add handler')
            for s in Schemes.allowable:
                session.mount('%s://' % (s,), adapter)

        # url
        parsed_url = parse_url(url)

        scheme = parsed_url.scheme or Schemes.default
        host = parsed_url.host
        if host is None:
            # todo('raise exception')
            pass
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

    def request(self, path: str):
        try:
            headers = dict(self.headers)
            url = self._url + path

            headers[
                Headers.user_agent] = self._user_agent if self._user_agent is not None else UserAgents.random_ua()

            response = self._session.get(
                url=url,
                headers=headers,
                timeout=self._timeout,
                verify=False
            )

            print(response)
        except requests.exceptions.TooManyRedirects as e:
            print('TooManyRedirects', str(e))
            pass
        except requests.exceptions.SSLError as e:
            print('SSLError', str(e))
            pass
        except requests.exceptions.ConnectionError as e:
            print('ConnectionError', str(e))
            pass
