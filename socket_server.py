import socket
import time
import sys
import file_change_finder
def _socket_server():
    HOST = '127.0.0.1'
    PORT = 9000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((HOST,PORT))
    s.listen(1)
    while 1:
        conn,addr = s.accept()
        data = conn.recv(1024)
        if not data:
            break
        if data == "delete":
            conn.sendall("Success Deleted!")


if __name__ == '__main__':
    _socket_server()
