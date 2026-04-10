import socket
import argparse

def send_nudge(target_ip, sender_name):
    # 1. Build the NUDGE packet
    packet = b'NUDG\x01' + sender_name.encode('ascii')
    
    # 2. Set up a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Enable broadcast mode
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    # 3. Send the packet
    try:
        sock.sendto(packet, (target_ip, 7777))
        print(f"[SUCCESS] Nudge sent to {target_ip} as '{sender_name}'!")
    except Exception as e:
        print(f"[ERROR] Failed to send nudge: {e}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Send a UDP Nudge across the LAN.")
    
    # Create a mutually exclusive group for broadcast and IP flags
    target_group = parser.add_mutually_exclusive_group()
    
    target_group.add_argument(
        "-b", "--broadcast", 
        action="store_true", 
        help="Broadcast the nudge to everyone"
    )
    
    target_group.add_argument(
        "-i", "--ip", 
        type=str, 
        default="127.0.0.1", 
        help="The specific target IP address (default: 127.0.0.1)"
    )
    
    parser.add_argument(
        "-n", "--name", 
        type=str, 
        default="User", 
        help="The sender name that will appear on the target PC (default: User)"
    )
    
    args = parser.parse_args()
    
    if args.broadcast:
        final_ip = "<broadcast>"
    else:
        final_ip = args.ip
        
    send_nudge(final_ip, args.name)