import csv
import json
import re

def parse_address(address):
    """Parse address into components: city, state/province, zip, country"""
    # Remove extra whitespace
    address = ' '.join(address.split())

    # Common patterns for US addresses
    us_states = {
        'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
        'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
        'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
        'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
        'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
        'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
        'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
        'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
        'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
        'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
        'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
        'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
        'WI': 'Wisconsin', 'WY': 'Wyoming', 'DC': 'District of Columbia'
    }

    # Canadian provinces
    ca_provinces = {
        'AB': 'Alberta', 'BC': 'British Columbia', 'MB': 'Manitoba', 'NB': 'New Brunswick',
        'NL': 'Newfoundland and Labrador', 'NS': 'Nova Scotia', 'NT': 'Northwest Territories',
        'NU': 'Nunavut', 'ON': 'Ontario', 'PE': 'Prince Edward Island', 'QC': 'Quebec',
        'SK': 'Saskatchewan', 'YT': 'Yukon'
    }

    # Split address into parts
    parts = address.split()

    country = None
    state = None
    city = None
    zip_code = None
    street = None

    # Detect country (usually last word or two)
    if len(parts) > 0:
        # Check for common countries
        if parts[-1] in ['USA', 'US', 'America']:
            country = 'United States'
            parts = parts[:-1]
        elif parts[-1] == 'Canada':
            country = 'Canada'
            parts = parts[:-1]
        elif parts[-1] == 'UK' or (len(parts) > 1 and parts[-2] + ' ' + parts[-1] == 'United Kingdom'):
            country = 'United Kingdom'
            if len(parts) > 1 and parts[-2] == 'United':
                parts = parts[:-2]
            else:
                parts = parts[:-1]
        elif parts[-1] in ['Australia', 'Singapore', 'Germany', 'France', 'Spain', 'Italy',
                           'Netherlands', 'Belgium', 'Switzerland', 'Austria', 'Sweden',
                           'Norway', 'Denmark', 'Finland', 'Poland', 'Ireland', 'Portugal',
                           'Greece', 'Romania', 'Bulgaria', 'Hungary', 'India', 'China',
                           'Japan', 'Brazil', 'Mexico', 'Argentina', 'Chile', 'Colombia',
                           'Russia', 'Nigeria', 'Ghana', 'Kenya', 'Kuwait', 'Qatar']:
            country = parts[-1]
            parts = parts[:-1]
        elif len(parts) > 1 and parts[-2] + ' ' + parts[-1] in ['South Africa', 'New Zealand',
                                                                   'South Korea', 'Saudi Arabia']:
            country = parts[-2] + ' ' + parts[-1]
            parts = parts[:-2]

    # Look for state abbreviations in remaining parts
    for i, part in enumerate(parts):
        if part in us_states:
            state = us_states[part]
            # City is typically before state
            if i > 0:
                city = parts[i-1]
                # Zip might be before city
                if i > 1 and re.match(r'\d{5}', parts[i-2]):
                    zip_code = parts[i-2]
                    street = ' '.join(parts[:i-2])
                else:
                    street = ' '.join(parts[:i-1])
            break
        elif part in ca_provinces:
            state = ca_provinces[part]
            if i > 0:
                city = parts[i-1]
                if i > 1 and re.match(r'[A-Z]\d[A-Z]\s*\d[A-Z]\d', parts[i-2]):
                    zip_code = parts[i-2]
                    street = ' '.join(parts[:i-2])
                else:
                    street = ' '.join(parts[:i-1])
            break

    # If no state found, try to extract city (often the last remaining part before country)
    if not city and len(parts) > 0:
        # Check for zip code patterns
        for i in range(len(parts)-1, -1, -1):
            if re.match(r'\d{5}', parts[i]) or re.match(r'\d{4,6}', parts[i]):
                zip_code = parts[i]
                if i < len(parts) - 1:
                    city = parts[i+1]
                    street = ' '.join(parts[:i])
                break

        if not city and len(parts) > 0:
            city = parts[-1]
            street = ' '.join(parts[:-1])

    if not street and len(parts) > 0:
        street = ' '.join(parts)

    return {
        'street': street or '',
        'city': city or '',
        'state': state or '',
        'zip': zip_code or '',
        'country': country or ''
    }

# Read the scraped CSV
datacenters = []
with open('datacenters_scraped.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        parsed_addr = parse_address(row['Address'])

        datacenter = {
            'name': row['Data Center Name'],
            'company': row['Company'],
            'street': parsed_addr['street'],
            'city': parsed_addr['city'],
            'state': parsed_addr['state'],
            'zip': parsed_addr['zip'],
            'country': parsed_addr['country'],
            'address': row['Address']  # Keep full address for reference
        }
        datacenters.append(datacenter)

# Save as JSON
with open('datacenters.json', 'w', encoding='utf-8') as f:
    json.dump(datacenters, f, indent=2, ensure_ascii=False)

# Save as CSV
with open('datacenters_clean.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = ['name', 'company', 'street', 'city', 'state', 'zip', 'country', 'address']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(datacenters)

print(f'Processed {len(datacenters)} datacenters')
print('Sample entries:')
for dc in datacenters[:5]:
    print(f"\n{dc['name']}")
    print(f"  City: {dc['city']}, State: {dc['state']}, Country: {dc['country']}")
