"""
Configuration file for real estate price prediction
Contains locality lists, feature definitions, and settings
"""

# ============================================================================
# AHMEDABAD LOCALITIES (150+ locations)
# ============================================================================

AHMEDABAD_LOCALITIES = [
    # Tier 1 - Premium localities
    "S G Highway", "Satellite", "Bopal", "Prahlad Nagar", "Vastrapur",
    "Bodakdev", "Thaltej", "Ambawadi", "Navrangpura", "C G Road",
    "New CG Road", "Gulbai Tekra", "Paldi", "Ellis Bridge",
    
    # Tier 2 - Mid-range localities
    "Dholera", "Jagatpur", "Chandkheda", "Gota", "Vaishno Devi",
    "Shela", "South Bopal", "Naranpura", "Bavla", "Maninagar",
    "Vejalpur", "Noblenagar", "Ghatlodia", "Motera", "Memnagar",
    "Ranip", "Vastral", "Gurukul", "Nikol", "S P Ring Road",
    "Shilaj", "Vasna", "Chandlodia", "Science City", "Sabarmati",
    "Ghodasar", "Juhapura", "New Ranip", "Narol", "Jivrajpark",
    "Bapunagar", "Tragad", "Nava Wadaj", "Shyamal", "Gokuldham",
    "Sanand", "Vatva", "Ashram road", "Dholka", "Sola",
    "Ghuma", "Jodhpur", "Isanpur", "Shahibaug", "Thaltej Road",
    "Changodar", "Kankaria", "New Maninagar", "Saraspur", "Makarba",
    "Amraiwadi", "Odhav", "Palodia", "Sanand - Nalsarovar Road", "Nehrunagar",
    
    # Tier 3 - Budget-friendly localities
    "Pipali Highway", "Naroda", "Ramdev Nagar", "Sarkhej", "Ambli",
    "Kathwada", "Nirnay Nagar", "Sanathal", "Sughad", "Hathijan",
    "Manipur", "Chanakyapuri", "Shah E Alam Roja", "Nava Naroda", "Khokra",
    "Saijpur Bogha", "Godhavi", "Mahadev Nagar", "Racharda", "Rakanpur",
    "Nasmed", "Jashoda Nagar", "Lambha", "Koteshwar", "Bagodara",
    "Lapkaman", "Anandnagar", "Kubernagar", "Sola Road", "Ognaj",
    "Bhadaj", "Shantipura", "Hansol", "Naroda road", "Narol Road",
    "Moraiya", "Behrampura", "Hatkeshwar", "Kalupur", "Meghani Nagar",
    "Barejadi", "kheda", "Khodiar Nagar", "Bhat", "Asarwa",
    "Chharodi", "Dhandhuka", "Khanpur", "Naroda GIDC", "Raipur",
    "Shahpur", "Thakkarbapa Nagar", "Usmanpura", "132 Feet Ring Road",
    "Sanand-Viramgam Road", "Ahmedabad-Rajkot-Highway", "Aslali", "Ayojan Nagar",
    "Bhadra", "Dani Limbada", "Dariapur", "Dudheshwar", "Girdhar Nagar",
    "Gomtipur", "Jamalpur", "Juna Wadaj", "Kalapinagar", "Keshav Nagar",
    "Khadia", "Khamasa", "Madhupura", "Navjivan", "Raikhad",
    "Rakhial", "Sadar Bazar", "Vatva GIDC", "Viramgam", "Kali",
    "Santej", "Nandej", "Raska", "Laxmanpura", "Bavla Nalsarovar Road",
    "Unali", "Mandal", "D Colony", "Sardar Colony", "Kotarpur",
    "Mirzapur", "Narayan Nagar", "Kolat", "Purshottam Nagar", "Gita Mandir",
    "Sachana", "Vinzol", "Geratpur", "Sarangpur", "Acher",
    "Hebatpur", "Devdholera", "Lilapur", "Mahemdabad", "Vishala",
    "Ashok Vatika"
]

TIER_1_LOCALITIES = [
    "S G Highway", "Satellite", "Bopal", "Prahlad Nagar", "Vastrapur",
    "Bodakdev", "Thaltej", "Ambawadi", "Navrangpura", "C G Road",
    "New CG Road", "Gulbai Tekra", "Paldi", "Ellis Bridge"]

TIER_2_LOCALITIES = [
    "Dholera", "Jagatpur", "Chandkheda", "Gota", "Vaishno Devi",
    "Shela", "South Bopal", "Naranpura", "Bavla", "Maninagar",
    "Vejalpur", "Noblenagar", "Ghatlodia", "Motera", "Memnagar",
    "Ranip", "Vastral", "Gurukul", "Nikol", "S P Ring Road",
    "Shilaj", "Vasna", "Chandlodia", "Science City", "Sabarmati",
    "Ghodasar", "Juhapura", "New Ranip", "Narol", "Jivrajpark",
    "Bapunagar", "Tragad", "Nava Wadaj", "Shyamal", "Gokuldham",
    "Sanand", "Vatva", "Ashram road", "Dholka", "Sola",
    "Ghuma", "Jodhpur", "Isanpur", "Shahibaug", "Thaltej Road",
    "Changodar", "Kankaria", "New Maninagar", "Saraspur", "Makarba",
    "Amraiwadi", "Odhav", "Palodia", "Sanand - Nalsarovar Road", "Nehrunagar"
]

