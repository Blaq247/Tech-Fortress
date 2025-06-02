import requests
import sys
import ipaddress # To validate IP addresses

def geolocate_ip(ip_address):
    """
    Fetches geolocation information for a given IP address using ip-api.com.
    """
    api_url = f"http://ip-api.com/json/{ip_address}"
    print(f"\n[*] Querying geolocation for: {ip_address}")

    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

        data = response.json() # Parse JSON response

        if data and data.get("status") == "success":
            print("\n--- Geolocation Details ---")
            print(f"    IP Address: {data.get('query')}")
            print(f"    Country:    {data.get('country')} ({data.get('countryCode')})")
            print(f"    Region:     {data.get('regionName')} ({data.get('region')})")
            print(f"    City:       {data.get('city')}")
            print(f"    ZIP Code:   {data.get('zip')}")
            print(f"    Latitude:   {data.get('lat')}")
            print(f"    Longitude:  {data.get('lon')}")
            print(f"    Timezone:   {data.get('timezone')}")
            print(f"    ISP:        {data.get('isp')}")
            print(f"    Org:        {data.get('org')}")
            print(f"    AS:         {data.get('as')}")
        elif data and data.get("status") == "fail":
            print(f"[!] Geolocation failed for {ip_address}: {data.get('message', 'Unknown error.')}")
        else:
            print(f"[!] Unexpected response from API for {ip_address}: {response.text}")

    except requests.exceptions.Timeout:
        print(f"[!] Request timed out for {ip_address}. The API took too long to respond.")
    except requests.exceptions.ConnectionError:
        print(f"[!] Failed to connect to the geolocation API. Check your internet connection.")
    except requests.exceptions.HTTPError as err:
        print(f"[!] HTTP Error during API request for {ip_address}: {err} (Status Code: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"[!] An unexpected error occurred during the API request for {ip_address}: {e}")
    except ValueError: # Catches JSON decoding errors
        print(f"[!] Failed to decode JSON response from API for {ip_address}.")
    except Exception as e:
        print(f"[!] An unexpected error occurred: {e}")

if __name__ == "__main__":
    print("--- Tech Fortress IP Geolocation Module ---")
    print("This tool fetches approximate geographical information for an IP address.")
    print("Data provided by ip-api.com")

    while True:
        target_ip = input("Enter target IP address (e.g., 8.8.8.8 or 'exit' to quit): ").strip()

        if target_ip.lower() == 'exit':
            print("[*] Exiting Tech Fortress Geolocation. Goodbye!")
            sys.exit(0)

        if not target_ip:
            print("[!] No IP address entered. Please try again.")
            continue

        # Basic IP address validation
        try:
            ipaddress.ip_address(target_ip) # Checks if it's a valid IPv4 or IPv6 address
        except ValueError:
            print(f"[!] '{target_ip}' is not a valid IP address. Please enter a valid IPv4 or IPv6 address.")
            continue

        geolocate_ip(target_ip)
        print("\n" + "="*50 + "\n") # Separator for multiple lookups
