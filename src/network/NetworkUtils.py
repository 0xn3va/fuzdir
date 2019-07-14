from requests import Response

from src.network.request.HeaderNames import HeaderNames


class NetworkUtils:
    @staticmethod
    def content_length(response: Response) -> int:
        if not isinstance(response, Response):
            raise TypeError('Invalid response type')
        try:
            return int(response.headers[HeaderNames.content_length])
        except (KeyError, ValueError):
            # length of responses body
            return len(response.content)
