from http.server import ThreadingHTTPServer
from handler import MinesweeperRequestHandler

httpd = ThreadingHTTPServer(('', 8000), MinesweeperRequestHandler)
httpd.serve_forever()