TIER_3_LOCALITIES = [
    "Pipali Highway", "Naroda", "Ramdev Nagar", "Sarkhej", "Ambli",
    "Kathwada", "Nirnay Nagar", "Sanathal", "Sughad", "Hathijan",
    "Manipur", "Chanakyapuri", "Shah E Alam Roja", "Nava Naroda", "Khokra",
    "Saijpur Bogha", "Godhavi", "Mahadev Nagar", "Racharda", "Rakanpur",
    "Nasmed", "Jashoda Nagar", "Lambha", "Koteshwar", "Bagodara",
    "Lapkaman", "Anandnagar", "Kubernagar", "Sola Road", "Ognaj",
    "Bhadaj", "Shantipura", "Hansol", "Naroda road", "Narol Road",
    "Moraiya", "Behrampura", "Hatkeshwar", "Kalupur", "Meghani Nagar",
    "Barejadi", "kheda", "Khodiar Nagar", "Bhat", "Asarwa",
    "Chharodi", "Dhandhuka", "Khanpur", "Naroda GIDC", "Raipur",
    "Shahpur", "Thakkarbapa Nagar", "Usmanpura", "132 Feet Ring Road",
    "Sanand-Viramgam Road", "Ahmedabad-Rajkot-Highway", "Aslali", "Ayojan Nagar",
    "Bhadra", "Dani Limbada", "Dariapur", "Dudheshwar", "Girdhar Nagar",
    "Gomtipur", "Jamalpur", "Juna Wadaj", "Kalapinagar", "Keshav Nagar",
    "Khadia", "Khamasa", "Madhupura", "Navjivan", "Raikhad",
    "Rakhial", "Sadar Bazar", "Vatva GIDC", "Viramgam", "Kali",
    "Santej", "Nandej", "Raska", "Laxmanpura", "Bavla Nalsarovar Road",
    "Unali", "Mandal", "D Colony", "Sardar Colony", "Kotarpur",
    "Mirzapur", "Narayan Nagar", "Kolat", "Purshottam Nagar", "Gita Mandir",
    "Sachana", "Vinzol", "Geratpur", "Sarangpur", "Acher",
    "Hebatpur", "Devdholera", "Lilapur", "Mahemdabad", "Vishala",
    "Ashok Vatika"
]    

# Normalize localities for matching (lowercase, no spaces)
NORMALIZED_LOCALITIES = {loc.lower().replace(" ", "").replace("-", ""): loc for loc in AHMEDABAD_LOCALITIES}

# ============================================================================
# CORE FEATURES (7-10 most important)
# ============================================================================

CORE_FEATURES = [
    'Price_Lakhs',           # Target variable ONLY
    'Area_SqFt',            # Property area
    'BHK',                  # Number of bedrooms
    'Property_Type',        # Apartment/Villa/House
    'Furnishing_Status',    # Furnished/Semi/Unfurnished
    'Locality',             # Location (WILL BE ENCODED - most important!)
    'Locality_Tier',        # Derived: Tier 1/2/3 (WILL BE ENCODED)
    'Seller_Type',          # Owner/Builder/Dealer/Agent (WILL BE ENCODED)
    'Under_Construction',   # True/False - Property construction status
    'Amenities_Count',      # Number of amenities (gym, pool, garden, etc.)
]

# NOTE: NO Price_Per_SqFt or Bathrooms (correlated with BHK)!
# Locality will be properly encoded as it's the most important feature
# Amenities extracted from Raw_JSON and descriptions

# ============================================================================
# SCRAPING CONFIGURATION
# ============================================================================

SCRAPING_CONFIG = {
    '99acres': {
        'max_pages': 10
    },
    'magicbricks': {
        'max_pages': 100  # As per requirement
    },
    'sulekha': {
        'max_pages': 10
    }
}

# ============================================================================
# DATA PATHS
# ============================================================================

DATA_PATHS = {
    'raw': 'data/raw/',
    'cleaned': 'data/cleaned/',
    'training': 'data/training/'
}

# ============================================================================
# MODEL CONFIGURATION
# ============================================================================

MODEL_CONFIG = {
    'target': 'Price_Lakhs',
    'test_size': 0.2,
    'random_state': 42,
    'target_r2': 0.8,
    'target_rmse': 5.0  # In Lakhs
}

# ============================================================================
# LOCALITY TIER MAPPING (for encoding)
# ============================================================================

LOCALITY_TIERS = {
    'Tier 1': [
        "S G Highway", "Satellite", "Bopal", "Prahlad Nagar", "Vastrapur",
        "Bodakdev", "Thaltej", "Ambawadi", "Navrangpura", "C G Road",
        "New CG Road", "Gulbai Tekra", "Paldi", "Ellis Bridge"
    ],
    'Tier 2': [
        "Dholera", "Jagatpur", "Chandkheda", "Gota", "Vaishno Devi",
        "Shela", "South Bopal", "Naranpura", "Bavla", "Maninagar",
        "Vejalpur", "Noblenagar", "Ghatlodia", "Motera", "Memnagar",
        "Ranip", "Vastral", "Gurukul", "Nikol", "S P Ring Road",
        "Shilaj", "Vasna", "Chandlodia", "Science City", "Sabarmati",
        "Ghodasar", "Juhapura", "New Ranip", "Narol", "Jivrajpark",
        "Bapunagar", "Tragad", "Nava Wadaj", "Shyamal", "Gokuldham",
        "Sanand", "Vatva", "Ashram road", "Dholka", "Sola",
        "Ghuma", "Jodhpur", "Isanpur", "Shahibaug", "Thaltej Road",
        "Changodar", "Kankaria", "New Maninagar", "Saraspur", "Makarba",
        "Amraiwadi", "Odhav", "Palodia", "Sanand - Nalsarovar Road", "Nehrunagar"
    ]
    # All others are Tier 3
}
