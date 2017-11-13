import http.client
import http.server
from urllib.parse import urlparse

class server(BaseHTTPRequestHandler):
    def do_GET(self):
        print("do_GET")
		query = urlparse(self.path).query
		
        self.send_response(200, 'ok')
        self.send_header("Content-type", "text/html")
        self.end_headers()

        message = "You sent {}".format(query)
        self.wfile.write(bytes(message, "utf8"))
        

address = ('localhost', 8000)
httpd = HTTPServer(address, server)
print("server running")
httpd.serve_forever()
