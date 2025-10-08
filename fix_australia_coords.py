#!/usr/bin/env python3
"""
Fix 3 Australia facilities with incorrect coordinates

These facilities have coordinates for UK/Europe locations instead of Australia:
1. Cromer - Has UK Cromer coords instead of Cromer, NSW, Australia
2. Edinburgh Parks - Has UK Edinburgh coords instead of Edinburgh Parks, SA, Australia
3. Sydney Data Station 1 - Has wrong coords instead of Sydney, NSW, Australia
"""

import json

# Correct coordinates for the 3 bad Australia facilities
AUSTRALIA_FIXES = {
    'Cromer': {
        'old': [-41.9028, 12.4964],
        'new': [-33.7360, 151.2800],  # Cromer, NSW, Australia
        'city': 'Cromer'
    },
    'Edinburgh Parks': {
        'old': [-55.9533, -3.1883],
        'new': [-34.7090, 138.6899],  # Edinburgh Parks, SA, Australia
        'city': 'Edinburgh'
    },
    'Sydney Data Station 1': {
        'old': [-53.4084, -2.9916],
        'new': [-33.8688, 151.2093],  # Sydney, NSW, Australia
        'city': 'Sydney'
    }
}

def fix_australia_coordinates(input_file, output_file):
    """Fix Australia coordinates in data file"""

    print(f"Processing {input_file}...")

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    fixed_count = 0

    for dc in data:
        if dc.get('country') == 'Australia' and dc.get('name') in AUSTRALIA_FIXES:
            fix = AUSTRALIA_FIXES[dc['name']]

            # Verify it has the old bad coordinates
            if dc.get('city_coords') == fix['old']:
                dc['city_coords'] = fix['new']
                fixed_count += 1

                print(f"  Fixed: {dc['name']} ({fix['city']})")
                print(f"    Old (plotting in ocean): {fix['old']}")
                print(f"    New (correct Australia): {fix['new']}")

    # Save fixed data
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n[SUCCESS] Fixed {fixed_count} Australia coordinates in {output_file}")

    return fixed_count

def verify_fix(file_path):
    """Verify Australia fixes"""

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"\nVerifying {file_path}...")

    # Check Australia bounds (lat: -10 to -44, lon: 113 to 154)
    australia = [dc for dc in data if dc.get('country') == 'Australia' and dc.get('city_coords')]

    outside_bounds = []
    for dc in australia:
        lat, lon = dc['city_coords']
        if lat > -10 or lat < -44 or lon < 113 or lon > 154:
            outside_bounds.append(f"{dc['name']} ({dc.get('city')}): [{lat}, {lon}]")

    if len(outside_bounds) == 0:
        print(f"  [OK] All {len(australia)} Australia facilities are within correct bounds!")
        return True
    else:
        print(f"  [ERROR] {len(outside_bounds)} facilities still outside Australia:")
        for item in outside_bounds:
            print(f"    {item}")
        return False

if __name__ == '__main__':
    print("="*70)
    print("AUSTRALIA COORDINATE FIX")
    print("="*70)
    print("\nIssue: 3 facilities have UK/Europe coordinates instead of Australia")
    print("Result: Plotting in Indian Ocean/Antarctica\n")

    # Fix both data files
    fixed_original = fix_australia_coordinates('datacenters.json', 'datacenters.json')
    fixed_cleaned = fix_australia_coordinates('datacenters_cleaned.json', 'datacenters_cleaned.json')

    print(f"\n" + "="*70)
    print(f"TOTAL FIXED: {fixed_original + fixed_cleaned} coordinates")
    print("="*70)

    # Verify fixes
    verify_original = verify_fix('datacenters.json')
    verify_cleaned = verify_fix('datacenters_cleaned.json')

    if verify_original and verify_cleaned:
        print(f"\n[SUCCESS] All Australia coordinates verified!")
    else:
        print(f"\n[ERROR] Verification failed!")
