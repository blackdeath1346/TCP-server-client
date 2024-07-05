import socket
import threading

class Client:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 8000
        self.cl_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cl_sock.connect((self.host, self.port))

    def start(self):
        recv_thread = threading.Thread(target=self.recv_messages)
        recv_thread.start()

        while True:
            message = input()
            self.send_message(message)

    def recv_messages(self):
        while True:
            try:
                message = self.cl_sock.recv(1024).decode('utf-8')
                if message:
                    print(message)
                else:
                    break
            except:
                break

    def send_message(self, message):
        try:
            self.cl_sock.send(message.encode('utf-8'))
        except:
            print('Error sending message')

if __name__ == '__main__':
    client = Client()
    client.start()