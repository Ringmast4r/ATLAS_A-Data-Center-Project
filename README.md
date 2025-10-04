# Global Data Center Intelligence System

🌍 **[LIVE INTERACTIVE MAP](https://ringmast4r.github.io/datacenter-atlas/)** 🌍

## Project Origin

This OSINT scraping tool was developed as part of a critical infrastructure mapping initiative for a commercial geospatial intelligence platform. Our company was building an advanced location-based system utilizing cellular coordinates and infrastructure data to power next-generation mapping and analytics services.

## Mission

**Objective**: Map every data center on Earth.

As critical infrastructure nodes forming the backbone of the global internet, data centers represent essential geolocation targets for our commercial database. This tool was engineered to systematically discover, validate, and extract GPS coordinates for data center facilities worldwide through open-source intelligence gathering.

## What It Does

The scraper autonomously harvests data center locations from public web sources, extracting:
- Facility names and operators
- Physical addresses
- Geographic coordinates
- Infrastructure classifications

The resulting dataset populates a specialized layer within our geospatial database, enabling critical infrastructure analysis, network topology mapping, and location-based services for commercial applications.

## Dataset

The scraped intelligence includes **6,266 verified data center locations** across 155 countries, operated by 2,508 companies. This represents one of the most comprehensive open-source data center location databases ever compiled.

### Quick Stats

- **Total Data Centers**: 6,266
- **Countries Covered**: 155
- **Companies Tracked**: 2,508
- **Top Country**: United States (2,070 facilities - 33%)
- **Top Operator**: Equinix (177 facilities)

See [STATISTICS.md](STATISTICS.md) for detailed breakdowns and regional analysis.

### Files

#### Data Files
- **`datacenters_clean.csv`** - Cleaned and standardized dataset (CSV format)
- **`datacenters.json`** - JSON format for API/application integration

#### Interactive Tools
- **`index.html`** - Live interactive world map with search/filter capabilities

#### Documentation
- **`STATISTICS.md`** - Comprehensive statistics and regional breakdowns
- **`README.md`** - This file
- **`LICENSE`** - Usage terms

### Data Schema

**CSV Format** (`datacenters_clean.csv`):
```csv
name,company,address,country
```

**JSON Format** (`datacenters.json`):
```json
[
  {
    "name": "NAP de las Americas Madrid",
    "company": "Terremark",
    "address": "Calle de Yecora, 4 28009 Madrid Spain",
    "country": "Spain"
  }
]
```

**Sample Records:**
```
NAP de las Americas Madrid,Terremark,"Calle de Yecora, 4 28009 Madrid Spain",Spain
Central Office 2,StarHub Ltd.,19 Tai Seng Dr 535222 Singapore Singapore,Singapore
Cluj-Napoca,GTS Telecom SRL,Str. Garii nr. 21 400267 Cluj-Napoca Romania,Romania
Etix Accra #1,Etix Everywhere,R40 Accra Ghana,Ghana
```

### Usage Examples

**Python - Load CSV:**
```python
import csv

with open('datacenters_clean.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"{row['name']} in {row['country']}")
```

**Python - Load JSON:**
```python
import json

with open('datacenters.json', 'r', encoding='utf-8') as f:
    datacenters = json.load(f)

# Filter by country
us_datacenters = [dc for dc in datacenters if dc['country'] == 'United States']

# Filter by company
equinix_facilities = [dc for dc in datacenters if 'Equinix' in dc['company']]
```

**JavaScript - Fetch and Query:**
```javascript
fetch('datacenters.json')
  .then(response => response.json())
  .then(data => {
    // Find all datacenters in a country
    const ukDatacenters = data.filter(dc => dc.country === 'United Kingdom');

    // Get unique countries
    const countries = [...new Set(data.map(dc => dc.country))];
  });
```

**Command Line - Query with jq:**
```bash
# Count by country
jq 'group_by(.country) | map({country: .[0].country, count: length})' datacenters.json

# Find specific operator
jq '.[] | select(.company | contains("Equinix"))' datacenters.json

# Extract all facilities in a country
jq '.[] | select(.country == "Germany")' datacenters.json
```

### Coverage

**Global Coverage by Region:**
- **North America**: 2,265 facilities (36.1%)
- **Europe**: 1,778+ facilities (28.4%)
- **Asia-Pacific**: 783+ facilities (12.5%)
- **Africa**: 179+ facilities (2.9%)
- **South America**: 183+ facilities (2.9%)
- **Middle East**: 86+ facilities (1.4%)

**Top 10 Countries:**
1. United States (2,070)
2. United Kingdom (461)
3. Netherlands (296)
4. France (261)
5. Germany (242)
6. Australia (181)
7. Canada (164)
8. India (147)
9. Brazil (141)
10. China (138)

## License

All Rights Reserved. This dataset may not be used, copied, modified, or distributed without explicit written permission from the author.

---

*Built for commercial geospatial intelligence. Powered by OSINT methodologies.*
