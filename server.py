import socket
import threading

class Receiver:
    def __init__(self, socket, client_address):
        self.socket = socket
        self.client_address = client_address
        self.isDone = False

    def initialize_client_connection(self):
        while True:
            try:
                self.socket.sendto(str.encode("RACK"), self.client_address)
                self.socket.recvfrom()
            except socket.timeout:
                pass    
            finally:
                if self.isDone:
                    break

    def receive(self):


class Server:
    def __init__(self, socket):
        self.socket = socket
    
    def handle_request(self, packet, address):
        pass

    def listen(self):
        while True:
            packet, address = self.socket.recvfrom(1200)
            thread = threading.Thread(target=self.handle_request, args=(packet, address))
            thread.daemon = True
            thread.start()

def main():
    print("server")

if __name__ == "__main__":
    main()