import SimpleHTTPServer
import SocketServer

def _http_server():
    PORT = 8000

    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

    httpd = SocketServer.TCPServer(("", PORT), Handler)

    httpd.serve_forever()
