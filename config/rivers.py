"""River monitoring station configurations."""

# Montana Regions for filtering
REGIONS = {
    'Flathead': ['Flathead', 'Swan', 'Stillwater', 'Whitefish'],
    'Missoula': ['Clark Fork', 'Bitterroot', 'Blackfoot', 'Rock Creek', 'St. Regis', 'Little Blackfoot'],
    'Northwest': ['Kootenai', 'Yaak', 'Fisher', 'Thompson'],
    'Missouri': ['Missouri', 'Madison', 'Gallatin', 'Jefferson', 'Boulder', 'Big Hole', 'Ruby', 'Dearborn', 'Smith', 'Sun', 'Teton', 'Marias'],
    'All': []  # Shows all rivers
}

# USGS station IDs for Western Montana rivers
# Format: (Name, USGS Site ID, has_temperature, region)
RIVER_STATIONS = [
    # Initial 10 stations
    ("Flathead River at Columbia Falls", "12363000", True),
    ("Flathead River near Polson", "12372000", True),
    ("Flathead River at Perma", "12388700", True),
    ("North Fork Flathead River near Polebridge", "12355000", True),
    ("South Fork Flathead River at Spotted Bear", "12359800", True),
    ("Clark Fork at St. Regis", "12354500", True),
    ("Bitterroot River near Missoula", "12352500", True),
    ("Blackfoot River near Bonner", "12340000", True),
    ("Swan River near Bigfork", "12370000", True),
    ("Jocko River near Arlee", "12380000", False),

    # Additional Western Montana stations (~30 more)
    ("Missouri River near Toston", "06054500", True),
    ("Missouri River at Cascade", "06090800", True),
    ("Madison River near West Yellowstone", "06037500", True),
    ("Madison River below Ennis Lake", "06041000", True),
    ("Gallatin River near Gallatin Gateway", "06043500", True),
    ("Jefferson River near Twin Bridges", "06026500", True),
    ("Clark Fork near Drummond", "12329500", True),
    ("Clark Fork at Turah Bridge near Bonner", "12334550", True),
    ("Clark Fork above Missoula", "12340500", True),
    ("Clark Fork at Milltown", "12334510", True),
    ("Bitterroot River at Darby", "12339500", True),
    ("Bitterroot River near Darby", "12338500", True),
    ("Rock Creek near Clinton", "12331800", True),
    ("Kootenai River near Libby", "12301300", True),
    ("Kootenai River at Libby", "12303100", True),
    ("Yaak River near Troy", "12304500", True),
    ("Fisher River near Libby", "12303500", True),
    ("Thompson River near Thompson Falls", "12389500", True),
    ("St. Regis River near St. Regis", "12353800", True),
    ("Little Blackfoot River near Elliston", "12323600", True),
    ("Sun River near Vaughn", "06089000", True),
    ("Teton River near Dutton", "06109500", True),
    ("Marias River near Shelby", "06099500", True),
    ("Stillwater River near Whitefish", "12366000", True),
    ("Whitefish River near Kalispell", "12369000", True),
    ("Middle Fork Flathead River near West Glacier", "12358500", True),
    ("Boulder River near Boulder", "06033000", True),
    ("Big Hole River near Melrose", "06025500", True),
    ("Ruby River above reservoir near Alder", "06019500", True),
    ("Dearborn River near Craig", "06073500", True),
    ("Smith River near Eden", "06077500", True),
]

def get_river_region(river_name):
    """Determine which region a river belongs to."""
    name_lower = river_name.lower()

    for region, keywords in REGIONS.items():
        if region == 'All':
            continue
        for keyword in keywords:
            if keyword.lower() in name_lower:
                return region

    return 'Missoula'  # Default region

def get_rivers_by_region(region):
    """Get all rivers in a specific region."""
    if region == 'All':
        return RIVER_STATIONS

    filtered = []
    for river_info in RIVER_STATIONS:
        river_region = get_river_region(river_info[0])
        if river_region == region:
            filtered.append(river_info)

    return filtered

# Historical average data (placeholder - will be fetched from USGS or calculated)
# Format: {site_id: {month: {flow_avg, temp_avg}}}
HISTORICAL_AVERAGES = {}
