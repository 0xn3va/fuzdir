import threading

from test.mocks.httpserver.threading_http_server import ThreadingHTTPServer


class HTTPServerManager:
    def __init__(self, handler, port):
        hostname = 'localhost'
        self.url = 'http://%s:%d' % (hostname, port,)
        self._http_server = ThreadingHTTPServer((hostname, port), handler)

    def __enter__(self):
        thread = threading.Thread(target=self._http_server.serve_forever)
        thread.daemon = True
        thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._http_server.server_close()
        self._http_server.shutdown()
