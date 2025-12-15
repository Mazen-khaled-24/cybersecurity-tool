import socket

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)  # prevent long wait
        result = sock.connect_ex((ip, port))
        if result == 0:
            print(f"[OPEN] Port {port}")
        sock.close()
    except:
        pass

def main():
    print("=== Basic Port Scanner ===")
    target_ip = input("Enter target IP: ")

    print(f"Scanning {target_ip}...\n")

    for port in range(20, 1000):  # small range for now
        scan_port(target_ip, port)

    print("\nScan complete.")

if __name__ == "__main__":
    main()
