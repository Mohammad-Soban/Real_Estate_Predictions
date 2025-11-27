"""
Enhanced Data Preprocessing with Price Bucketing & Feature Engineering
- Adds Price_Category (20 Lakhs buckets) as categorical feature
- Adds Area_Per_BHK, Locality-BHK interaction, Price-Tier patterns
- Removes price-related features from input (no data leakage)
- Keeps all existing features + new engineered features
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime
import sys
sys.path.append('src')
from config import AHMEDABAD_LOCALITIES, NORMALIZED_LOCALITIES, LOCALITY_TIERS, DATA_PATHS

print("\n" + "="*70)
print("ENHANCED DATA PREPROCESSING - BUCKETING & FEATURE ENGINEERING")
print("="*70)
print("🎯 Goal: Add Price Bucketing + Feature Engineering")
print("📊 New Features: Price_Category (20L buckets), Area_Per_BHK")
print("🚫 NO price-related features in model input!")
print("="*70)

# ============================================================================
# LOAD CLEANED DATA (from previous preprocessing)
# ============================================================================

print(f"\n📂 Loading: data/cleaned/cleaned_data.csv")
df = pd.read_csv('data/cleaned/cleaned_data.csv')
print(f"✅ Loaded {len(df)} records")

initial_count = len(df)

# Filter out Unknown localities (those with <3 properties from simple preprocessing)
if 'Unknown' in df['Locality'].values:
    unknown_count = (df['Locality'] == 'Unknown').sum()
    df = df[df['Locality'] != 'Unknown'].copy()
    print(f"🧹 Removed {unknown_count} properties from 'Unknown' localities (<3 properties)")
    print(f"✅ Remaining: {len(df)} properties from valid localities")

# ============================================================================
# STEP 1: CREATE PRICE BUCKETS (TARGET CATEGORIES)
# ============================================================================

print("\n" + "="*70)
print("STEP 1: PRICE BUCKETING (20 LAKHS BUCKETS)")
print("="*70)

# Get price range
min_price = df['Price_Lakhs'].min()
max_price = df['Price_Lakhs'].max()

print(f"💰 Price Range: {min_price:.2f}L - {max_price:.2f}L")

# Create buckets of 20 Lakhs starting from 0
bucket_size = 20
buckets = np.arange(0, max_price + bucket_size, bucket_size)
print(f"📊 Creating {len(buckets)-1} buckets with {bucket_size}L size")

# Create price categories
df['Price_Category'] = pd.cut(df['Price_Lakhs'], 
                               bins=buckets, 
                               labels=[f'{int(buckets[i])}-{int(buckets[i+1])}L' for i in range(len(buckets)-1)],
                               include_lowest=True)

print(f"✅ Price categories created!")
print(f"\n📊 Top 10 Price Categories:")
print(df['Price_Category'].value_counts().head(10))

# Calculate mean price per category (for analysis)
category_means = df.groupby('Price_Category')['Price_Lakhs'].agg(['mean', 'count']).sort_values('mean')
print(f"\n📈 Category Statistics (top 5 by volume):")
print(category_means.nlargest(5, 'count'))

# ============================================================================
# STEP 2: FEATURE ENGINEERING (NO PRICE LEAKAGE!)
# ============================================================================

print("\n" + "="*70)
print("STEP 2: FEATURE ENGINEERING")
print("="*70)

# 1. Area per BHK (useful proxy for room size)
df['Area_Per_BHK'] = df['Area_SqFt'] / df['BHK']
print(f"✅ Added: Area_Per_BHK (Range: {df['Area_Per_BHK'].min():.0f} - {df['Area_Per_BHK'].max():.0f})")

# 2. Is_Large_Apartment (BHK >= 4)
df['Is_Large_Apartment'] = (df['BHK'] >= 4).astype(int)
print(f"✅ Added: Is_Large_Apartment ({df['Is_Large_Apartment'].sum()} properties, {df['Is_Large_Apartment'].sum()/len(df)*100:.1f}%)")

# 3. Is_Premium_Locality (Tier 1)
df['Is_Premium_Locality'] = (df['Locality_Tier'] == 'Tier 1').astype(int)
print(f"✅ Added: Is_Premium_Locality ({df['Is_Premium_Locality'].sum()} properties, {df['Is_Premium_Locality'].sum()/len(df)*100:.1f}%)")

# 4. Is_Budget_Locality (Tier 3)
df['Is_Budget_Locality'] = (df['Locality_Tier'] == 'Tier 3').astype(int)
print(f"✅ Added: Is_Budget_Locality ({df['Is_Budget_Locality'].sum()} properties, {df['Is_Budget_Locality'].sum()/len(df)*100:.1f}%)")

# 5. BHK_Area_Interaction (categorical interaction)
df['BHK_Area_Category'] = pd.cut(df['Area_SqFt'], bins=[0, 800, 1500, 3000, 10000], 
                                  labels=['Small', 'Medium', 'Large', 'XLarge'])
df['BHK_Area_Combo'] = df['BHK'].astype(str) + '_' + df['BHK_Area_Category'].astype(str)
print(f"✅ Added: BHK_Area_Combo ({df['BHK_Area_Combo'].nunique()} unique combinations)")

# 6. High Amenity Property
df['High_Amenity'] = (df['Amenities_Count'] >= 3).astype(int)
print(f"✅ Added: High_Amenity ({df['High_Amenity'].sum()} properties, {df['High_Amenity'].sum()/len(df)*100:.1f}%)")

# 7. Property Age Category (Under_Construction vs Ready)
df['Construction_Category'] = df['Under_Construction'].apply(lambda x: 'Under_Construction' if x else 'Ready_To_Move')
print(f"✅ Added: Construction_Category")

# ============================================================================
# STEP 3: STATISTICAL FEATURES (LOCALITY-BASED, NO PRICE!)
# ============================================================================

print("\n" + "="*70)
print("STEP 3: LOCALITY-BASED STATISTICAL FEATURES")
print("="*70)

# Count of properties in each locality (popularity metric)
locality_counts = df['Locality'].value_counts()
df['Locality_Property_Count'] = df['Locality'].map(locality_counts)
print(f"✅ Added: Locality_Property_Count (Range: {df['Locality_Property_Count'].min()} - {df['Locality_Property_Count'].max()})")

# Median area in each locality (area patterns - more robust to outliers)
locality_median_area = df.groupby('Locality')['Area_SqFt'].median()
df['Locality_Median_Area'] = df['Locality'].map(locality_median_area)
print(f"✅ Added: Locality_Median_Area (Range: {df['Locality_Median_Area'].min():.0f} - {df['Locality_Median_Area'].max():.0f})")

# Most common BHK in locality
locality_mode_bhk = df.groupby('Locality')['BHK'].agg(lambda x: x.mode()[0] if len(x.mode()) > 0 else x.median())
df['Locality_Common_BHK'] = df['Locality'].map(locality_mode_bhk)
print(f"✅ Added: Locality_Common_BHK")

# Median price in each locality (target variable pattern - for reference only, NOT used in training)
locality_median_price = df.groupby('Locality')['Price_Lakhs'].median()
df['Locality_Median_Price'] = df['Locality'].map(locality_median_price)
print(f"✅ Added: Locality_Median_Price (Range: {df['Locality_Median_Price'].min():.1f}L - {df['Locality_Median_Price'].max():.1f}L)")
print(f"⚠️  Note: Locality_Median_Price is for analysis only, NOT used in model training (price leakage risk)")

# ============================================================================
# STEP 4: VERIFY NO PRICE LEAKAGE IN FEATURES
# ============================================================================

print("\n" + "="*70)
print("STEP 4: VERIFY NO PRICE LEAKAGE")
print("="*70)

# List all features (exclude target and metadata)
feature_columns = [col for col in df.columns if col not in ['Price_Lakhs', 'Price_Category', 'Source_Website', 'BHK_Area_Category']]
print(f"📊 Total Features: {len(feature_columns)}")
print(f"✅ Features: {feature_columns}")

# Check for price-related keywords
price_related = [col for col in feature_columns if 'price' in col.lower() or 'cost' in col.lower()]
if price_related:
    print(f"⚠️  WARNING: Possible price-related features: {price_related}")
else:
    print(f"✅ NO price-related features detected!")

# ============================================================================
# STEP 5: SAVE ENHANCED DATA
# ============================================================================

print("\n" + "="*70)
print("STEP 5: SAVING ENHANCED DATA")
print("="*70)

# Select final columns
final_columns = [
    # Target
    'Price_Lakhs',
    'Price_Category',
    
    # Original Core Features
    'Area_SqFt', 
    'BHK',
    'Property_Type',
    'Furnishing_Status',
    'Locality',
    'Locality_Tier',
    'Seller_Type',
    'Under_Construction',
    'Amenities_Count',
    
    # New Engineered Features
    'Area_Per_BHK',
    'Is_Large_Apartment',
    'Is_Premium_Locality',
    'Is_Budget_Locality',
    'BHK_Area_Combo',
    'High_Amenity',
    'Construction_Category',
    'Locality_Property_Count',
    'Locality_Median_Area',
    'Locality_Common_BHK',
    'Locality_Median_Price',  # For reference/analysis only
    
    # Metadata
    'Source_Website'
]

df_final = df[final_columns].copy()

# Sort by price
df_final = df_final.sort_values('Price_Lakhs', ascending=False).reset_index(drop=True)

# Save
output_file = 'data/training/training_data_enhanced.csv'
df_final.to_csv(output_file, index=False)

print(f"\n✅ SUCCESS! Saved {len(df_final)} enhanced records")
print(f"📁 Output: {output_file}")

# ============================================================================
# ENHANCED DATA QUALITY REPORT
# ============================================================================

print("\n" + "="*70)
print("ENHANCED DATA QUALITY REPORT")
print("="*70)
print(f"📊 Total Properties: {len(df_final)}")

print(f"\n💰 Price Statistics:")
print(f"  Range: {df_final['Price_Lakhs'].min():.1f}L - {df_final['Price_Lakhs'].max():.1f}L")
print(f"  Mean: {df_final['Price_Lakhs'].mean():.1f}L")
print(f"  Median: {df_final['Price_Lakhs'].median():.1f}L")
print(f"  Price Categories: {df_final['Price_Category'].nunique()} buckets")

print(f"\n📏 Area Statistics:")
print(f"  Range: {df_final['Area_SqFt'].min():.0f} - {df_final['Area_SqFt'].max():.0f} sqft")
print(f"  Area per BHK: {df_final['Area_Per_BHK'].mean():.0f} sqft/BHK (avg)")

print(f"\n🏠 Feature Summary:")
print(f"  Original Features: 9")
print(f"  New Features: 10")
print(f"  Total Features: 19 (+ 1 target + 1 Price_Category)")
print(f"  Localities: {df_final['Locality'].nunique()} unique")
print(f"  BHK-Area Combinations: {df_final['BHK_Area_Combo'].nunique()} unique")

print(f"\n📊 New Feature Statistics:")
print(f"  Large Apartments (BHK≥4): {df_final['Is_Large_Apartment'].sum()} ({df_final['Is_Large_Apartment'].sum()/len(df_final)*100:.1f}%)")
print(f"  Premium Localities (Tier 1): {df_final['Is_Premium_Locality'].sum()} ({df_final['Is_Premium_Locality'].sum()/len(df_final)*100:.1f}%)")
print(f"  High Amenity (≥3): {df_final['High_Amenity'].sum()} ({df_final['High_Amenity'].sum()/len(df_final)*100:.1f}%)")
print(f"  Under Construction: {df_final['Under_Construction'].sum()} ({df_final['Under_Construction'].sum()/len(df_final)*100:.1f}%)")

print(f"\n🔝 Top 5 Localities by Property Count:")
print(df_final['Locality'].value_counts().head())

print(f"\n💯 Data Completeness: {df_final.isnull().sum().sum() / (len(df_final) * len(df_final.columns)) * 100:.2f}% missing")

print("\n" + "="*70)
print("✅ Ready for Enhanced ML Training!")
print("📌 Use Price_Category for classification OR Price_Lakhs for regression")
print("📌 19 features (NO price leakage!)")
print("="*70)
