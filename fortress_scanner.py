import socket
import sys
import threading
import time
import argparse # Needed if we want to run this standalone with args

# Global list to store open ports
open_ports = []

# Function to check if a single port is open
def check_port(target, port, timeout):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))
        if result == 0:
            try:
                service = socket.getservbyport(port)
                print(f"[+] Port {port} ({service}) is OPEN")
            except OSError:
                print(f"[+] Port {port} is OPEN (unknown service)")
            open_ports.append(port)
        sock.close()
    except socket.gaierror:
        # This is handled at a higher level (scan_ports function)
        pass
    except socket.error as e:
        # Handle other socket errors for individual port checks
        # print(f"[-] Port {port} error: {e}") # Too verbose, uncomment for debugging
        pass
    except Exception as e:
        print(f"[!] An unexpected error occurred checking port {port}: {e}")

# Main function to scan ports
def scan_ports(target, port_range_list, timeout=1, max_threads=50):
    """
    Scans a list of ports on a target.
    target: IP address or hostname
    port_range_list: an iterable of ports (e.g., a list or a range)
    timeout: socket timeout in seconds
    max_threads: maximum number of concurrent threads
    """
    global open_ports # Clear previous scan results
    open_ports = []

    print(f"\n[*] Starting port scan for {target}...")
    print(f"[*] Scanning ports: {min(port_range_list)} - {max(port_range_list) if port_range_list else 'N/A'}")

    try:
        # Resolve hostname to IP address once
        target_ip = socket.gethostbyname(target)
        print(f"[*] Resolved {target} to {target_ip}")
    except socket.gaierror:
        print(f"[!] Error: Could not resolve hostname '{target}'.")
        return # Exit the function if target is unreachable

    threads = []
    for port in port_range_list:
        thread = threading.Thread(target=check_port, args=(target_ip, port, timeout))
        threads.append(thread)
        thread.start()

        # Limit active threads to avoid overwhelming the system or target
        while threading.active_count() >= max_threads:
            time.sleep(0.1) # Short delay to let threads finish

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    if open_ports:
        print(f"\n[*] Scan completed. Found {len(open_ports)} open ports on {target_ip}:")
        print(sorted(open_ports))
    else:
        print(f"\n[*] Scan completed. No open ports found on {target_ip} in the specified range.")


if __name__ == "__main__":
    print("--- Tech Fortress Enhanced Port Scanner Module ---")
    print("This tool performs a multithreaded port scan on a target IP/hostname.")

    parser = argparse.ArgumentParser(description="Multithreaded Port Scanner.")
    parser.add_argument("-t", "--target", help="Target IP address or hostname (e.g., example.com)", required=True)
    parser.add_argument("-p", "--ports", help="Port range (e.g., 1-1024) or specific ports (e.g., 22,80,443)", required=True)
    parser.add_argument("--timeout", type=float, default=1.0, help="Socket timeout in seconds (default: 1.0)")
    parser.add_argument("--threads", type=int, default=50, help="Maximum number of concurrent threads (default: 50)")

    args = parser.parse_args()

    # Parse ports argument
    ports_to_scan = []
    if '-' in args.ports:
        try:
            start_port, end_port = map(int, args.ports.split('-'))
            ports_to_scan = list(range(start_port, end_port + 1))
        except ValueError:
            print("[!] Invalid port range format. Use 'START-END' (e.g., 1-1024).")
            sys.exit(1)
    else:
        try:
            ports_to_scan = [int(p) for p in args.ports.split(',')]
        except ValueError:
            print("[!] Invalid port list format. Use 'PORT1,PORT2' (e.g., 22,80,443).")
            sys.exit(1)

    if not ports_to_scan:
        print("[!] No valid ports to scan. Exiting.")
        sys.exit(1)

    # Remove duplicate ports and sort them
    ports_to_scan = sorted(list(set(ports_to_scan)))

    # Validate port numbers
    ports_to_scan = [p for p in ports_to_scan if 0 < p <= 65535]
    if not ports_to_scan:
        print("[!] No valid ports remaining after validation (ports must be 1-65535). Exiting.")
        sys.exit(1)

    scan_ports(args.target, ports_to_scan, args.timeout, args.threads)
    print("\n" + "="*50 + "\n") # Separator for multiple scans
