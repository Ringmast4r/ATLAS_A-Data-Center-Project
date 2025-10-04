# Global Data Center Intelligence System

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

The scraped intelligence includes **6,265 verified data center locations** across every continent, forming one of the most comprehensive open-source data center location databases ever compiled.

### Files

- `datacenters_scraped.csv` - Primary dataset with 6,265+ global data center records
- `DataCenters.csv` - Secondary dataset
- `datacenters.pdf` - Supporting documentation

### Data Schema

```csv
Data Center Name,Company,Address
```

**Sample Records:**
```
NAP de las Americas Madrid,Terremark,"Calle de Yecora, 4 28009 Madrid Spain"
Central Office 2,StarHub Ltd.,19 Tai Seng Dr 535222 Singapore Singapore
Cluj-Napoca,GTS Telecom SRL,Str. Garii nr. 21 400267 Cluj-Napoca Romania
Etix Accra #1,Etix Everywhere,R40 Accra Ghana
```

### Coverage

Global coverage spanning:
- North America
- Europe
- Asia-Pacific
- Middle East
- Africa
- South America

## License

All Rights Reserved. This dataset may not be used, copied, modified, or distributed without explicit written permission from the author.

---

*Built for commercial geospatial intelligence. Powered by OSINT methodologies.*
