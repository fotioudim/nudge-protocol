import threading
import socket

from . import protocol

# ==========================================
# Handles incoming NUDGE packets
# ==========================================
class Listener:
    def __init__(self, name_provider, nudge_callback, scan_callback):
        self.name_provider = name_provider
        self.nudge_callback = nudge_callback
        self.scan_callback = scan_callback
        self.running = False
        self.sock = None

    def start(self):
        if self.running: return
        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()

    def stop(self):
        self.running = False
        if self.sock:
            self.sock.close() # Closing the socket breaks the recvfrom block

    def _loop(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.sock.bind(('0.0.0.0', protocol.DEFAULT_PORT))
        except: 
            self.running = False
            return

        while self.running:
            try:
                data, addr = self.sock.recvfrom(1024)
                if not data.startswith(protocol.MAGIC_HEADER): continue
                
                cmd = data[4:5]
                payload = data[5:].decode('ascii', errors='ignore')

                if cmd == protocol.CMD_NUDGE:
                    self.nudge_callback(payload, addr[0])
                elif cmd == protocol.CMD_DISCOVERY_REQ:
                    resp = protocol.MAGIC_HEADER + protocol.CMD_DISCOVERY_RES + self.name_provider().encode('ascii', errors='ignore')
                    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as rs:
                        rs.sendto(resp, (addr[0], protocol.DEFAULT_PORT))
                elif cmd == protocol.CMD_DISCOVERY_RES:
                    self.scan_callback(addr[0], payload)
            except: 
                break
        self.running = False
