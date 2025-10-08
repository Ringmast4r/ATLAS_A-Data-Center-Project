#!/usr/bin/env python3
"""
ATLAS Data Cleaning & Optimization Script
Fixes country parsing, US state extraction, and coordinate validation
"""

import json
import re
from collections import Counter

# US State ZIP code ranges
ZIP_TO_STATE = {
    range(35000, 36999): 'Alabama',
    range(99500, 99999): 'Alaska',
    range(85000, 86999): 'Arizona',
    range(71600, 72999): 'Arkansas',
    range(90000, 96199): 'California',
    range(80000, 81999): 'Colorado',
    range(6000, 6999): 'Connecticut',
    range(19700, 19999): 'Delaware',
    range(20000, 20599): 'District of Columbia',
    range(32000, 34999): 'Florida',
    range(30000, 31999): 'Georgia',
    range(96700, 96999): 'Hawaii',
    range(83200, 83999): 'Idaho',
    range(60000, 62999): 'Illinois',
    range(46000, 47999): 'Indiana',
    range(50000, 52999): 'Iowa',
    range(66000, 67999): 'Kansas',
    range(40000, 42999): 'Kentucky',
    range(70000, 71599): 'Louisiana',
    range(3900, 4999): 'Maine',
    range(20600, 21999): 'Maryland',
    range(1000, 2799): 'Massachusetts',
    range(48000, 49999): 'Michigan',
    range(55000, 56999): 'Minnesota',
    range(38600, 39999): 'Mississippi',
    range(63000, 65999): 'Missouri',
    range(59000, 59999): 'Montana',
    range(68000, 69999): 'Nebraska',
    range(88900, 89999): 'Nevada',
    range(3000, 3899): 'New Hampshire',
    range(7000, 8999): 'New Jersey',
    range(87000, 88499): 'New Mexico',
    range(10000, 14999): 'New York',
    range(27000, 28999): 'North Carolina',
    range(58000, 58999): 'North Dakota',
    range(43000, 45999): 'Ohio',
    range(73000, 74999): 'Oklahoma',
    range(97000, 97999): 'Oregon',
    range(15000, 19699): 'Pennsylvania',
    range(2800, 2999): 'Rhode Island',
    range(29000, 29999): 'South Carolina',
    range(57000, 57999): 'South Dakota',
    range(37000, 38599): 'Tennessee',
    range(75000, 79999): 'Texas',
    range(73301, 73399): 'Texas',
    range(88500, 88599): 'Texas',
    range(84000, 84999): 'Utah',
    range(5000, 5999): 'Vermont',
    range(22000, 24699): 'Virginia',
    range(98000, 99499): 'Washington',
    range(24700, 26999): 'West Virginia',
    range(53000, 54999): 'Wisconsin',
    range(82000, 83199): 'Wyoming',
}

def get_state_from_zip(zip_code):
    """Get US state from ZIP code"""
    if not zip_code:
        return None

    # Extract first 5 digits
    zip_match = re.search(r'(\d{5})', str(zip_code))
    if not zip_match:
        return None

    zip_num = int(zip_match.group(1))

    for zip_range, state in ZIP_TO_STATE.items():
        if zip_num in zip_range:
            return state
    return None

def extract_country_from_address(address):
    """Extract country name from address string"""
    if not address:
        return None

    # Comprehensive country list (UN members + territories)
    countries = [
        # North America
        'United States', 'USA', 'Canada', 'Mexico',

        # Europe
        'United Kingdom', 'UK', 'England', 'Scotland', 'Wales', 'Netherlands', 'Nederland',
        'France', 'Germany', 'Spain', 'Italy', 'Portugal', 'Belgium', 'Austria', 'Switzerland',
        'Sweden', 'Norway', 'Denmark', 'Finland', 'Iceland', 'Ireland', 'Poland', 'Czech Republic',
        'Czechia', 'Slovakia', 'Hungary', 'Romania', 'Bulgaria', 'Greece', 'Croatia', 'Slovenia',
        'Serbia', 'Bosnia', 'Montenegro', 'Albania', 'North Macedonia', 'Macedonia', 'Lithuania',
        'Latvia', 'Estonia', 'Belarus', 'Ukraine', 'Moldova', 'Luxembourg', 'Malta', 'Cyprus',

        # Asia
        'China', 'Japan', 'South Korea', 'Korea', 'India', 'Indonesia', 'Thailand', 'Vietnam',
        'Malaysia', 'Singapore', 'Philippines', 'Pakistan', 'Bangladesh', 'Sri Lanka', 'Myanmar',
        'Cambodia', 'Laos', 'Nepal', 'Afghanistan', 'Iran', 'Iraq', 'Israel', 'Jordan', 'Lebanon',
        'Syria', 'Yemen', 'Oman', 'Kuwait', 'Bahrain', 'Qatar', 'United Arab Emirates', 'UAE',
        'Saudi Arabia', 'Turkey', 'Azerbaijan', 'Georgia', 'Armenia', 'Kazakhstan', 'Uzbekistan',
        'Turkmenistan', 'Kyrgyzstan', 'Tajikistan', 'Mongolia', 'Taiwan', 'Hong Kong', 'Macau',

        # Africa
        'Egypt', 'South Africa', 'Nigeria', 'Kenya', 'Ghana', 'Ethiopia', 'Tanzania', 'Uganda',
        'Morocco', 'Algeria', 'Tunisia', 'Libya', 'Sudan', 'Angola', 'Mozambique', 'Zimbabwe',
        'Zambia', 'Botswana', 'Namibia', 'Senegal', "Côte d'Ivoire", "Cote d'Ivoire", 'Ivory Coast',
        'Burkina Faso', 'Mali', 'Niger', 'Chad', 'Cameroon', 'Gabon', 'Congo', 'Rwanda', 'Burundi',
        'Somalia', 'Mauritius', 'Madagascar', 'Seychelles',

        # South America
        'Brazil', 'Argentina', 'Chile', 'Peru', 'Colombia', 'Venezuela', 'Ecuador', 'Bolivia',
        'Paraguay', 'Uruguay', 'Guyana', 'Suriname',

        # Central America & Caribbean
        'Guatemala', 'Honduras', 'El Salvador', 'Nicaragua', 'Costa Rica', 'Panama', 'Cuba',
        'Dominican Republic', 'Haiti', 'Jamaica', 'Trinidad', 'Barbados', 'Bahamas',

        # Oceania
        'Australia', 'New Zealand', 'Papua New Guinea', 'Fiji', 'Samoa', 'Tonga',

        # Middle East
        'Palestine', 'Russia'
    ]

    # Check last part of address
    address_parts = address.strip().split()
    if len(address_parts) > 0:
        # Check last word
        last_word = address_parts[-1]
        for country in countries:
            if country.lower() == last_word.lower():
                return country

        # Check last two words
        if len(address_parts) > 1:
            last_two = ' '.join(address_parts[-2:])
            for country in countries:
                if country.lower() == last_two.lower():
                    return country

        # Check last three words
        if len(address_parts) > 2:
            last_three = ' '.join(address_parts[-3:])
            for country in countries:
                if country.lower() == last_three.lower():
                    return country

    return None

