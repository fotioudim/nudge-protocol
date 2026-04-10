import socket

# 1. Set up a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 2. Bind to all network interfaces on port 7777
sock.bind(('0.0.0.0', 7777))

print("Listening for NUDGES on UDP port 7777...")

while True:
    data, addr = sock.recvfrom(1024) # Wait for a packet
    
    # 3. Check if it matches our protocol (starts with 'NUDG' and Version '1')
    if data.startswith(b'NUDG\x01'):
        # Extract the name (everything after the 5th byte)
        sender_name = data[5:].decode('ascii')
        
        print(f"\a\n*** YOU HAVE BEEN NUDGED BY: {sender_name} ***\n")
    