import http.server
from urllib.parse import urlparse, parse_qs
import json

#url = "GET /result?q=search+term&f=json"

class server(BaseHTTPRequestHandler):
    def return_Json(self, queries):
        return json.dumps(queries)
		
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        query = urlparse(self.path).query
        queries = parse_qs(query)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("<html><head><title>Python</title></head>".encode())
        if "f" in queries.keys() and "json" in queries["f"]:
            self.wfile.write("<body><p>{}</p></body></html>".format(self.getJson(queries)).encode())
        else:
            for (k, v) in queries.items():
                self.wfile.write("<body><p>You sent {} with value {}</p></body></html>".format(k, v).encode())


httpd = HTTPServer(("localhost", 8000), server)
print("server running")
httpd.serve_forever()
