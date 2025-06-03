import requests
import sys
import argparse
from urllib.parse import urlparse, urljoin

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
        return [] # Return empty list instead of sys.exit for integration
    except Exception as e:
        print(f"[!] An error occurred while loading wordlist: {e}")
        return [] # Return empty list for integration

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
        full_url = urljoin(base_url, path)
        try:
            response = requests.head(full_url, timeout=3)
            status_code = response.status_code

            if status_code == 200:
                print(f"[+] Found: {full_url} (Status: {status_code} OK)")
                found_count += 1
            elif status_code == 403:
                print(f"[!] Forbidden: {full_url} (Status: {status_code} - Access Denied)")
                found_count += 1
            elif status_code == 301 or status_code == 302:
                print(f"[>] Redirect: {full_url} (Status: {status_code} to {response.headers.get('Location', 'N/A')})")
                found_count += 1

        except requests.exceptions.Timeout:
            # print(f"[!] Timeout for {full_url}") # Suppress for cleaner output in main script
            pass
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
    print("Note: This uses external wordlists.")

    parser = argparse.ArgumentParser(description="Tech Fortress Basic File/Directory Existence Checker Module. This tool attempts to find common files and directories on a target web server using a wordlist.")
    parser.add_argument("-u", "--url", help="Target base URL (e.g., http://example.com/)", required=True)
    parser.add_argument("-w", "--wordlist", help="Path to the directory/file wordlist file (e.g., /usr/share/wordlists/seclists/Discovery/Web-Content/common.txt)", required=True)

    args = parser.parse_args()

    target_url = args.url.strip()
    wordlist_path = args.wordlist.strip()

    # Basic URL validation
    parsed_url = urlparse(target_url)
    if not parsed_url.scheme or not parsed_url.netloc:
        print("[!] Invalid URL format. Please include http:// or https:// (e.g., http://example.com/).")
        sys.exit(1)

    # Load the wordlist
    paths_to_check = load_wordlist(wordlist_path)

    if not paths_to_check:
        print("[!] The provided wordlist is empty or could not be loaded. Exiting.")
        sys.exit(1)

    check_paths(target_url, paths_to_check)
    print("\n" + "="*50 + "\n")
