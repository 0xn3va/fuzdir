
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
