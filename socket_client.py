import socket

def _socket_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect(('127.0.0.1',9000))
    s.sendall("delete")
    print s.recv(1024)
    s.close()
if __name__ == '__main__':
    _socket_client()
