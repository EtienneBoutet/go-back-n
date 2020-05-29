import socket

class Client:
    def __init__(self):
        self.status = "START"
        self.socket = None
        self.socket.settimeout(3)
        self.target_ip = None
        self.target_port = None
        self.packets_to_send = []

    def send_packets(self, packet):
        for packet in self.packets_to_send:
            self.socket.sendto(packet, (self.target_ip, self.target_port))

    def receive_packet(self):
        try:
            return self.socket.recvfrom(65000)
        except socket.timeout:
            return None

    def handle_received_packet(self, packet):
        if packet is not None:
            if packet.status == "RACK":
                self.status = "DATA"
            elif packet.status == "ACK":
                pass

    def communicate(self):
        while True:
            packet = self.get_packet_to_send()
            self.send_packet(packet)
            recv_packet = self.receive_packet()
            self.handle_received_packet(recv_packet)

def main():
    Client().communicate()

if __name__ == "__main__":
    main()