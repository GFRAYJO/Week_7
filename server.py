from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import socket
import json

HOST = socket.gethostname() 
PORT = 9500

serverName = 'server1'
serverPK = 'session cipher key'

ca = http.client.HTTPConnection(HOST, 9500)
params = json.dumps({SERVER_NAME: SERVER_PUBLIC_KEY})
ca.request("POST", "", params)
response = ca.getresponse()

print(response.status)

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()

        self.wfile.write(SERVER_NAME.encode())

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        content_length = int(self.headers['Content-Length'])
        body = json.loads(self.rfile.read(content_length))

        client_text = body['cipher_text']
        server_text = self.encode(SERVER_PUBLIC_KEY, 'session cipher key').decode()

        response = BytesIO()

        if client_text == server_text:
            response.write(b'session cipher key')
        else:
            response.write(b'Goodbye')
        
        self.wfile.write(response.getvalue())

    def encode(self, key, string):
        encoded_chars = []
        for i in range(len(string)):
            key_c = key[i % len(key)]
            encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
            encoded_chars.append(encoded_c)
        encoded_string = "".join(encoded_chars)
        return base64.urlsafe_b64encode(encoded_string.encode())


httpd = HTTPServer(('localhost', 9500), SimpleHTTPRequestHandler)
httpd.serve_forever()