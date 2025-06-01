import socket  # Essential for network connections
import sys     # For exiting the script
import time    # For adding a small delay/timeout

def check_port(target_ip, port, timeout=1):
    """
    Attempts to connect to a target IP on a specified port to check if it's open.
    :param target_ip: The IP address or hostname to scan.
    :param port: The port number to check.
    :param timeout: How long to wait for a connection before timing out (in seconds).
    :return: True if the port is open, False otherwise.
    """
    try:
        # Create a new socket object
        # AF_INET specifies IPv4 addressing
        # SOCK_STREAM specifies TCP (for connection-oriented service)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout) # Set a timeout for the connection attempt

        # Attempt to connect to the target and port
        result = sock.connect_ex((target_ip, port)) # connect_ex returns 0 on success

        if result == 0:
            print(f"[+] Port {port} is OPEN on {target_ip}")
            return True
        else:
            # print(f"[-] Port {port} is CLOSED or FILTERED on {target_ip} (Error code: {result})") # For debugging
            return False

    except socket.gaierror:
        print(f"[-] Hostname '{target_ip}' could not be resolved.")
        return False
    except socket.error as e:
        print(f"[-] Could not connect to {target_ip} on port {port}: {e}")
        return False
    except Exception as e:
        print(f"[!] An unexpected error occurred: {e}")
        return False
    finally:
        sock.close() # Always close the socket

if __name__ == "__main__":
    print("--- Tech Fortress Port Scanner Module ---")
    print("This tool checks if a specific port is open on a target host.")

    while True:
        target = input("Enter target IP address or hostname (e.g., 192.168.1.1 or example.com, or 'exit' to quit): ").strip()

        if target.lower() == 'exit':
            print("[*] Exiting Tech Fortress Port Scanner. Goodbye!")
            sys.exit(0)

        if not target:
            print("[!] No target entered. Please try again.")
            continue

        port_input = input("Enter the port number to check (e.g., 80, 22, 443): ").strip()
        if not port_input.isdigit():
            print("[!] Invalid port number. Please enter a number.")
            continue
        port = int(port_input)

        if not (0 < port < 65536): # Ports range from 1 to 65535
            print("[!] Port number must be between 1 and 65535.")
            continue

        # Call the port check function
        check_port(target, port)
