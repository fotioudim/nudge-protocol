import socket

from . import protocol

# ==========================================
# Handles discovery logic
# ==========================================
class Scanner:
    def __init__(self, add_ui_callback):
        self.found_devices = {}
        self.add_ui_callback = add_ui_callback

    def broadcast_search(self):
        self.found_devices.clear()
        packet = protocol.MAGIC_HEADER + protocol.CMD_DISCOVERY_REQ
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                s.sendto(packet, ("255.255.255.255", protocol.DEFAULT_PORT))
        except Exception as e:
            print(f"Discovery Error: {e}")

    def register(self, ip, name):
        if ip not in self.found_devices:
            self.found_devices[ip] = name
            self.add_ui_callback(ip, name)