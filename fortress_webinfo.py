import requests # New library for making HTTP requests
import sys
from urllib.parse import urlparse # To help with URL validation

def get_web_info(url):
    """
    Connects to a URL, fetches HTTP headers, and the page title.
    """
    print(f"\n[*] Gathering web information for: {url}")
    try:
        # Add a timeout to prevent hanging
        response = requests.get(url, timeout=5)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

        print("\n--- HTTP Headers ---")
        for header, value in response.headers.items():
            print(f"    {header}: {value}")

        # Get the page title
        title = "Not Found"
        if "<title>" in response.text and "</title>" in response.text:
            start = response.text.find("<title>") + len("<title>")
            end = response.text.find("</title>")
            title = response.text[start:end].strip()
        print(f"\n--- Page Title ---")
        print(f"    Title: {title}")

    except requests.exceptions.Timeout:
        print(f"[!] Request timed out for {url}. The server took too long to respond.")
    except requests.exceptions.ConnectionError:
        print(f"[!] Failed to connect to {url}. Check if the URL is correct or if the host is reachable.")
    except requests.exceptions.HTTPError as err:
        print(f"[!] HTTP Error for {url}: {err} (Status Code: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"[!] An unexpected error occurred during the request for {url}: {e}")
    except Exception as e:
        print(f"[!] An unexpected error occurred: {e}")

if __name__ == "__main__":
    print("--- Tech Fortress Web Info Gatherer Module ---")
    print("This tool fetches HTTP headers and page titles from a given URL.")

    while True:
        target_url = input("Enter target URL (e.g., http://example.com or 'exit' to quit): ").strip()

        if target_url.lower() == 'exit':
            print("[*] Exiting Tech Fortress Web Info Gatherer. Goodbye!")
            sys.exit(0)

        if not target_url:
            print("[!] No URL entered. Please try again.")
            continue

        # Basic URL validation
        parsed_url = urlparse(target_url)
        if not parsed_url.scheme or not parsed_url.netloc:
            print("[!] Invalid URL format. Please include http:// or https:// (e.g., http://example.com).")
            continue

        get_web_info(target_url)
        print("\n" + "="*50 + "\n") # Separator for multiple scans
