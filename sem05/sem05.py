import http.client
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

class server(BaseHTTPRequestHandler):
    def do_GET(self):
        print("do_GET")
        query = urlparse(self.path).query
        self.send_response(200, 'ok')
        self.send_header("Content-type", "text/html")
        self.end_headers()

        message = "You asked for {}".format(self.path[1:])
        self.wfile.write(bytes('<html><head><title>title</title></head>', 'utf8'))
        self.wfile.write(bytes("<body><p>body</p>", 'utf8'))
        self.wfile.write(bytes("<p>%s</p>" %message, 'utf8'))
        self.wfile.write(bytes("</body></html>", 'utf8'))        

def start():
    address = ('localhost', 8000)
    httpd = HTTPServer(address, server)
    print("server running")
    httpd.serve_forever()
    
def exit():
    httpd.server_close()
    print("server stopped")

start()
