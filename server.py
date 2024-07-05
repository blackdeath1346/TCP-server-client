import socket
import threading

class Server:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 8000
        self.serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv_sock.bind((self.host, self.port))
        self.cl_list = []

    def start(self):
        self.serv_sock.listen(5)
        print(f'Server listening on {self.host}:{self.port}')

        while True:
            cl_sock, cl_addr = self.serv_sock.accept()
            print(f'New connection from {cl_addr}')
            cl_thread = threading.Thread(target=self.handle_cl, args=(cl_sock,))
            cl_thread.start()
            self.cl_list.append(cl_sock)

    def handle_cl(self, cl_sock):
        while True:
            try:
                message = cl_sock.recv(1024).decode('utf-8')
                if message:
                    print(f'Received message: {message}')
                    self.broadcast(message, cl_sock)
                else:
                    self.remove_cl(cl_sock)
                    break
            except:
                self.remove_cl(cl_sock)
                break

    def broadcast(self, message, sender_sock):
        for cl_sock in self.cl_list:
            if cl_sock != sender_sock:
                try:
                    cl_sock.send(message.encode('utf-8'))
                except:
                    self.remove_cl(cl_sock)

    def remove_cl(self, cl_sock):
        if cl_sock in self.cl_list:
            self.cl_list.remove(cl_sock)
            cl_sock.close()

if __name__ == '__main__':
    server = Server()
    server.start()
