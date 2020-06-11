import socket
import pickle
from packet import DataPacket, AckPacket, RequestPacket
import threading
import os
import math

WINDOW_SIZE = 10

class Handler:
    def __init__(self, socket):
        self.socket = socket


    def send_file(self, file_path, destination):
        self.socket.settimeout(5)

        last_packet = 0
        last_ack_packet = 0
        file_size = os.path.getsize(file_path)
        total_packet = math.ceil(file_size / 50000)
        sent_packets = []

        with open(file_path, "rb") as f:
            while True:
                while last_packet - last_ack_packet < WINDOW_SIZE and last_packet < total_packet:
                    data = f.read(50000)
                    packet = DataPacket(data, last_packet, last_packet == total_packet - 1)

                    self.socket.sendto(pickle.dumps(packet), destination)

                    sent_packets.append(packet)
                    last_packet += 1

                try:
                    packet, _ = self.socket.recvfrom(65000)

                    pckSeq = int(packet)

                    if pckSeq == total_packet:
                        break

                    last_ack_packet = max(last_ack_packet, pckSeq)

                except socket.timeout:
                    for i in range(last_ack_packet, last_packet):
                        packet = pickle.dumps(sent_packets[i])
                        self.socket.sendto(packet, destination)

class Server:
    def __init__(self, socket):
        self.socket = socket
        self.connections = []

    def listen_for_connection(self):
        while True:
            packet, address = self.socket.recvfrom(65000)

            packet = pickle.loads(packet)

            # Créer un socket avec un port libre
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(("127.0.0.1", 0))

            if address not in self.connections:
                self.connections.append(address)

                handler = Handler(sock)
                
                thread = threading.Thread(target=handler.send_file, args=("server.pdf", address))
                thread.start()

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 9000))
    Server(sock).listen_for_connection()

if __name__ == "__main__":
    main()
