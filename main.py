from http.server import HTTPServer, BaseHTTPRequestHandler
from modules.user_interface import user_interface as UI

class Server(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.path = '/modules/user_interface/user_interface.html'
        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file_to_open = "File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        query = post_data.decode('utf-8').split("=")[1] # Hacky but for now working
        
        UI.test(query)


httpd = HTTPServer(('localhost', 8080), Server)
httpd.serve_forever()