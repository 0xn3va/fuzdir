from requests import Response


class Headers:
    accept_lang = 'Accept-Language'
    cache_control = 'Cache-Control'
    cookie = 'Cookie'
    user_agent = 'User-Agent'
    host = 'Host'
    content_length = 'Content-Length'
    location = 'Location'


class Schemes:
    allowable = ('http', 'https', )
    ports = {
        allowable[0]: 80,
        allowable[1]: 443
    }
    default = allowable[0]


class NetworkUtil:
    @staticmethod
    def content_length(response: Response) -> int:
        if not isinstance(response, Response):
            raise TypeError('Invalid response type')
        try:
            return int(response.headers[Headers.content_length])
        except (KeyError, ValueError):
            # length of responses body
            return len(response.content)
