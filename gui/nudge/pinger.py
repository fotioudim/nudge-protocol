import socket

from . import protocol

# ==========================================
# Handles Sending NUDGE packets
# ==========================================
class Pinger:
    def send(self, targets, sender_name):
        packet = protocol.MAGIC_HEADER + protocol.CMD_NUDGE + sender_name.encode('ascii', errors='ignore')
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                for ip in targets:
                    s.sendto(packet, (ip, protocol.DEFAULT_PORT))
            return True, None
        except Exception as e:
            return False, str(e)