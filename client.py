import socket
from packet import RequestPacket, AckPacket
import pickle

class Client:
    def __init__(self, socket):
        self.socket = socket
        self.is_last_packet_received = False
        self.waiting_for = 0
        self.received_packets = []

    def listen(self):
        while True:
            packet, address = self.socket.recvfrom(65000)
            packet = pickle.loads(packet)

            if packet.lastPck == self.waiting_for:
                self.waiting_for += 1

                self.received_packets.append(packet)

                if packet.isLast:
                    self.is_last_packet_received = True

            self.socket.sendto(str.encode(str(self.waiting_for)), address)

    def initiate_connection(self):
        self.socket.settimeout(5)
        
        req_packet = RequestPacket("r")

        while True:
            self.socket.sendto(pickle.dumps(req_packet), ("127.0.0.1", 9000))

            try:
                self.listen()
            except socket.timeout:
                if self.is_last_packet_received:
                    break

        print("Done receiving from server.")

        with open("from_server.pdf", "a+b") as f:
            for packet in self.received_packets:
                f.write(packet.data)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 0))

    Client(sock).initiate_connection()

if __name__ == "__main__":
    main()
