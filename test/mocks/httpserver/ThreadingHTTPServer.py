import threading
from socketserver import ThreadingMixIn
from http.server import HTTPServer, BaseHTTPRequestHandler


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    def __init__(self, handler: BaseHTTPRequestHandler, port: int = 8000):
        super(ThreadingHTTPServer, self).__init__(('', port), handler)
        self._httpd_thread = None

    def start(self):
        self._httpd_thread = threading.Thread(target=self.serve_forever)
        self._httpd_thread.start()

    def stop(self):
        self.shutdown()
        self._httpd_thread.join()
