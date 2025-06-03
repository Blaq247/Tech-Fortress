import socket
import sys
import argparse

def grab_banner(target_host, target_port, timeout=5):
    """
    Attempts to grab a banner from the specified host and port.
    """
    print(f"\n[*] Attempting banner grab for {target_host} on port {target_port}...")
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout) # Set a timeout for connection and data reception

        # Connect to the target
        sock.connect((target_host, target_port))

        # For HTTP, send a simple GET request to provoke a response
        # For other services, simply receiving data often works
        if target_port == 80 or target_port == 443: # Common web ports
            # Basic HTTP GET request
            sock.sendall(b"GET / HTTP/1.1\r\nHost: " + target_host.encode() + b"\r\n\r\n")
        elif target_port == 21: # FTP
            # A simple FTP request might get a banner
            sock.sendall(b"HELP\r\n")
        elif target_port == 25 or target_port == 587: # SMTP
            # SMTP requires HELO/EHLO
            sock.sendall(b"EHLO test.com\r\n")
        elif target_port == 23: # Telnet
            # Just connect and wait
            pass # No initial send for telnet usually

        # Receive data (banner)
        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip() # Read up to 1024 bytes

        if banner:
            print(f"[+] Banner received from {target_host}:{target_port}:")
            for line in banner.splitlines():
                print(f"    {line}")
        else:
            print(f"[-] No banner received from {target_host}:{target_port}.")

        sock.close()

    except socket.timeout:
        print(f"[!] Timeout: Could not connect or receive data from {target_host}:{target_port}.")
    except ConnectionRefusedError:
        print(f"[!] Connection Refused: Port {target_port} is likely closed or filtered on {target_host}.")
    except socket.gaierror:
        print(f"[!] Hostname Resolution Error: Could not resolve '{target_host}'.")
    except socket.error as e:
        print(f"[!] Socket Error: An error occurred while connecting to {target_host}:{target_port} - {e}")
    except Exception as e:
        print(f"[!] An unexpected error occurred: {e}")

if __name__ == "__main__":
    print("--- Tech Fortress Banner Grabbing Module ---")
    print("This tool attempts to retrieve service banners from specified ports.")

    parser = argparse.ArgumentParser(description="Banner Grabbing Tool.")
    parser.add_argument("-t", "--target", help="Target IP address or hostname (e.g., example.com or 192.168.1.1)", required=True)
    parser.add_argument("-p", "--port", type=int, help="Target port number (e.g., 80, 22, 21)", required=True)
    parser.add_argument("--timeout", type=int, default=5, help="Connection and reception timeout in seconds (default: 5)")

    args = parser.parse_args()

    if not (0 < args.port <= 65535):
        print("[!] Invalid port number. Port must be between 1 and 65535.")
        sys.exit(1)

    grab_banner(args.target, args.port, args.timeout)
    print("\n" + "="*50 + "\n")
