import json
import time
import requests
from urllib.parse import quote

def geocode_address(address):
    """Geocode an address using Nominatim (OpenStreetMap)"""
    try:
        # Nominatim requires a user agent
        headers = {
            'User-Agent': 'DataCenterMapper/1.0'
        }

        url = f"https://nominatim.openstreetmap.org/search?q={quote(address)}&format=json&limit=1"

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                return {
                    'lat': float(data[0]['lat']),
                    'lon': float(data[0]['lon'])
                }
        return None
    except Exception as e:
        print(f"Error geocoding {address}: {e}")
        return None

# Load existing data
with open('datacenters.json', 'r', encoding='utf-8') as f:
    datacenters = json.load(f)

print(f"Geocoding {len(datacenters)} datacenters...")
print("This will take a while due to rate limiting (1 request per second)")

geocoded_count = 0
failed_count = 0

for i, dc in enumerate(datacenters):
    # Skip if already has coordinates
    if 'lat' in dc and 'lon' in dc and dc['lat'] is not None:
        geocoded_count += 1
        continue

    # Build address string
    address_parts = []
    if dc.get('street'):
        address_parts.append(dc['street'])
    if dc.get('city'):
        address_parts.append(dc['city'])
    if dc.get('state'):
        address_parts.append(dc['state'])
    if dc.get('country'):
        address_parts.append(dc['country'])

    address_str = ', '.join(address_parts)

    if not address_str:
        address_str = dc.get('address', '')

    if address_str:
        print(f"[{i+1}/{len(datacenters)}] Geocoding: {dc['name'][:50]}...")

        coords = geocode_address(address_str)

        if coords:
            dc['lat'] = coords['lat']
            dc['lon'] = coords['lon']
            geocoded_count += 1
            print(f"  [OK] Found: {coords['lat']}, {coords['lon']}")
        else:
            dc['lat'] = None
            dc['lon'] = None
            failed_count += 1
            print(f"  [FAIL] Not found")

        # Rate limiting: 1 request per second for Nominatim
        time.sleep(1)

        # Save progress every 100 entries
        if (i + 1) % 100 == 0:
            print(f"Saving progress... ({geocoded_count} geocoded, {failed_count} failed)")
            with open('datacenters.json', 'w', encoding='utf-8') as f:
                json.dump(datacenters, f, indent=2, ensure_ascii=False)
    else:
        dc['lat'] = None
        dc['lon'] = None
        failed_count += 1

# Final save
print("Saving final results...")
with open('datacenters.json', 'w', encoding='utf-8') as f:
    json.dump(datacenters, f, indent=2, ensure_ascii=False)

print(f"\nGeocoding complete!")
print(f"Successfully geocoded: {geocoded_count}")
print(f"Failed: {failed_count}")
print(f"Total: {len(datacenters)}")
