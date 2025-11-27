"""
Simplified Data Preprocessing - Focus on Core Features Only
Extracts and cleans 7-10 most important features including Locality
No imputation unless absolutely necessary - drops incomplete rows
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime
import sys
sys.path.append('src')
from config import AHMEDABAD_LOCALITIES, NORMALIZED_LOCALITIES, LOCALITY_TIERS, DATA_PATHS

print("\n" + "="*70)
print("SIMPLIFIED DATA PREPROCESSING - CORE FEATURES ONLY")
print("="*70)
print("🎯 Goal: Extract 9 core features with verified data")
print("📍 Focus: Locality, Seller_Type, Under_Construction, Amenities")
print("📍 Removed: Bathrooms (correlated with BHK)")
print("="*70)

# ============================================================================
# LOAD RAW DATA
# ============================================================================

raw_file = 'data/raw/all_sources_detailed_' + datetime.now().strftime("%Y%m%d") + '.csv'

# Try today's file, if not found use latest
import glob
import os
raw_files = glob.glob('data/raw/all_sources_detailed_*.csv')
if not raw_files:
    print("❌ No raw data found! Please run scraper first.")
    sys.exit(1)

raw_file = max(raw_files, key=os.path.getctime)
print(f"\n📂 Loading: {raw_file}")

df = pd.read_csv(raw_file)
print(f"✅ Loaded {len(df)} raw records")

initial_count = len(df)

# ============================================================================
# STEP 1: EXTRACT LOCALITY (Most Important Feature)
# ============================================================================

print("\n" + "="*70)
print("STEP 1: LOCALITY EXTRACTION")
print("="*70)

def extract_locality(row):
    """
    Extract locality from title, description, locality field
    Matches against 150+ known Ahmedabad localities
    """
    # Combine all text fields for matching
    text_fields = []
    
    if pd.notna(row.get('Property_Title')):
        text_fields.append(str(row['Property_Title']))
    if pd.notna(row.get('Locality')):
        text_fields.append(str(row['Locality']))
    if pd.notna(row.get('Description')):
        text_fields.append(str(row['Description']))
    
    combined_text = ' '.join(text_fields).lower()
    
    # Try exact match first (case-insensitive)
    for locality in AHMEDABAD_LOCALITIES:
        if locality.lower() in combined_text:
            return locality
    
    # Try normalized match (remove spaces, hyphens)
    combined_normalized = combined_text.replace(" ", "").replace("-", "")
    for norm_key, locality in NORMALIZED_LOCALITIES.items():
        if norm_key in combined_normalized:
            return locality
    
    return None

print("🔍 Extracting localities from titles, descriptions, and locality fields...")
df['Locality_Extracted'] = df.apply(extract_locality, axis=1)

# Count how many localities found
found = df['Locality_Extracted'].notna().sum()
print(f"✅ Found locality for {found}/{len(df)} properties ({found/len(df)*100:.1f}%)")

# Drop rows without locality (critical feature)
df = df[df['Locality_Extracted'].notna()].copy()
print(f"🧹 Removed {initial_count - len(df)} rows without valid Ahmedabad locality")

# Filter localities: Mark as 'Unknown' if less than 3 properties
print(f"\n🔍 Filtering localities with insufficient data...")
locality_counts = df['Locality_Extracted'].value_counts()
localities_to_keep = locality_counts[locality_counts >= 3].index
localities_to_mark_unknown = locality_counts[locality_counts < 3].index

print(f"✅ Keeping {len(localities_to_keep)} localities with ≥3 properties")
print(f"⚠️  Marking {len(localities_to_mark_unknown)} localities with <3 properties as 'Unknown'")

# Mark localities with <3 properties as 'Unknown'
df.loc[df['Locality_Extracted'].isin(localities_to_mark_unknown), 'Locality_Extracted'] = 'Unknown'

if len(localities_to_mark_unknown) > 0:
    print(f"📊 Properties marked as Unknown: {df[df['Locality_Extracted'] == 'Unknown'].shape[0]}")

# ============================================================================
# STEP 2: CLEAN PRICE (Target Variable)
# ============================================================================

print("\n" + "="*70)
print("STEP 2: PRICE CLEANING")
print("="*70)

def clean_price(price_str):
    """Convert price to Lakhs (integers)"""
    if pd.isna(price_str):
        return None
    
    price_str = str(price_str).lower().replace(',', '').replace('₹', '').strip()
    
    # Extract number
    numbers = re.findall(r'[\d.]+', price_str)
    if not numbers:
        return None
    
    value = float(numbers[0])
    
    # Convert to Lakhs
    if 'crore' in price_str or 'cr' in price_str:
        return value * 100  # Crore to Lakhs
    elif 'lakh' in price_str or 'lac' in price_str or 'l' in price_str:
        return value
    elif value < 500:  # Assume Crores if < 500
        return value * 100
    else:  # Assume already in Lakhs
        return value

print("💰 Cleaning prices...")
df['Price_Lakhs'] = df['Price'].apply(clean_price)

# Drop rows without valid price
before = len(df)
df = df[df['Price_Lakhs'].notna()].copy()
df = df[df['Price_Lakhs'] > 0].copy()
print(f"✅ Converted {len(df)} prices to Lakhs")
print(f"🧹 Removed {before - len(df)} rows with invalid price")

# ============================================================================
# STEP 3: CLEAN AREA
# ============================================================================

print("\n" + "="*70)
print("STEP 3: AREA CLEANING")
print("="*70)

def clean_area(area_str):
    """Extract area in square feet"""
    if pd.isna(area_str):
        return None
    
    area_str = str(area_str).lower().replace(',', '').strip()
    
    # Extract number
    numbers = re.findall(r'[\d.]+', area_str)
    if not numbers:
        return None
    
    value = float(numbers[0])
    
    # Convert to sq ft if needed
    if 'sq.m' in area_str or 'sqm' in area_str:
        value = value * 10.764  # Convert sq.m to sq.ft
    
    # Validate range (200 - 10000 sq ft is reasonable)
    if 200 <= value <= 10000:
        return value
    return None

print("📏 Cleaning areas...")
df['Area_SqFt'] = df['Area_SqFt'].apply(clean_area)

# Drop rows without valid area
before = len(df)
df = df[df['Area_SqFt'].notna()].copy()
print(f"✅ Extracted {len(df)} valid areas")
print(f"🧹 Removed {before - len(df)} rows with invalid area")

# ============================================================================
# STEP 4: CLEAN BHK
# ============================================================================

print("\n" + "="*70)
print("STEP 4: BHK CLEANING")
print("="*70)

def clean_bhk(bhk_str):
    """Extract number of bedrooms"""
    if pd.isna(bhk_str):
        return None
    
    bhk_str = str(bhk_str).lower()
    
    # Extract number before 'bhk'
    match = re.search(r'(\d+)\s*bhk', bhk_str)
    if match:
        bhk = int(match.group(1))
        if 1 <= bhk <= 10:
            return bhk
    
    # Try just extracting first number
    numbers = re.findall(r'\d+', bhk_str)
    if numbers:
        bhk = int(numbers[0])
        if 1 <= bhk <= 10:
            return bhk
    
    return None

print("🛏️  Cleaning BHK...")
df['BHK'] = df['BHK'].apply(clean_bhk)

# Drop rows without valid BHK
before = len(df)
df = df[df['BHK'].notna()].copy()
print(f"✅ Extracted {len(df)} valid BHK values")
print(f"🧹 Removed {before - len(df)} rows with invalid BHK")

# ============================================================================
# STEP 5: CLEAN SELLER TYPE
# ============================================================================

print("\n" + "="*70)
print("STEP 5: SELLER TYPE CLEANING")
print("="*70)

def clean_seller_type(seller_str):
    """Standardize seller type"""
    if pd.isna(seller_str):
        return 'Unknown'
    
    seller_str = str(seller_str).strip().lower()
    
    if 'owner' in seller_str:
        return 'Owner'
    elif 'builder' in seller_str:
        return 'Builder'
    elif 'dealer' in seller_str:
        return 'Dealer'
    elif 'agent' in seller_str:
        return 'Agent'
    else:
        return 'Unknown'

print("👤 Cleaning seller types...")
df['Seller_Type'] = df['Seller_Type'].apply(clean_seller_type)
print(f"✅ Seller type distribution:")
print(df['Seller_Type'].value_counts())

# ============================================================================
# STEP 6: EXTRACT UNDER CONSTRUCTION STATUS
# ============================================================================

print("\n" + "="*70)
print("STEP 6: UNDER CONSTRUCTION STATUS EXTRACTION")
print("="*70)

def extract_under_construction(row):
    """Check if property is under construction from Raw_JSON and description"""
    text_to_check = []
    
    if pd.notna(row.get('Raw_JSON')):
        text_to_check.append(str(row['Raw_JSON']).lower())
    if pd.notna(row.get('Description')):
        text_to_check.append(str(row['Description']).lower())
    if pd.notna(row.get('Property_Title')):
        text_to_check.append(str(row['Property_Title']).lower())
    
    combined_text = ' '.join(text_to_check)
    
    # Check for under construction keywords
    under_construction_keywords = [
        'under construction', 'underconstruction', 'under-construction',
        'upcoming', 'new launch', 'pre-launch', 'construction status',
        'to be completed', 'possession date', 'ready by'
    ]
    
    for keyword in under_construction_keywords:
        if keyword in combined_text:
            return True
    
    # Check for ready to move (opposite)
    ready_keywords = ['ready to move', 'ready for possession', 'immediate possession']
    for keyword in ready_keywords:
        if keyword in combined_text:
            return False
    
    return False  # Default: assume ready

print("🏗️  Extracting construction status...")
df['Under_Construction'] = df.apply(extract_under_construction, axis=1)
under_construction_count = df['Under_Construction'].sum()
print(f"✅ Found {under_construction_count} properties under construction ({under_construction_count/len(df)*100:.1f}%)")
print(f"📊 Construction status distribution:")
print(df['Under_Construction'].value_counts())

# ============================================================================
# STEP 7: EXTRACT AMENITIES COUNT
# ============================================================================

print("\n" + "="*70)
print("STEP 7: AMENITIES EXTRACTION")
print("="*70)

def extract_amenities_count(row):
    """Count number of amenities from Raw_JSON and description"""
    text_to_check = []
    
    if pd.notna(row.get('Raw_JSON')):
        text_to_check.append(str(row['Raw_JSON']).lower())
    if pd.notna(row.get('Description')):
        text_to_check.append(str(row['Description']).lower())
    if pd.notna(row.get('Property_Title')):
        text_to_check.append(str(row['Property_Title']).lower())
    
    combined_text = ' '.join(text_to_check)
    
    # List of amenities to search for (avoiding duplicates)
    amenities_list = [
        'gymnasium', 'gym', 'swimming pool', 'pool', 'garden', 'park',
        'playground', 'club house', 'clubhouse', 'lift', 'elevator',
        'parking', 'car parking', 'security', '24x7 security', '24/7 security',
        'cctv', 'power backup', 'generator', 'children play area', 'kids play',
        'sports facility', 'indoor games', 'outdoor games', 'tennis court',
        'badminton court', 'jogging track', 'yoga', 'meditation', 'spa',
        'library', 'community hall', 'banquet hall', 'multipurpose hall',
        'rainwater harvesting', 'solar', 'intercom', 'fire safety',
        'vastu compliant', 'gated community', 'landscaping', 'senior citizen',
        'wifi', 'broadband', 'amphitheater', 'aerobics', 'cafeteria',
        'restaurant', 'shopping center', 'medical', 'hospital', 'atm'
    ]
    
    # Count unique amenities found (avoid counting same amenity multiple times)
    found_amenities = set()
    for amenity in amenities_list:
        if amenity in combined_text:
            # Group similar amenities
            if amenity in ['gym', 'gymnasium', 'fitness']:
                found_amenities.add('gym')
            elif amenity in ['swimming pool', 'pool']:
                found_amenities.add('pool')
            elif amenity in ['garden', 'park', 'landscaping']:
                found_amenities.add('garden')
            elif amenity in ['lift', 'elevator']:
                found_amenities.add('lift')
            elif amenity in ['parking', 'car parking']:
                found_amenities.add('parking')
            elif amenity in ['club house', 'clubhouse']:
                found_amenities.add('clubhouse')
            elif amenity in ['security', '24x7 security', '24/7 security', 'cctv']:
                found_amenities.add('security')
            elif amenity in ['power backup', 'generator']:
                found_amenities.add('power_backup')
            elif amenity in ['children play area', 'kids play', 'playground']:
                found_amenities.add('playground')
            else:
                found_amenities.add(amenity.replace(' ', '_'))
    
    return len(found_amenities)

print("🏢 Extracting amenities count...")
df['Amenities_Count'] = df.apply(extract_amenities_count, axis=1)
print(f"✅ Amenities statistics:")
print(f"   Mean: {df['Amenities_Count'].mean():.2f}")
print(f"   Median: {df['Amenities_Count'].median():.0f}")
print(f"   Range: {df['Amenities_Count'].min():.0f} - {df['Amenities_Count'].max():.0f}")
print(f"\n📊 Amenities distribution:")
print(df['Amenities_Count'].value_counts().sort_index().head(10))

# ============================================================================
# STEP 8: CLEAN PROPERTY TYPE
# ============================================================================

print("\n" + "="*70)
print("STEP 8: PROPERTY TYPE STANDARDIZATION")
print("="*70)

def clean_property_type(prop_type_str):
    """Standardize property types"""
    if pd.isna(prop_type_str):
        return 'Apartment'  # Default
    
    prop_type_str = str(prop_type_str).lower()
    
    if any(word in prop_type_str for word in ['apartment', 'flat']):
        return 'Apartment'
    elif any(word in prop_type_str for word in ['villa']):
        return 'Villa'
    elif any(word in prop_type_str for word in ['house', 'bungalow']):
        return 'Independent House'
    elif any(word in prop_type_str for word in ['plot', 'land']):
        return 'Plot'
    elif any(word in prop_type_str for word in ['penthouse']):
        return 'Penthouse'
    elif any(word in prop_type_str for word in ['studio']):
        return 'Studio'
    else:
        return 'Apartment'  # Default

print("🏠 Standardizing property types...")
df['Property_Type'] = df['Property_Type'].apply(clean_property_type)
print(f"✅ Property type distribution:")
print(df['Property_Type'].value_counts())

# ============================================================================
# STEP 9: CLEAN FURNISHING STATUS
# ============================================================================

print("\n" + "="*70)
print("STEP 9: FURNISHING STATUS STANDARDIZATION")
print("="*70)

def clean_furnishing(furnishing_str):
    """Standardize furnishing status"""
    if pd.isna(furnishing_str):
        return 'Unfurnished'  # Default
    
    furnishing_str = str(furnishing_str).lower()
    
    if any(word in furnishing_str for word in ['semi', 'semi-furnished']):
        return 'Semi-Furnished'
    elif any(word in furnishing_str for word in ['furnished', 'fully']):
        return 'Furnished'
    else:
        return 'Unfurnished'

print("🪑 Standardizing furnishing status...")
df['Furnishing_Status'] = df['Furnishing_Status'].apply(clean_furnishing)
print(f"✅ Furnishing distribution:")
print(df['Furnishing_Status'].value_counts())

# ============================================================================
# STEP 10: ADD DERIVED FEATURES
# ============================================================================

print("\n" + "="*70)
print("STEP 10: ADDING DERIVED FEATURES")
print("="*70)

# NO PRICE_PER_SQFT - removed as it's price-related!

# Locality Tier (will be encoded later)
def get_locality_tier(locality):
    """Assign tier based on locality"""
    if locality in LOCALITY_TIERS['Tier 1']:
        return 'Tier 1'
    elif locality in LOCALITY_TIERS['Tier 2']:
        return 'Tier 2'
    else:
        return 'Tier 3'

df['Locality_Tier'] = df['Locality_Extracted'].apply(get_locality_tier)
print("✅ Added: Locality_Tier (will be encoded in training)")

print(f"\n📊 Locality Tier distribution:")
print(df['Locality_Tier'].value_counts())

# ============================================================================
# STEP 11: REMOVE OUTLIERS
# ============================================================================

print("\n" + "="*70)
print("STEP 11: OUTLIER REMOVAL")
print("="*70)

# Remove extreme price outliers using IQR
Q1 = df['Price_Lakhs'].quantile(0.25)
Q3 = df['Price_Lakhs'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 3 * IQR
upper_bound = Q3 + 3 * IQR

before = len(df)
df = df[(df['Price_Lakhs'] >= lower_bound) & (df['Price_Lakhs'] <= upper_bound)].copy()
print(f"💰 Price outliers removed: {before - len(df)} (kept {lower_bound:.1f}L - {upper_bound:.1f}L)")

# Remove area outliers
before = len(df)
df = df[(df['Area_SqFt'] >= 200) & (df['Area_SqFt'] <= 10000)].copy()
print(f"📏 Area outliers removed: {before - len(df)} (kept 200-10000 sqft)")

# ============================================================================
# STEP 12: SELECT FINAL FEATURES AND SAVE
# ============================================================================

print("\n" + "="*70)
print("STEP 12: SAVING CLEANED DATA")
print("="*70)

# Select only core features (NO PRICE-RELATED FEATURES, NO BATHROOMS!)
final_columns = [
    'Price_Lakhs',
    'Area_SqFt', 
    'BHK',
    'Property_Type',
    'Furnishing_Status',
    'Locality_Extracted',
    'Locality_Tier',
    'Seller_Type',
    'Under_Construction',
    'Amenities_Count',
    'Source_Website'  # Keep for tracking
]

df_final = df[final_columns].copy()
df_final = df_final.rename(columns={'Locality_Extracted': 'Locality'})

# Sort by price
df_final = df_final.sort_values('Price_Lakhs', ascending=False).reset_index(drop=True)

# Save to cleaned folder
output_file = DATA_PATHS['cleaned'] + 'cleaned_data.csv'
df_final.to_csv(output_file, index=False)

print(f"\n✅ SUCCESS! Saved {len(df_final)} cleaned records")
print(f"📁 Output: {output_file}")

# ============================================================================
# DATA QUALITY REPORT
# ============================================================================

print("\n" + "="*70)
print("DATA QUALITY REPORT")
print("="*70)
print(f"📊 Total Properties: {len(df_final)}")
print(f"\n💰 Price (Lakhs):")
print(f"  Range: {df_final['Price_Lakhs'].min():.1f}L - {df_final['Price_Lakhs'].max():.1f}L")
print(f"  Mean: {df_final['Price_Lakhs'].mean():.1f}L")
print(f"  Median: {df_final['Price_Lakhs'].median():.1f}L")

print(f"\n📏 Area (SqFt):")
print(f"  Range: {df_final['Area_SqFt'].min():.0f} - {df_final['Area_SqFt'].max():.0f}")
print(f"  Mean: {df_final['Area_SqFt'].mean():.0f}")

print(f"\n🛏️  BHK Distribution:")
print(df_final['BHK'].value_counts().sort_index())

print(f"\n🏠 Property Types:")
print(df_final['Property_Type'].value_counts())

print(f"\n📍 Locality Tiers:")
print(df_final['Locality_Tier'].value_counts())

print(f"\n👤 Seller Types:")
print(df_final['Seller_Type'].value_counts())

print(f"\n🏗️  Construction Status:")
under_const = df_final['Under_Construction'].sum()
ready = len(df_final) - under_const
print(f"  Under Construction: {under_const} ({under_const/len(df_final)*100:.1f}%)")
print(f"  Ready to Move: {ready} ({ready/len(df_final)*100:.1f}%)")

print(f"\n🏢 Amenities Statistics:")
print(f"  Mean: {df_final['Amenities_Count'].mean():.2f} amenities/property")
print(f"  Median: {df_final['Amenities_Count'].median():.0f}")
print(f"  Range: {df_final['Amenities_Count'].min():.0f} - {df_final['Amenities_Count'].max():.0f}")

print(f"\n🔝 Top 10 Localities by Count:")
print(df_final['Locality'].value_counts().head(10))

print(f"\n💯 Data Completeness: 100% (no missing values in core features)")
print("="*70)
print(f"\n✅ Ready for ML training with 9 features (added Amenities_Count)!")
