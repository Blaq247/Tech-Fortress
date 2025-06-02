import requests
import sys
from urllib.parse import urlparse, urljoin # urljoin helps construct full URLs safely

# A small list of common files/directories for testing
# In a real scenario, you'd load a large wordlist from a file
COMMON_PATHS = [
    "admin/", "login.php", "robots.txt", "sitemap.xml", "backup/",
    "config.php", "index.php", "test/", "upload/", "phpmyadmin/",
    ".env", "wp-admin/", "wp-login.php", "panel/"
]

def check_paths(base_url, paths_list):
    """
    Checks for the existence of specified paths on a base URL.
    """
    print(f"\n[*] Starting directory/file existence check for: {base_url}")
    found_count = 0

    # Ensure base_url ends with a slash for consistent joining
    if not base_url.endswith('/'):
        base_url += '/'

    for path in paths_list:
        full_url = urljoin(base_url, path) # Safely joins base_url and path
        try:
            # Use HEAD request for efficiency if only status code is needed, else GET
            # HEAD requests retrieve headers only, not full content, often faster.
            response = requests.head(full_url, timeout=3)
            status_code = response.status_code

            if status_code == 200:
                print(f"[+] Found: {full_url} (Status: {status_code} OK)")
                found_count += 1
            elif status_code == 403:
                print(f"[!] Forbidden: {full_url} (Status: {status_code} - Access Denied)")
                found_count += 1 # Often indicates existence, but restricted
            elif status_code == 301 or status_code == 302:
                print(f"[>] Redirect: {full_url} (Status: {status_code} to {response.headers.get('Location', 'N/A')})")
                found_count += 1 # Indicates existence and redirection
            # Uncomment the following line for verbose output of 404s
            # elif status_code == 404:
            #     print(f"[-] Not Found: {full_url} (Status: {status_code})")

        except requests.exceptions.Timeout:
            print(f"[!] Timeout for {full_url}")
        except requests.exceptions.ConnectionError:
            print(f"[!] Connection Error for {full_url}. Is the host reachable?")
        except requests.exceptions.RequestException as e:
            print(f"[!] An unexpected error occurred with {full_url}: {e}")
        except Exception as e:
            print(f"[!] An unexpected error occurred: {e}")

    if found_count == 0:
        print(f"[*] No common files or directories found for {base_url} from the provided list.")
    else:
        print(f"[*] Existence check for {base_url} completed. Found {found_count} potential paths.")


if __name__ == "__main__":
    print("--- Tech Fortress Basic File/Directory Existence Checker Module ---")
    print("This tool attempts to find common files and directories on a target web server.")
    print("Note: This uses a small built-in list. For real use, consider external wordlists.")

    while True:
        target_url = input("Enter target base URL (e.g., http://example.com/ or 'exit' to quit): ").strip()

        if target_url.lower() == 'exit':
            print("[*] Exiting Tech Fortress Dirbuster. Goodbye!")
            sys.exit(0)

        if not target_url:
            print("[!] No URL entered. Please try again.")
            continue

        # Basic URL validation
        parsed_url = urlparse(target_url)
        if not parsed_url.scheme or not parsed_url.netloc:
            print("[!] Invalid URL format. Please include http:// or https:// (e.g., http://example.com/).")
            continue

        check_paths(target_url, COMMON_PATHS)
        print("\n" + "="*50 + "\n") # Separator for multiple scans
