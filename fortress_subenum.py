import socket # For DNS lookups
import sys

# A small list of common subdomains for testing
# In a real scenario, you'd use a much larger wordlist from a file
COMMON_SUBDOMAINS = [
    "www", "mail", "ftp", "blog", "dev", "test", "admin",
    "api", "webmail", "ns1", "ns2", "vpn", "m", "portal"
]

def enumerate_subdomains(domain, subdomains_list):
    """
    Attempts to resolve common subdomains for a given domain.
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
            # print(f"[-] Not found: {full_domain}") # Uncomment for verbose output
            pass # Suppress 'not found' messages for cleaner output
        except Exception as e:
            print(f"[!] An unexpected error occurred with {full_domain}: {e}")

    if found_count == 0:
        print(f"[*] No common subdomains found for {domain} from the provided list.")
    else:
        print(f"[*] Subdomain enumeration for {domain} completed. Found {found_count} subdomains.")


if __name__ == "__main__":
    print("--- Tech Fortress Simple Subdomain Enumerator Module ---")
    print("This tool attempts to find common subdomains for a target domain.")
    print("Note: This uses a small built-in list. For real use, consider external wordlists.")

    while True:
        target_domain = input("Enter target domain (e.g., example.com or 'exit' to quit): ").strip()

        if target_domain.lower() == 'exit':
            print("[*] Exiting Tech Fortress Subdomain Enumerator. Goodbye!")
            sys.exit(0)

        if not target_domain:
            print("[!] No domain entered. Please try again.")
            continue

        enumerate_subdomains(target_domain, COMMON_SUBDOMAINS)
        print("\n" + "="*50 + "\n") # Separator for multiple scans
