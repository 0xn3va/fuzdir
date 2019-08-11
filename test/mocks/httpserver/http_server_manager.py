import threading

from test.mocks.httpserver.threading_http_server import ThreadingHTTPServer


class HTTPServerManager:
    def __init__(self, handler, port: int = 8000):
        self._http_server = ThreadingHTTPServer(('localhost', port), handler)

    def __enter__(self):
        thread = threading.Thread(target=self._http_server.serve_forever)
        thread.daemon = True
        thread.start()
        return self._http_server

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._http_server.server_close()
        self._http_server.shutdown()
