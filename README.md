# ATLAS
## **A**ll **T**he **L**ocations of **A**ll **S**ervers

🌍 **[LIVE INTERACTIVE MAP](https://ringmast4r.github.io/ATLAS_A-Data-Center-Project/)** 🌍

A comprehensive global data center intelligence system mapping the world's critical infrastructure.

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

## ⚡ Latest Enhancements (v2.2)

### 🚀 Cloudflare R2 + Workers API (v2.2)
**Performance & Architecture Upgrade:**
- 📦 **Migrated 1.8MB database to Cloudflare R2** object storage
- ⚡ **Smart filtering API** reduces page loads from 1.8MB → ~100KB (18x faster)
- 🌐 **Edge caching** via Cloudflare Workers for global low-latency access
- 🔌 **RESTful API endpoints**: `/api/all`, `/api/search`, `/api/country`, `/api/stats`
- 💰 **Cost-effective**: Nearly free operation on Cloudflare free tier
- 🔒 **CORS-enabled** for seamless browser integration

### 🎨 UI Optimization & Professional Design (v2.2)
**Compact, Clean Interface:**
- 📐 **40% reduction in UI footprint** - headers, panels, buttons all optimized
- 🎯 **Two-column layout**: Search filters (left) | Action buttons (right)
- 📏 **Consistent sizing**: 6px/10px padding, 11-12px fonts throughout
- 🔲 **Subtle 2px border-radius** on all UI elements
- 🖼️ **Clean map view**: Hidden Leaflet attribution for distraction-free experience
- ⚡ **Better UX**: Larger search box (320px), organized controls

### 📸 Screenshot Export with Embedded Metadata (v2.2)
**Professional Map Capture:**
- 🖼️ **High-resolution export**: 2x scale capture for crisp quality
- 🏷️ **Embedded watermark**: "by ringmast4r" branding in every screenshot
- 📊 **Auto-embedded data**: Facility count, coordinates, zoom, timestamp, URL
- 💾 **PNG format**: Maximum quality (1.0) with html2canvas library
- 🔍 **Hidden feature**: Users just see "Screenshot" button, data embeds automatically

### 🔍 Massive SEO Optimization (v2.2)
**Search Engine Domination:**
- 🎯 **500+ strategic keywords**: data centers, cloud infrastructure, colocation, edge computing, CDN, etc.
- 🏢 **All major providers**: AWS, Azure, Google Cloud, Equinix, Digital Realty, etc.
- 📍 **Global tech hubs**: Silicon Valley, London, Singapore, Tokyo, Sydney, Amsterdam, etc.
- 📱 **Open Graph + Twitter Cards**: Perfect social media sharing
- ⭐ **Schema.org structured data**: Rich search results with 4.9★ rating
- 🤖 **Multi-engine optimization**: Google, Bing, with specialized bot directives

## ⚡ Previous Enhancements (v2.0-2.1)

### 🔬 Advanced Data Cleaning & Optimization
**Critical Issues Discovered & Fixed:**
- 🔍 **970 entries (15.5%)** had missing country fields → **Fixed 707 via intelligent address parsing (73% improvement)**
- 🔍 **1,708 US entries (83.5%)** lacked state information → **Added 1,434 via ZIP code geocoding**
- 🔍 **Only 36.6% (2,292)** had precise city-level coordinates
- ✅ **Result:** Reduced invalid plotting by 73% (970 → 263 remaining)

**Automated Data Cleaning Script:**
- Expanded country dictionary to 200+ countries/territories (UN members + territories)
- Comprehensive country alias system (USA→United States, UK→United Kingdom, Nederland→Netherlands, etc.)
- Special character handling (Côte d'Ivoire, etc.)
- Multi-word country name support (United Arab Emirates, South Korea, etc.)
- US state geocoding via ZIP code ranges (all 50 states + DC)
- Coordinate validation (lat: -90 to 90, lon: -180 to 180)
- Created optimized `datacenters_cleaned.json` database

### 🌍 Batch Geocoding & Coordinate Accuracy (v2.1)
**Major Accuracy Improvement:**
- 🎯 **Batch geocoded 3,973 facilities** using OpenStreetMap Nominatim API
- 📍 **Added 2,119 precise coordinates** (53% success rate)
- 📈 **Coverage increased: 36.6% → 70.4%** (2,293 → 4,412 facilities with coordinates)
- 🔧 **Fixed critical coordinate errors:**
  - 261 Southern Hemisphere facilities with inverted latitude signs
  - 3 Australia facilities with UK/Europe coordinates
  - 6 facilities with completely wrong city coordinates
  - Hawaii & Iceland state/country fallback coordinate corrections

**Geocoding Methodology:**
- Free OpenStreetMap Nominatim API (no cost, no API key required)
- Address-to-coordinate conversion with ~100m accuracy
- Country-specific boundary validation
- Automatic retry logic and error handling
- Rate-limited to 1 request/second (API compliance)

**Result:** Facilities now plot at actual street addresses instead of state/country centers (50-200 miles more accurate)

### 📊 Interactive Statistics Dashboard
- **Real-time Analytics** with Chart.js integration
- **Top 10 Countries** - Bar chart showing facility distribution
- **Top 10 Operators** - Bar chart of leading data center providers
- **Data Quality Metrics** - Doughnut chart displaying coordinate precision stats
- **Regional Distribution** - Pie chart of global infrastructure spread
- **Live Metrics** - Key stats updating dynamically based on filtered data
- **Collapsible Panel** - Matrix-themed UI with smooth animations

### 🎨 Multi-Theme Support (5 Themes)
- 🟢 **Dark Matrix** (CartoDB Dark) - Default cybersecurity aesthetic
- ☀️ **Light Professional** (OpenStreetMap) - Clean business presentation
- 🛰️ **Satellite View** (ESRI World Imagery) - Real satellite photography
- 🗺️ **Topographic** (OpenTopoMap) - Terrain and elevation mapping
- 🌊 **Ocean Navigation** (ESRI Ocean Base) - Maritime infrastructure focus
- CSS variable system for dynamic UI theming across all components
- LocalStorage persistence - remembers user preference

### 🛠️ Advanced Geospatial Analysis Tools

**📍 Radius Search**
- Interactive circle drawing with click-to-place center point
- Customizable radius (1-10,000 miles or kilometers)
- Haversine distance calculations for accurate great-circle distances
- Real-time facility discovery within radius
- Results sorted by distance with top 10 display
- Visual circle overlay with adjustable parameters

**📏 Distance Calculator**
- Measure precise distance between any two points on the map
- Click-to-place Point A and Point B markers
- Support for 3 unit types: Miles, Kilometers, Nautical Miles
- Visual line drawing between points with dashed styling
- Real-time unit conversion
- Auto-zoom to fit both points in view

**🎯 Proximity Analysis**
- Click any facility to find N nearest neighbors (1-50)
- Haversine-based distance ranking
- Visual connection lines (top 3 highlighted in green, others in yellow)
- Detailed neighbor information (name, company, location, distance)
- Configurable neighbor count and distance units
- Auto-zoom to display all related facilities

### 💾 Export Functionality
- **CSV Export** - Properly escaped, Excel-compatible format
- **JSON Export** - Structured data for API/application integration
- **GeoJSON Export** - Geographic format with coordinates for GIS tools
- **📸 Screenshot Export** - High-res 2x PNG with embedded metadata (facility count, coordinates, timestamp, ringmast4r branding)
- Smart coordinate fallback system (city → state → country)
- Timestamped filenames for version tracking
- Export visible/filtered results only

### 🚀 Performance & Visualization
- **Marker Clustering** - Smart proximity grouping for 6,266 markers (dramatic performance boost)
- **Heatmap Layer** - Infrastructure density visualization with Matrix-style gradient
- **Precision Mapping** - Eliminated ocean/null island plotting (0,0 coordinates)
- **Enhanced UI** - Matrix-themed cluster bubbles with dynamic sizing
- **Instant Filtering** - Real-time search across 6,266 entries
- **Live Statistics** - Dynamic country/facility count updates

### Quick Stats

- **Total Data Centers**: 6,266
- **Countries Covered**: 155
- **Companies Tracked**: 2,508
- **Top Country**: United States (2,070 facilities - 33%)
- **Top Operator**: Equinix (177 facilities)

See [STATISTICS.md](STATISTICS.md) for detailed breakdowns and regional analysis.

### 🎮 How to Use the Interactive Map

**Basic Navigation:**
- **Search Bar** - Type facility name, company, city, state, or country
- **Filters** - Use dropdown menus to filter by country or company
- **Zoom** - Scroll or pinch to zoom, click clusters to expand

**Advanced Tools (Toolbar Buttons):**

1. **🔥 Toggle Heatmap** - Switch between marker view and density heatmap
2. **📊 Statistics Dashboard** - View interactive charts and analytics
3. **🎨 Theme Selector** - Choose from 5 map themes (dropdown menu)
4. **💾 Export Data** - Download visible facilities in CSV, JSON, or GeoJSON format
5. **📍 Radius Search** - Click button → Click map → Set radius → View facilities within distance
6. **📏 Distance Calculator** - Click button → Click Point A → Click Point B → View distance
7. **🎯 Proximity Analysis** - Click button → Click any facility marker → View N nearest neighbors

**Tips:**
- Click any facility marker to view detailed information
- Use filters before exporting to get specific subsets
- Proximity Analysis shows top 3 neighbors highlighted in green
- Theme preference is saved automatically

### Files

#### Data Files
- **`datacenters_cleaned.json`** ⭐ **NEW** - Optimized dataset with country/state extraction and coordinate validation
- **`datacenters_processed.csv`** - Processed dataset with parsed address fields (CSV format)
- **`datacenters_original_scraped.csv`** - Original scraped data (reference)
- **`datacenters.json`** - JSON format for API/application integration with structured address data

#### Interactive Tools
- **`index.html`** - Live interactive world map with:
  - ✨ **Marker Clustering** - Smart proximity grouping for 6,266 facilities
  - 🔥 **Heatmap Layer** - Density visualization with Matrix-style gradient
  - 🔍 **Advanced Search** - Real-time filtering (name, company, city, state, country)
  - 📊 **Statistics Dashboard** - 4 interactive charts (Chart.js)
  - 🎨 **Multi-Theme Support** - 5 map themes (Dark Matrix, Light, Satellite, Topographic, Ocean)
  - 💾 **Export Tools** - CSV/JSON/GeoJSON download of filtered data
  - 📍 **Radius Search** - Find facilities within customizable distance from any point
  - 📏 **Distance Calculator** - Measure between two points (miles/km/nautical miles)
  - 🎯 **Proximity Analysis** - Find N nearest neighbors to any facility
  - 🎯 **Country/Company Filtering** - Dropdown filters for precise queries
  - 📍 **Interactive Results Panel** - Click-through facility details

#### Utilities
- **`clean_data.py`** ⭐ **NEW** - Data cleaning script with country/state extraction and coordinate validation

#### Documentation
- **`STATISTICS.md`** - Comprehensive statistics and regional breakdowns
- **`README.md`** - This file
- **`LICENSE`** - Usage terms

### Data Schema

**CSV Format** (`datacenters_processed.csv`):
```csv
name,company,city,administrative_area,country,address
```

**JSON Format** (`datacenters.json`):
```json
[
  {
    "name": "NAP de las Americas Madrid",
    "company": "Terremark",
    "city": "Madrid",
    "country": "Spain",
    "address": "Calle de Yecora, 4 28009 Madrid Spain"
  }
]
```

**Field Descriptions:**
- `administrative_area` - First-level administrative division (e.g., US states, Canadian provinces, UK counties, German Länder, French régions)
- The JSON format includes additional fields like `street`, `state`, `zip`, and `city_coords` for internal map processing

**Sample Records:**
```
NAP de las Americas Madrid,Terremark,Madrid,,Spain,"Calle de Yecora, 4 28009 Madrid Spain"
Handy Networks Denver,Handy Networks,Denver,Colorado,United States,"1801 California St, Suite 240 Denver"
Central Office 2,StarHub Ltd.,Singapore,,Singapore,19 Tai Seng Dr 535222 Singapore Singapore
Toronto,Allied Properties REIT,Toronto,Ontario,Canada,151 Front Street Toronto Canada
```

### Usage Examples

**Python - Load CSV:**
```python
import csv

with open('datacenters_processed.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"{row['name']} - {row['city']}, {row['country']}")
```

**Python - Load JSON:**
```python
import json

with open('datacenters.json', 'r', encoding='utf-8') as f:
    datacenters = json.load(f)

# Filter by country
us_datacenters = [dc for dc in datacenters if dc.get('country') == 'United States']

# Filter by city
london_datacenters = [dc for dc in datacenters if dc.get('city') == 'London']

# Filter by company
equinix_facilities = [dc for dc in datacenters if 'Equinix' in dc.get('company', '')]

# Search across all fields
search_term = 'miami'
results = [dc for dc in datacenters
           if search_term.lower() in str(dc.get('address', '')).lower() or
              search_term.lower() in str(dc.get('city', '')).lower()]
```

**JavaScript - Fetch and Query:**
```javascript
fetch('datacenters.json')
  .then(response => response.json())
  .then(data => {
    // Find all datacenters in a country
    const ukDatacenters = data.filter(dc => dc.country === 'United Kingdom');

    // Find all datacenters in a US state
    const californiaDatacenters = data.filter(dc => dc.state === 'California');

    // Find all datacenters in a city
    const nycDatacenters = data.filter(dc => dc.city === 'New York');

    // Get unique countries
    const countries = [...new Set(data.map(dc => dc.country))];

    // Get unique US states
    const states = [...new Set(data.filter(dc => dc.state).map(dc => dc.state))];
  });
```

**Command Line - Query with jq:**
```bash
# Count by country
jq 'group_by(.country) | map({country: .[0].country, count: length})' datacenters.json

# Count by state (US only)
jq '[.[] | select(.state != "")] | group_by(.state) | map({state: .[0].state, count: length})' datacenters.json

# Find specific operator
jq '.[] | select(.company | contains("Equinix"))' datacenters.json

# Extract all facilities in a state
jq '.[] | select(.state == "Florida")' datacenters.json

# Extract all facilities in a city
jq '.[] | select(.city == "Miami")' datacenters.json
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
