#!/usr/bin/env python3
"""
Batch Geocoding Script for ATLAS Data Center Project

Uses OpenStreetMap Nominatim (free) to geocode facilities without coordinates.
Processes ~3,973 facilities at 1 request/second (~1.1 hours total).

Features:
- Free geocoding via Nominatim
- Rate limiting (1 req/sec compliance)
- Progress tracking
- Error handling and retry logic
- Incremental saves (resume if interrupted)
- Coordinate validation
"""

import json
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from datetime import datetime

# Configuration
INPUT_FILE = 'datacenters_cleaned.json'
OUTPUT_FILE = 'datacenters_cleaned.json'
BACKUP_FILE = f'datacenters_cleaned_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
RATE_LIMIT_DELAY = 1.1  # Seconds between requests (slightly over 1 sec for safety)

# Initialize geocoder
geolocator = Nominatim(user_agent="atlas_datacenter_project_v2")

def geocode_address(address, max_retries=3):
    """Geocode an address with retry logic"""
    for attempt in range(max_retries):
        try:
            location = geolocator.geocode(address, timeout=10)
            if location:
                return [location.latitude, location.longitude]
            return None
        except GeocoderTimedOut:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            return None
        except GeocoderServiceError:
            if attempt < max_retries - 1:
                time.sleep(5)
                continue
            return None
        except Exception as e:
            print(f"    Error: {e}")
            return None
    return None

def validate_coords(coords, country):
    """Basic validation - coords should be within reasonable ranges"""
    if not coords or len(coords) != 2:
        return False

    lat, lon = coords

    # Basic range check
    if lat < -90 or lat > 90 or lon < -180 or lon > 180:
        return False

    # Country-specific bounds (basic checks)
    country_bounds = {
        'United States': {'lat': (24, 50), 'lon': (-125, -66)},
        'Brazil': {'lat': (-35, 5), 'lon': (-75, -30)},
        'Australia': {'lat': (-44, -10), 'lon': (113, 154)},
        'United Kingdom': {'lat': (49, 61), 'lon': (-8, 2)},
        'Germany': {'lat': (47, 55), 'lon': (5, 16)},
        'France': {'lat': (41, 51), 'lon': (-5, 10)},
        'Canada': {'lat': (41, 84), 'lon': (-141, -52)},
        'India': {'lat': (6, 36), 'lon': (68, 98)},
        'South Africa': {'lat': (-35, -22), 'lon': (16, 33)},
        'Singapore': {'lat': (1, 2), 'lon': (103, 104)},
    }

    if country in country_bounds:
        bounds = country_bounds[country]
        if lat < bounds['lat'][0] or lat > bounds['lat'][1]:
            return False
        if lon < bounds['lon'][0] or lon > bounds['lon'][1]:
            return False

    return True

def batch_geocode():
    """Main geocoding function"""

    print("="*70)
    print("ATLAS BATCH GEOCODING")
    print("="*70)
    print(f"\nUsing: OpenStreetMap Nominatim (free)")
    print(f"Rate: 1 request per {RATE_LIMIT_DELAY} seconds")
    print(f"Input: {INPUT_FILE}")
    print(f"Output: {OUTPUT_FILE}")

    # Load data
    print(f"\nLoading data...")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Create backup
    print(f"Creating backup: {BACKUP_FILE}")
    with open(BACKUP_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Find facilities without coordinates
    facilities_to_geocode = []
    for i, dc in enumerate(data):
        if not dc.get('city_coords'):
            facilities_to_geocode.append(i)

    total_to_geocode = len(facilities_to_geocode)
    print(f"\nFacilities without coordinates: {total_to_geocode}")

    if total_to_geocode == 0:
        print("\n[INFO] All facilities already have coordinates!")
        return

    estimated_time = (total_to_geocode * RATE_LIMIT_DELAY) / 60
    print(f"Estimated time: {estimated_time:.1f} minutes ({estimated_time/60:.1f} hours)")
    print(f"\nStarting geocoding...\n")

    # Statistics
    successful = 0
    failed = 0
    invalid = 0
    start_time = time.time()

    # Geocode each facility
    for count, idx in enumerate(facilities_to_geocode, 1):
        dc = data[idx]

        # Build address string
        address_parts = []
        if dc.get('address'):
            address_parts.append(dc['address'])
        elif dc.get('city'):
            address_parts.append(dc['city'])
            if dc.get('state'):
                address_parts.append(dc['state'])
            if dc.get('country'):
                address_parts.append(dc['country'])

        address = ', '.join(address_parts)

        # Safe printing with Unicode handling
        facility_name = dc.get('name', 'Unknown')[:50].encode('ascii', 'replace').decode('ascii')
        address_safe = address[:70].encode('ascii', 'replace').decode('ascii')

        print(f"[{count}/{total_to_geocode}] {facility_name}")
        print(f"  Address: {address_safe}")

        # Geocode
        coords = geocode_address(address)

        if coords:
            # Validate coordinates
            if validate_coords(coords, dc.get('country')):
                data[idx]['city_coords'] = coords
                successful += 1
                print(f"  [OK] Success: [{coords[0]:.4f}, {coords[1]:.4f}]")
            else:
                invalid += 1
                print(f"  [INVALID] Coords outside bounds: [{coords[0]:.4f}, {coords[1]:.4f}]")
        else:
            failed += 1
            print(f"  [FAILED] Could not geocode")

        # Save progress every 50 facilities
        if count % 50 == 0:
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            elapsed = (time.time() - start_time) / 60
            remaining = (total_to_geocode - count) * RATE_LIMIT_DELAY / 60
            print(f"\n  [PROGRESS SAVED] {count}/{total_to_geocode} | Elapsed: {elapsed:.1f}m | Remaining: ~{remaining:.1f}m\n")

        # Rate limiting
        if count < total_to_geocode:
            time.sleep(RATE_LIMIT_DELAY)

    # Final save
    print(f"\nSaving final results to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Summary
    elapsed_time = (time.time() - start_time) / 60
    print(f"\n" + "="*70)
    print("GEOCODING COMPLETE")
    print("="*70)
    print(f"\nTotal processed: {total_to_geocode}")
    print(f"  [OK] Successful: {successful} ({successful/total_to_geocode*100:.1f}%)")
    print(f"  [FAILED] Failed: {failed} ({failed/total_to_geocode*100:.1f}%)")
    print(f"  [INVALID] Invalid: {invalid} ({invalid/total_to_geocode*100:.1f}%)")
    print(f"\nTime elapsed: {elapsed_time:.1f} minutes ({elapsed_time/60:.1f} hours)")
    print(f"Backup saved: {BACKUP_FILE}")

    # Calculate new coverage
    total_facilities = len(data)
    with_coords = len([dc for dc in data if dc.get('city_coords')])
    print(f"\nCoordinate coverage: {with_coords}/{total_facilities} ({with_coords/total_facilities*100:.1f}%)")
    print(f"\n[SUCCESS] Geocoding complete!")

if __name__ == '__main__':
    try:
        batch_geocode()
    except KeyboardInterrupt:
        print("\n\n[INTERRUPTED] Geocoding stopped by user")
        print("Progress has been saved. Run script again to resume.")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
