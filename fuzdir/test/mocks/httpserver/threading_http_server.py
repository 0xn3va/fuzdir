from socketserver import ThreadingMixIn
from http.server import HTTPServer


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
