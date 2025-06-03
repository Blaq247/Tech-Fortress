import sys
import os

# Ensure the current directory is in the Python path to import modules
# This is useful if you run fortress.py from elsewhere, though you typically run it from its dir
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import functions from your individual modules
# We'll import only the main function from each for cleaner execution
try:
    from fortress_pinger import ping_host
    from fortress_scanner import scan_ports
    from fortress_webinfo import get_web_info
    from fortress_subenum import enumerate_subdomains, load_wordlist as load_subdomain_wordlist # Rename to avoid conflict
    from fortress_dirbuster import check_paths, load_wordlist as load_path_wordlist # Rename to avoid conflict
    from fortress_geolocate import geolocate_ip
    from fortress_bannergrab import grab_banner # NEW IMPORT
except ImportError as e:
    print(f"[!] Error importing a module: {e}")
    print("[!] Please ensure all 'fortress_*.py' files are in the same directory.")
    sys.exit(1)
except Exception as e:
    print(f"[!] An unexpected error occurred during module import: {e}")
    sys.exit(1)

def display_menu():
    """Displays the main menu options."""
    print("\n" + "="*50)
    print("          Tech Fortress Reconnaissance Toolkit")
    print("="*50)
    print("1. Host Discovery (Ping)")
    print("2. Port Scanning")
    print("3. Basic Web Info Gathering")
    print("4. Simple Subdomain Enumeration (with wordlist)")
    print("5. Basic Directory/File Existence Check (with wordlist)")
    print("6. Banner Grabbing") # NEW OPTION
    print("7. IP Geolocation Lookup") # CORRECTED TYPO AND NUMBER
    print("0. Exit")
    print("="*50)

def main():
    """Main function to run the Tech Fortress toolkit."""
    while True:
        display_menu()
        choice = input("Enter your choice (0-7): ").strip() # UPDATED RANGE

        if choice == '1':
            print("\n--- Host Discovery (Ping) ---")
            target = input("Enter target IP or hostname: ").strip()
            if target:
                ping_host(target)
            else:
                print("[!] No target entered.")

        elif choice == '2':
            print("\n--- Port Scanning ---")
            target = input("Enter target IP or hostname: ").strip()
            if target:
                print("Scanning common ports (20-1024)...")
                scan_ports(target, range(20, 1025))
            else:
                print("[!] No target entered.")

        elif choice == '3':
            print("\n--- Basic Web Info Gathering ---")
            target_url = input("Enter target URL (e.g., http://example.com/): ").strip()
            if target_url:
                get_web_info(target_url)
            else:
                print("[!] No URL entered.")

        elif choice == '4':
            print("\n--- Simple Subdomain Enumeration ---")
            target_domain = input("Enter target domain (e.g., example.com): ").strip()
            if not target_domain:
                print("[!] No domain entered.")
                continue

            default_sub_wordlist = "/usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt"
            if not os.path.exists(default_sub_wordlist):
                print(f"[!] Warning: Default subdomain wordlist not found at '{default_sub_wordlist}'.")
                print("    Please ensure 'seclists' is installed or manually provide a path.")
                wordlist_path = input("Enter path to subdomain wordlist (or press Enter for default if installed): ").strip()
                if not wordlist_path: wordlist_path = default_sub_wordlist
            else:
                wordlist_path = default_sub_wordlist

            if os.path.exists(wordlist_path):
                subdomains_to_check = load_subdomain_wordlist(wordlist_path)
                if subdomains_to_check:
                    enumerate_subdomains(target_domain, subdomains_to_check)
                else:
                    print("[!] Wordlist could not be loaded or is empty.")
            else:
                print(f"[!] Subdomain wordlist not found at '{wordlist_path}'.")

        elif choice == '5':
            print("\n--- Basic Directory/File Existence Check ---")
            target_url = input("Enter target base URL (e.g., http://example.com/): ").strip()
            if not target_url:
                print("[!] No URL entered.")
                continue # CORRECTED: Added continue here for empty URL

            # Moved this entire block INSIDE choice '5'
            default_dir_wordlist = "/usr/share/wordlists/seclists/Discovery/Web-Content/common.txt"
            if not os.path.exists(default_dir_wordlist):
                print(f"[!] Warning: Default directory/file wordlist not found at '{default_dir_wordlist}'.")
                print("    Please ensure 'seclists' is installed or manually provide a path.")
                wordlist_path = input("Enter path to dir/file wordlist (or press Enter for default if installed): ").strip()
                if not wordlist_path: wordlist_path = default_dir_wordlist
            else:
                wordlist_path = default_dir_wordlist

            if os.path.exists(wordlist_path):
                paths_to_check = load_path_wordlist(wordlist_path)
                if paths_to_check:
                    check_paths(target_url, paths_to_check)
                else:
                    print("[!] Wordlist could not be loaded or is empty.")
            else:
                print(f"[!] Directory/file wordlist not found at '{wordlist_path}'.")


        elif choice == '6':
            print("\n--- Banner Grabbing ---")
            target = input("Enter target IP or hostname (e.g., example.com): ").strip()
            if not target:
                print("[!] No target entered.")
                continue
            try:
                port = int(input("Enter target port number (e.g., 80, 22): ").strip())
                if not (0 < port <= 65535):
                    print("[!] Invalid port number. Port must be between 1 and 65535.")
                    continue
            except ValueError:
                print("[!] Invalid port number. Please enter an integer.")
                continue # CORRECTED: Indentation for this continue
            grab_banner(target, port) # This will now be reached

        elif choice == '7':
            print("\n--- IP Geolocation Lookup ---")
            target_ip = input("Enter target IP address (e.g., 8.8.8.8): ").strip()
            if target_ip:
                geolocate_ip(target_ip)
            else:
                print("[!] No IP address entered.")

        elif choice == '0':
            print("\nExiting Tech Fortress. Stay safe and ethical, comrade!")
            sys.exit(0)

        else:
            print("[!] Invalid choice. Please enter a number between 0 and 7.") # UPDATED RANGE

if __name__ == "__main__":
    main()
