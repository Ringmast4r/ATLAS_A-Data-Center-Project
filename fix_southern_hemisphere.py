#!/usr/bin/env python3
"""
Fix Southern Hemisphere Latitude Sign Error

Issue: Facilities in Southern Hemisphere countries have POSITIVE latitudes
when they should be NEGATIVE. This causes them to plot in the ocean/Africa
instead of their actual locations.

Affected: 261 entries across Australia, Singapore, Brazil, South Africa, New Zealand
"""

import json

# Southern Hemisphere countries (latitude should be negative)
SOUTHERN_HEMISPHERE_COUNTRIES = [
    # South America
    'Brazil', 'Argentina', 'Chile', 'Uruguay', 'Paraguay', 'Peru', 'Bolivia',
    'Ecuador', 'Colombia', 'Venezuela', 'Guyana', 'Suriname',

    # Oceania
    'Australia', 'New Zealand', 'Fiji', 'Papua New Guinea', 'Samoa', 'Tonga',

    # Africa (Southern portion)
    'South Africa', 'Namibia', 'Botswana', 'Zimbabwe', 'Mozambique',
    'Madagascar', 'Zambia', 'Angola', 'Malawi', 'Lesotho', 'Swaziland',

    # Southeast Asia (partially southern - equator region)
    'Indonesia', 'Singapore', 'East Timor'
]

def fix_coordinates(input_file, output_file):
    """Fix latitude signs for Southern Hemisphere countries"""

    print(f"Processing {input_file}...")

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    fixed_count = 0

    for dc in data:
        country = dc.get('country')

        # Check if this is a Southern Hemisphere country with coordinates
        if country in SOUTHERN_HEMISPHERE_COUNTRIES and dc.get('city_coords'):
            lat, lon = dc['city_coords']

            # If latitude is positive (Northern Hemisphere) but should be negative
            if lat > 0:
                # Flip the sign
                dc['city_coords'] = [-lat, lon]
                fixed_count += 1

                if fixed_count <= 5:  # Show first 5 fixes
                    print(f"  Fixed: {dc.get('name')} ({country})")
                    print(f"    [{lat}, {lon}] -> [{-lat}, {lon}]")

    # Save fixed data
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n[SUCCESS] Fixed {fixed_count} coordinates in {output_file}")

    return fixed_count

def verify_fix(file_path):
    """Verify that all Southern Hemisphere countries have negative latitudes"""

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"\nVerifying {file_path}...")

    still_wrong = 0
    for country in SOUTHERN_HEMISPHERE_COUNTRIES:
        wrong = [dc for dc in data
                if dc.get('country') == country
                and dc.get('city_coords')
                and dc['city_coords'][0] > 0]

        if wrong:
            print(f"  WARNING: {country} still has {len(wrong)} positive latitudes")
            still_wrong += len(wrong)

    if still_wrong == 0:
        print(f"  [OK] All Southern Hemisphere coordinates are correct!")
    else:
        print(f"  [ERROR] {still_wrong} entries still have wrong signs")

    return still_wrong == 0

if __name__ == '__main__':
    print("="*60)
    print("SOUTHERN HEMISPHERE LATITUDE FIX")
    print("="*60)

    # Fix both data files
    fixed_original = fix_coordinates('datacenters.json', 'datacenters.json')
    fixed_cleaned = fix_coordinates('datacenters_cleaned.json', 'datacenters_cleaned.json')

    print(f"\n" + "="*60)
    print(f"TOTAL FIXED: {fixed_original + fixed_cleaned} coordinates")
    print("="*60)

    # Verify fixes
    verify_original = verify_fix('datacenters.json')
    verify_cleaned = verify_fix('datacenters_cleaned.json')

    if verify_original and verify_cleaned:
        print(f"\n✓ ALL FIXES VERIFIED SUCCESSFULLY!")
    else:
        print(f"\n✗ VERIFICATION FAILED - Manual review needed")
