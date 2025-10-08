#!/usr/bin/env python3
"""
Fix facilities with incorrect city coordinates

Issues found:
1. São José facilities (Brazil) - Wrong coords [-46.948, 7.4474] plotting in ocean
   Correct: [-27.6167, -48.6333] (São José, Santa Catarina, Brazil)

2. East London (South Africa) - Has London UK coords [-51.5074, -0.1278]
   Correct: [-33.0153, 27.9116] (East London, South Africa)
"""

import json

# Coordinate fixes - map old wrong coords to correct new coords
COORD_FIXES = {
    # São José, SC, Brazil facilities (multiple have same wrong coords)
    '[-46.948, 7.4474]': {
        'new': [-27.6167, -48.6333],
        'location': 'São José, Santa Catarina, Brazil',
        'country': 'Brazil'
    },
    # East London, South Africa (has London UK coords)
    '[-51.5074, -0.1278]': {
        'new': [-33.0153, 27.9116],
        'location': 'East London, South Africa',
        'country': 'South Africa'
    },
    # São Carlos, Brazil (plotting in Pacific Ocean)
    '[-38.9072, -77.0369]': {
        'new': [-22.0087, -47.8906],
        'location': 'São Carlos, São Paulo, Brazil',
        'country': 'Brazil'
    },
    # Johannesburg/Centurion, South Africa (plotting in Pacific Ocean)
    '[-39.0062, -77.4286]': {
        'new': [-25.8601, 28.1871],
        'location': 'Centurion, South Africa',
        'country': 'South Africa'
    }
}

def coord_key(coords):
    """Create string key from coordinate list"""
    if coords:
        return str(coords)
    return None

def fix_coordinates(input_file, output_file):
    """Fix incorrect city coordinates"""

    print(f"Processing {input_file}...")

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    fixed_count = 0
    fixes_by_location = {}

    for dc in data:
        coords = dc.get('city_coords')
        if coords:
            key = coord_key(coords)

            if key in COORD_FIXES:
                fix = COORD_FIXES[key]

                # Only fix if country matches (safety check)
                if dc.get('country') == fix['country']:
                    dc['city_coords'] = fix['new']
                    fixed_count += 1

                    location = fix['location']
                    if location not in fixes_by_location:
                        fixes_by_location[location] = []
                    fixes_by_location[location].append(dc.get('name'))

    # Save fixed data
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n[SUCCESS] Fixed {fixed_count} coordinates in {output_file}")

    # Show what was fixed
    for location, facilities in fixes_by_location.items():
        print(f"\n  {location}: {len(facilities)} facilities")
        for name in facilities[:3]:  # Show first 3
            print(f"    - {name}")
        if len(facilities) > 3:
            print(f"    ... and {len(facilities) - 3} more")

    return fixed_count

def verify_fix(file_path):
    """Verify the bad coordinates are gone"""

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"\nVerifying {file_path}...")

    bad_coords_found = []
    for dc in data:
        coords = dc.get('city_coords')
        if coords:
            key = coord_key(coords)
            if key in COORD_FIXES:
                bad_coords_found.append(f"{dc.get('name')} ({dc.get('country')}): {coords}")

    if len(bad_coords_found) == 0:
        print(f"  [OK] No bad coordinates found!")
        return True
    else:
        print(f"  [ERROR] Still found {len(bad_coords_found)} bad coordinates:")
        for item in bad_coords_found:
            print(f"    {item}")
        return False

if __name__ == '__main__':
    print("="*70)
    print("BAD CITY COORDINATE FIX")
    print("="*70)
    print("\nIssues to fix:")
    print("- São José, Brazil: Wrong coords plotting in ocean")
    print("- East London, SA: Has London UK coordinates instead")
    print()

    # Fix both data files
    fixed_original = fix_coordinates('datacenters.json', 'datacenters.json')
    fixed_cleaned = fix_coordinates('datacenters_cleaned.json', 'datacenters_cleaned.json')

    print(f"\n" + "="*70)
    print(f"TOTAL FIXED: {fixed_original + fixed_cleaned} coordinates")
    print("="*70)

    # Verify fixes
    verify_original = verify_fix('datacenters.json')
    verify_cleaned = verify_fix('datacenters_cleaned.json')

    if verify_original and verify_cleaned:
        print(f"\n[SUCCESS] All bad coordinates fixed!")
    else:
        print(f"\n[ERROR] Verification failed!")
