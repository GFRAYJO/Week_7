from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
from urllib.parse import urlparse, parse_qs
import json

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    server_lookup = {}

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        print(self.path)

        query = parse_qs(urlparse(self.path).query)

        server_name = query['server_name'][0]

        response = BytesIO()

        if server_name in self.server_lookup.keys():
            response.write(self.server_lookup[server_name].encode())
        else:
            response.write(''.encode())

        self.wfile.write(response.getvalue())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body)

        self.server_lookup.update(data)

        print(self.server_lookup)

        self.send_response(200)
        self.end_headers()


httpd = HTTPServer(('localhost', 9500), SimpleHTTPRequestHandler)
httpd.serve_forever()