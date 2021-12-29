from http.server import BaseHTTPRequestHandler
import json
import random, string
from minesweeper import Minesweeper

games = {}

class MinesweeperRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            global games

            # Check path
            path = list(filter(bool, self.path[:].split('/')))
            if len(path) != 1 or path[0] not in games:
                self.send_response(404)
                self.end_headers()
                return

            # Build response body
            id = path[0]
            game = games[id]
            body = {
                'state': game.game_state,
                'width': game.width,
                'height': game.height,
                'mine_count': game.mine_count,
                'board': game.get_visible_cells()
            }

            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(body).encode('utf-8'))

        except Exception as exception:
            self.send_error(500, explain=repr(exception))
            self.end_headers()


    def do_POST(self):
        try:
            global games

            # Check path
            path = list(filter(bool, self.path[:].split('/')))
            if len(path) != 1 or path[0] not in games:
                self.send_response(404)
                self.end_headers()
                return

            # Parse body parameters
            id = path[0]
            game = games[id]
            parameters = {}
            content_len_str = self.headers.get('Content-Length')
            content_len = int(content_len_str) if content_len_str else 0

            if content_len:
                request_body = self.rfile.read(content_len)
                parameters = json.loads(request_body)
            else:
                self.send_response(400)
                self.end_headers()
                return

            # Perform action
            game.open_cell(parameters['x'], parameters['y'])

            # Send response
            self.send_response(200)
            self.end_headers()

        except Exception as exception:
            self.send_error(500, explain=repr(exception))
            self.end_headers()


    def do_PUT(self):
        try:
            global games

            # Check path
            path = list(filter(bool, self.path[:].split('/')))
            if len(path) != 0:
                self.send_response(400)
                self.end_headers()
                return

            # Parse body parameters
            parameters = {}
            content_len_str = self.headers.get('Content-Length')
            content_len = int(content_len_str) if content_len_str else 0

            if content_len:
                request_body = self.rfile.read(content_len)
                parameters = json.loads(request_body)

            # Create game
            id = None
            while not id or id in games:
                id = ''.join(random.choice(string.ascii_uppercase) for i in range(8))
            games[id] = Minesweeper(
                width=parameters.get('width', 10),
                height=parameters.get('height', 10),
                mine_count=parameters.get('mine_count', 10)
            )

            # Build response body
            body = {
                'id': id
            }

            # Send response
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(body).encode('utf-8'))

        except Exception as exception:
            try:
                del games[id]
            except Exception:
                pass
            finally:
                self.send_error(500, explain=repr(exception))
                self.end_headers()


    def do_DELETE(self):
        try:
            global games

            # Check path
            path = list(filter(bool, self.path[:].split('/')))
            if len(path) != 1 or path[0] not in games:
                self.send_response(404)
                self.end_headers()
                return

            # Build response body
            id = path[0]
            del games[id]

            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

        except Exception as exception:
            self.send_error(500, explain=repr(exception))
            self.end_headers()
