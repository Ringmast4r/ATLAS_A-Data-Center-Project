#!/usr/bin/env python3
"""
Fix incorrect state and country coordinates in index.html

Issues found:
- Hawaii: Wrong coordinates (off by 0.36° longitude)
- Iceland: Wrong coordinates (off by 2.92° longitude - major error!)
"""

import re

# Coordinate fixes needed
FIXES = {
    # US States
    "'Hawaii': [21.094318, -157.498337]": "'Hawaii': [21.3069, -157.8583]",  # Honolulu

    # Countries
    "'Iceland': [64.9631, -19.0208]": "'Iceland': [64.1466, -21.9426]",  # Reykjavik
}

def fix_coordinates(file_path):
    """Fix coordinates in index.html"""

    print(f"Reading {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    fixes_applied = 0

    for old_coord, new_coord in FIXES.items():
        if old_coord in content:
            content = content.replace(old_coord, new_coord)
            fixes_applied += 1

            # Extract location name for display
            location = old_coord.split("'")[1]
            old_vals = old_coord.split('[')[1].split(']')[0]
            new_vals = new_coord.split('[')[1].split(']')[0]

            print(f"  Fixed {location}:")
            print(f"    Old: [{old_vals}]")
            print(f"    New: [{new_vals}]")

    if fixes_applied > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n[SUCCESS] Applied {fixes_applied} coordinate fixes to {file_path}")
    else:
        print(f"\n[INFO] No fixes needed in {file_path}")

    return fixes_applied

def verify_fixes(file_path):
    """Verify the fixes were applied"""

    print(f"\nVerifying {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    all_good = True
    for old_coord, new_coord in FIXES.items():
        location = old_coord.split("'")[1]

        if old_coord in content:
            print(f"  [ERROR] {location} still has old coordinates!")
            all_good = False
        elif new_coord in content:
            print(f"  [OK] {location} coordinates corrected")
        else:
            print(f"  [WARNING] {location} coordinates not found")

    return all_good

if __name__ == '__main__':
    print("="*60)
    print("COORDINATE FIX SCRIPT")
    print("="*60)
    print("\nIssues to fix:")
    print("- Hawaii: 0.36° longitude error")
    print("- Iceland: 2.92° longitude error (MAJOR!)")
    print()

    # Fix coordinates
    fixes_applied = fix_coordinates('index.html')

    # Verify
    if fixes_applied > 0:
        if verify_fixes('index.html'):
            print(f"\n[SUCCESS] All coordinate fixes verified!")
        else:
            print(f"\n[ERROR] Verification failed!")

    print("\n" + "="*60)
