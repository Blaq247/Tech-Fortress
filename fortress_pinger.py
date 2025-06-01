import subprocess # Import the 'os' module to interact with the operating system (to run commands)
import sys # Import thimport subprocess # <--- CHANGED FROM 'os'
import sys

def check_host(target_ip):
    """
    Pings a target IP address or hostname and reports if it's online.
    """
    print(f"\n[*] Checking connectivity to: {target_ip}")

    try:
        # Use subprocess.run to execute the ping command
        # capture_output=True: captures stdout and stderr
        # text=True: decodes output as text (string)
        # timeout=10: sets a timeout for the command (optional but good practice)
        # check=True: raises CalledProcessError if the command returns a non-zero exit code
        result = subprocess.run(
            ['ping', '-c', '4', target_ip],
            capture_output=True,
            text=True,
            timeout=10,
            check=False # We handle the check ourselves to get the return code
        )

        # Print the full ping output (stdout and stderr)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)

        # Check the return code (returncode is 0 for success)
        if result.returncode == 0:
            print(f"[+] {target_ip} is ONLINE.")
            return True
        else:
            print(f"[-] {target_ip} is OFFLINE or unreachable (Return code: {result.returncode}).")
            return False

    except subprocess.TimeoutExpired:
        print(f"[-] {target_ip} is OFFLINE or unreachable (Ping timed out).")
        return False
    except FileNotFoundError:
        print("[!] Error: 'ping' command not found. Is it installed and in your PATH?")
        return False
    except Exception as e:
        print(f"[!] An unexpected error occurred: {e}")
        return False

if __name__ == "__main__":
    print("--- Tech Fortress Pinger Module ---")
    print("This tool checks if a target host is reachable on the network.")

    while True:
        target = input("Enter target IP address or hostname (e.g., 8.8.8.8 or google.com, or 'exit' to quit): ").strip()

        if target.lower() == 'exit':
            print("[*] Exiting Tech Fortress Pinger. Goodbye!")
            sys.exit(0)

        if not target:
            print("[!] No target entered. Please try again.")
            continue

        check_host(target) # call the function to check the host
import datetime # <-- NEW LINE

def check_host(target_ip):
    """
    Pings a target IP address or hostname and reports if it's online.
    """
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # <-- Add this line
    print(f"\n[*] Checking connectivity to: {target_ip} at {current_time}") # <-- Modify this line
    print(f"\n[*] Checking connectivity to: {target_ip}")
    # -c 4 means send 4 packets (for Linux/macOS ping)
    # -n 1 means send 1 packet (for Windows ping)
    # We'll use -c 4 as Kali is Linux-based.
    response = os.system(f"ping -c 4 {target_ip}")
    print(f"DEBUG: os.system returned: {response}")
    # <-- ADD OR CONFIRM THIS LINE

    # os.system returns 0 if the command was successful (host is reachable)
    if response == 0:
        print(f"[+] {target_ip} is ONLINE.(Checked at {current_time})")
        return True
    else:
        print(f"[-] {target_ip} is OFFLINE or unreachable. (Checked at {current_time})")
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


def check_host(target_ip):
    """
    Pings a target IP address or hostname and reports if it's online.
    """
    print(f"\n[*] Checking connectivity to: {target_ip}")
    response = os.system(f"ping -c 4 {target_ip}")

    if response == 0:
        print(f"[+] {target_ip} is ONLINE.")
        return True
    else:
        print(f"[-] {target_ip} is OFFLINE or unreachable.")
        return False

# --- NEW FUNCTION FOR READING TARGETS FROM FILE ---
def read_targets_from_file(filename):
    """
    Reads a list of IP addresses/hostnames from a specified file.
    Each target should be on a new line.
    """
    targets = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                target = line.strip() # Remove leading/trailing whitespace
                if target and not target.startswith('#'): # Ignore empty lines and comments
                    targets.append(target)
        print(f"[*] Successfully read {len(targets)} targets from {filename}.")
        return targets
    except FileNotFoundError:
        print(f"[-] Error: File '{filename}' not found.")
        return None
    except Exception as e:
        print(f"[-] An error occurred while reading the file: {e}")
        return None

if __name__ == "__main__":
    print("--- Tech Fortress Pinger Module ---")
    print("This tool checks if target hosts are reachable on the network.")

    while True:
        # --- NEW USER INPUT FOR CHOICE ---
        choice = input("\nDo you want to ping targets (M)anually or from a (F)ile? (M/F/exit): ").strip().lower()

        if choice == 'exit':
            print("[*] Exiting Tech Fortress Pinger. Goodbye!")
            sys.exit(0)
        elif choice == 'm':
            target = input("Enter target IP address or hostname (e.g., 8.8.8.8 or google.com): ").strip()
            if not target:
                print("[!] No target entered. Please try again.")
                continue
            check_host(target)
        elif choice == 'f':
            filename = input("Enter the filename containing targets (e.g., targets.txt): ").strip()
            if not filename:
                print("[!] No filename entered. Please try again.")
                continue

            targets_list = read_targets_from_file(filename)
            if targets_list: # Only proceed if targets were successfully read
                for target_from_file in targets_list:
                    check_host(target_from_file)
            else:
                print("[!] No targets to ping or file could not be read. Please try again.")
        else:
            print("[!] Invalid choice. Please enter 'M', 'F', or 'exit'.")
