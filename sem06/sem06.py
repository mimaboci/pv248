from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json as jason
import sqlite3
from json2html import *

#url = "GET /result?q=search+term&f=json"

def search(composer, is_json):
    con = sqlite3.connect('scorelib.dat')
    cur = con.cursor()
    res = cur.execute("select person.name, score.name, print.id "
                      "from person left join score_author on person.id=score_author.composer "
                      "join score on score_author.score=score.id "
                      "join edition on edition.score = score.id "
                      "join print on print.edition = edition.id "
                      "where person.name like ? order by person.name", ("%{}%".format(composer),))

    out = []
    for row in res:
        d = {}
        d['Composer'] = row[0]
        d['Score'] = row[1]
        d['Print Number'] = row[2]
    
        out.append(d)

    json_out = jason.dumps(out, indent=2)
    con.close()
    
    if is_json:
        return json_out
    else:
        return json2html.convert(json=json_out)

class server(BaseHTTPRequestHandler):

    def do_GET(self):        
        parsed = urlparse(self.path[1:])
        format_ = 'html'
        is_json = False
        comp = ''
        body = ''
        if parsed.path == 'result':
            query = parse_qs(parsed.query)
            if 'f' in query.keys() and 'json' == query['f'][0]:
                is_json = True
                format_ = 'json'
            if 'q' in query.keys():
                comp = query['q'][0]
            body = search(comp, is_json)
        else:
            form = "<form action=\"/result\" method=\"get\">" \
                   "<p>composer:<input type=\"text\" name=\"q\"></p>" \
                   "<p><input type=\"radio\" name=\"f\" value=\"html\" checked>Html</p>" \
                   "<p><input type=\"radio\" name=\"f\" value=\"json\" >Json</p>" \
                   "<p><input type=\"submit\" value=\"Submit\"></p></form>"
            
        self.send_response(200)
        self.send_header('Content-type', 'text/' + format_ + '; charset=utf8')
        self.end_headers()
        if parsed.path != 'result':
            self.wfile.write(form.encode())
        elif is_json:
            self.wfile.write(body.encode())
        else:
            self.wfile.write(bytes('<html><head><title>title</title></head><body><p>%s</p></body></html>' %body, 'utf8'))

address = ('localhost', 8000)
httpd = HTTPServer(address, server)
    
def start():
    print("server running")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("server stopped")

start()
