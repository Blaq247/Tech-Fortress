import os # Import the 'os' module to interact with the operating system (to run commands)
import sys # Import the 'sys' module to exit the script gracefully

def check_host(target_ip):
    """
    Pings a target IP address or hostname and reports if it's online.
    """
    print(f"\n[*] Checking connectivity to: {target_ip}")
    # -c 4 means send 4 packets (for Linux/macOS ping)
    # -n 1 means send 1 packet (for Windows ping)
    # We'll use -c 4 as Kali is Linux-based.
    response = os.system(f"ping -c 4 {target_ip}")

    # os.system returns 0 if the command was successful (host is reachable)
    if response == 0:
        print(f"[+] {target_ip} is ONLINE.")
        return True
    else:
        print(f"[-] {target_ip} is OFFLINE or unreachable.")
        return False

if __name__ == "__main__":
    print("--- Tech Fortress Pinger Module ---")
    print("This tool checks if a target host is reachable on the network.")

    while True:
        target = input("Enter target IP address or hostname (e.g., 8.8.8.8 or google.com, or 'exit' to quit): ").strip()

        if target.lower() == 'exit':
            print("[*] Exiting Tech Fortress Pinger. Goodbye!")
            sys.exit(0) # Exit the script

        if not target:
            print("[!] No target entered. Please try again.")
            continue

        check_host(target)