def normalize_country_name(country):
    """Normalize country names with aliases"""
    if not country:
        return None

    country = country.strip()
    country_upper = country.upper()

    # Country aliases and normalizations
    aliases = {
        # USA variants
        'USA': 'United States',
        'US': 'United States',
        'UNITED STATES OF AMERICA': 'United States',

        # UK variants
        'UK': 'United Kingdom',
        'GREAT BRITAIN': 'United Kingdom',
        'ENGLAND': 'United Kingdom',
        'SCOTLAND': 'United Kingdom',
        'WALES': 'United Kingdom',

        # Netherlands variants
        'NEDERLAND': 'Netherlands',
        'THE NETHERLANDS': 'Netherlands',
        'HOLLAND': 'Netherlands',

        # Other common aliases
        'KOREA': 'South Korea',
        'UAE': 'United Arab Emirates',
        'CZECHIA': 'Czech Republic',
        'MACEDONIA': 'North Macedonia',
        'IVORY COAST': "Côte d'Ivoire",
        "COTE D'IVOIRE": "Côte d'Ivoire",
        'BURMA': 'Myanmar',
        'PERSIA': 'Iran',
        'HOLLAND': 'Netherlands',
    }

    if country_upper in aliases:
        return aliases[country_upper]

    return country

def clean_datacenters(input_file, output_file):
    """Clean and optimize datacenter data"""
    print("Loading data...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Total entries: {len(data)}")

    stats = {
        'countries_fixed': 0,
        'states_added': 0,
        'coords_validated': 0,
        'invalid_coords': 0
    }

    for entry in data:
        # Fix missing countries
        if not entry.get('country'):
            extracted = extract_country_from_address(entry.get('address', ''))
            if extracted:
                entry['country'] = normalize_country_name(extracted)
                stats['countries_fixed'] += 1
        else:
            entry['country'] = normalize_country_name(entry.get('country'))

        # Extract US states from ZIP codes
        if entry.get('country') == 'United States' and not entry.get('state'):
            state_from_zip = get_state_from_zip(entry.get('zip'))
            if state_from_zip:
                entry['state'] = state_from_zip
                stats['states_added'] += 1

        # Validate coordinates
        if 'city_coords' in entry and entry['city_coords']:
            lat, lon = entry['city_coords']
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                stats['coords_validated'] += 1
            else:
                stats['invalid_coords'] += 1
                entry['city_coords'] = None  # Remove invalid coords

    print(f"\nCleaning Results:")
    print(f"  Countries fixed: {stats['countries_fixed']}")
    print(f"  States added: {stats['states_added']}")
    print(f"  Valid coordinates: {stats['coords_validated']}")
    print(f"  Invalid coordinates removed: {stats['invalid_coords']}")

    # Save cleaned data
    print(f"\nSaving cleaned data to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Generate statistics
    countries = Counter([d.get('country') for d in data if d.get('country')])
    companies = Counter([d.get('company') for d in data])

    print(f"\nTop 10 Countries:")
    for country, count in countries.most_common(10):
        print(f"  {country}: {count}")

    print(f"\nTop 10 Companies:")
    for company, count in companies.most_common(10):
        print(f"  {company}: {count}")

    # Check remaining issues
    still_empty = sum(1 for d in data if not d.get('country'))
    print(f"\nRemaining entries without country: {still_empty}")

    return data

if __name__ == '__main__':
    cleaned_data = clean_datacenters('datacenters.json', 'datacenters_cleaned.json')
    print("\n[SUCCESS] Data cleaning complete!")
