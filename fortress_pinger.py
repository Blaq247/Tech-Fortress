import os
import sys
import subprocess # More robust than os.system for capturing output

def ping_host(target):
    """
    Performs an ICMP ping to the target host.
    """
    print(f"[*] Pinging {target}...")
    try:
        # Use subprocess.run for better control and error handling
        # -c 1: send 1 packet
        # -W 1: wait 1 second for response
        # -n: numeric output only (don't resolve hostnames)
        process = subprocess.run(
            ['ping', '-c', '1', '-W', '1', target],
            capture_output=True,
            text=True,
            check=True # Raise an exception for non-zero exit codes (e.g., host unreachable)
        )
        # If ping is successful, it will not raise CalledProcessError
        print(f"[+] {target} is UP!")
        # print(process.stdout) # Uncomment to see full ping output
    except subprocess.CalledProcessError as e:
        # Host is down or unreachable
        print(f"[-] {target} is DOWN or unreachable.")
        # print(e.stdout) # Uncomment to see ping error output
        # print(e.stderr) # Uncomment to see ping error output
    except FileNotFoundError:
        print("[!] Error: 'ping' command not found. Please ensure ping is installed and in your PATH.")
    except Exception as e:
        print(f"[!] An unexpected error occurred while pinging {target}: {e}")

if __name__ == "__main__":
    print("--- Tech Fortress Host Discovery Module ---")
    print("This tool performs a basic ICMP ping to check host reachability.")

    while True:
        target_host = input("Enter target IP address or hostname (e.g., 192.168.1.1 or example.com, or 'exit' to quit): ").strip()

        if target_host.lower() == 'exit':
            print("[*] Exiting Tech Fortress Host Discovery. Goodbye!")
            sys.exit(0)

        if not target_host:
            print("[!] No target entered. Please try again.")
            continue

        ping_host(target_host)
        print("\n" + "="*50 + "\n") # Separator for multiple pings
