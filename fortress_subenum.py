import socket # For DNS lookups
import sys
import argparse # New import for command-line arguments

def load_wordlist(filepath):
    """
    Loads items from a wordlist file into a list.
    """
    try:
        with open(filepath, 'r') as f:
            # Read lines, strip whitespace (like newlines), and filter out empty lines
            wordlist = [line.strip() for line in f if line.strip()]
        print(f"[*] Loaded {len(wordlist)} items from wordlist: {filepath}")
        return wordlist
    except FileNotFoundError:
        print(f"[!] Error: Wordlist file not found at '{filepath}'.")
        sys.exit(1)
    except Exception as e:
        print(f"[!] An error occurred while loading wordlist: {e}")
        sys.exit(1)

def enumerate_subdomains(domain, subdomains_list):
    """
    Attempts to resolve common subdomains for a given domain using a provided list.
    """
    print(f"\n[*] Starting subdomain enumeration for: {domain}")
    found_count = 0
    for subdomain in subdomains_list:
        full_domain = f"{subdomain}.{domain}"
        try:
            # Attempt to get IP address for the full domain
            ip_address = socket.gethostbyname(full_domain)
            print(f"[+] Found: {full_domain} -> {ip_address}")
            found_count += 1
        except socket.gaierror:
            # This means the subdomain does not resolve (i.e., doesn't exist)
            pass # Suppress 'not found' messages for cleaner output
        except Exception as e:
            print(f"[!] An unexpected error occurred with {full_domain}: {e}")
    
    if found_count == 0:
        print(f"[*] No subdomains found for {domain} from the provided list.")
    else:
        print(f"[*] Subdomain enumeration for {domain} completed. Found {found_count} subdomains.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tech Fortress Simple Subdomain Enumerator Module. This tool attempts to find common subdomains for a target domain using a wordlist.")
    parser.add_argument("-d", "--domain", help="Target domain (e.g., example.com)", required=True)
    parser.add_argument("-w", "--wordlist", help="Path to the subdomain wordlist file (e.g., /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt)", required=True)
    
    args = parser.parse_args()

    print("--- Tech Fortress Simple Subdomain Enumerator Module ---")
    
    target_domain = args.domain.strip()
    wordlist_path = args.wordlist.strip()

    # Load the wordlist
    subdomains_to_check = load_wordlist(wordlist_path)

    if not subdomains_to_check:
        print("[!] The provided wordlist is empty or could not be loaded. Exiting.")
        sys.exit(1)

    enumerate_subdomains(target_domain, subdomains_to_check)
    print("\n" + "="*50 + "\n") # Separator for scan
