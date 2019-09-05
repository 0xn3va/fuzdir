from http.server import BaseHTTPRequestHandler


class HTTPRequestHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def _set_headers(self, status_code: int, headers: dict):
        self.send_response(status_code)
        for key, value in headers.items():
            self.send_header(key, value)
        self.end_headers()

    def log_message(self, format, *args):
        # logging disable
        return
