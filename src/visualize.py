"""
COMPREHENSIVE DATA VISUALIZATIONS (20 Charts)
No price-related features, proper locality encoding focus
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
sys.path.append('.')
from src.config import DATA_PATHS
import warnings
warnings.filterwarnings('ignore')

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

print("\n" + "="*80)
print(" "*20 + "COMPREHENSIVE DATA VISUALIZATIONS")
print(" "*28 + "(21 DETAILED CHARTS)")
print("="*80)

os.makedirs('visualizations', exist_ok=True)

print("\n📂 Loading cleaned data...")
try:
    df = pd.read_csv(DATA_PATHS['cleaned'] + 'cleaned_data.csv')
    print(f"✅ Loaded {len(df)} properties")
    
    # Filter out 'Unknown' localities (those with <3 properties)
    if 'Unknown' in df['Locality'].values:
        unknown_count = (df['Locality'] == 'Unknown').sum()
        df = df[df['Locality'] != 'Unknown'].copy()
        print(f"🧹 Excluded {unknown_count} properties from 'Unknown' localities (<3 properties)")
        print(f"📊 Visualizing {len(df)} properties from valid localities")
except:
    print("❌ No cleaned data found! Run preprocessing first.")
    sys.exit(1)

viz_count = 0

print("\n" + "="*80)
print("Creating 21 comprehensive visualizations...")
print("="*80)

# 1. LOCALITY PROPERTY COUNT (TOP 30)
print(f"  {viz_count+1}. Creating Locality Property Count...")
plt.figure(figsize=(16, 8))
locality_counts = df['Locality'].value_counts().head(30)
colors = plt.cm.viridis(np.linspace(0, 1, len(locality_counts)))
locality_counts.plot(kind='barh', color=colors)
plt.title('Top 30 Localities by Property Count', fontsize=16, fontweight='bold')
plt.xlabel('Number of Properties', fontsize=12)
plt.ylabel('Locality', fontsize=12)
plt.gca().invert_yaxis()
for i, v in enumerate(locality_counts.values):
    plt.text(v + 2, i, str(v), va='center', fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/01_locality_property_count.png', dpi=300, bbox_inches='tight')
plt.close()
viz_count += 1

# 2. LOCALITY AVERAGE PRICE (TOP 30)
print(f"  {viz_count+1}. Creating Locality Average Price...")
plt.figure(figsize=(16, 8))
locality_avg_price = df.groupby('Locality')['Price_Lakhs'].mean().sort_values(ascending=False).head(30)
colors = plt.cm.coolwarm(np.linspace(0, 1, len(locality_avg_price)))
locality_avg_price.plot(kind='barh', color=colors)
plt.title('Top 30 Localities by Average Price', fontsize=16, fontweight='bold')
plt.xlabel('Average Price (Lakhs)', fontsize=12)
plt.ylabel('Locality', fontsize=12)
plt.gca().invert_yaxis()
for i, v in enumerate(locality_avg_price.values):
    plt.text(v + 2, i, f'₹{v:.1f}L', va='center', fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/02_locality_avg_price.png', dpi=300, bbox_inches='tight')
plt.close()
viz_count += 1

# 3. LOCALITY TIER DISTRIBUTION
print(f"  {viz_count+1}. Creating Locality Tier Distribution...")
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
tier_counts = df['Locality_Tier'].value_counts()
colors_tier = ['#FF6B6B', '#4ECDC4', '#45B7D1']
axes[0].pie(tier_counts, labels=tier_counts.index, autopct='%1.1f%%', startangle=90, colors=colors_tier)
axes[0].set_title('Locality Tier Distribution (Pie)', fontsize=14, fontweight='bold')
tier_counts.plot(kind='bar', ax=axes[1], color=colors_tier)
axes[1].set_title('Locality Tier Distribution (Bar)', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Tier', fontsize=12)
axes[1].set_ylabel('Count', fontsize=12)
axes[1].tick_params(axis='x', rotation=0)
for i, v in enumerate(tier_counts.values):
    axes[1].text(i, v + 20, str(v), ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/03_locality_tier_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
viz_count += 1

# 4. BHK COMPREHENSIVE ANALYSIS
print(f"  {viz_count+1}. Creating BHK Comprehensive Analysis...")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
df['BHK'].value_counts().sort_index().plot(kind='bar', ax=axes[0,0], color='skyblue')
axes[0,0].set_title('BHK Distribution', fontsize=14, fontweight='bold')
axes[0,0].set_xlabel('BHK', fontsize=12)
axes[0,0].set_ylabel('Count', fontsize=12)
df.groupby('BHK')['Price_Lakhs'].mean().plot(kind='line', ax=axes[0,1], marker='o', color='green', linewidth=2)
axes[0,1].set_title('Average Price by BHK', fontsize=14, fontweight='bold')
axes[0,1].set_xlabel('BHK', fontsize=12)
axes[0,1].set_ylabel('Price (Lakhs)', fontsize=12)
axes[0,1].grid(True, alpha=0.3)
df.boxplot(column='Price_Lakhs', by='BHK', ax=axes[1,0])
axes[1,0].set_title('Price Distribution by BHK (Box Plot)', fontsize=14, fontweight='bold')
axes[1,0].set_xlabel('BHK', fontsize=12)
axes[1,0].set_ylabel('Price (Lakhs)', fontsize=12)
plt.sca(axes[1,0])
plt.xticks(rotation=0)
df.groupby('BHK')['Area_SqFt'].mean().plot(kind='bar', ax=axes[1,1], color='orange')
axes[1,1].set_title('Average Area by BHK', fontsize=14, fontweight='bold')
axes[1,1].set_xlabel('BHK', fontsize=12)
axes[1,1].set_ylabel('Area (SqFt)', fontsize=12)
plt.tight_layout()
plt.savefig('visualizations/04_bhk_comprehensive_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
viz_count += 1

# 5. SELLER TYPE ANALYSIS
print(f"  {viz_count+1}. Creating Seller Type Analysis...")
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
seller_counts = df['Seller_Type'].value_counts()
colors_seller = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
seller_counts.plot(kind='bar', ax=axes[0], color=colors_seller[:len(seller_counts)])
axes[0].set_title('Seller Type Distribution', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Seller Type', fontsize=12)
axes[0].set_ylabel('Count', fontsize=12)
axes[0].tick_params(axis='x', rotation=45)
for i, v in enumerate(seller_counts.values):
    axes[0].text(i, v + 20, str(v), ha='center', fontweight='bold')
df.groupby('Seller_Type')['Price_Lakhs'].mean().sort_values(ascending=False).plot(kind='bar', ax=axes[1], color=colors_seller[:len(seller_counts)])
axes[1].set_title('Average Price by Seller Type', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Seller Type', fontsize=12)
axes[1].set_ylabel('Price (Lakhs)', fontsize=12)
axes[1].tick_params(axis='x', rotation=45)
plt.tight_layout()
plt.savefig('visualizations/05_seller_type_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
viz_count += 1

# 6. UNDER CONSTRUCTION ANALYSIS
print(f"  {viz_count+1}. Creating Under Construction Analysis...")
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
construction_counts = df['Under_Construction'].value_counts()
construction_labels = ['Ready to Move', 'Under Construction']
colors_const = ['#66BB6A', '#FFA726']
axes[0].pie(construction_counts.values, labels=construction_labels, autopct='%1.1f%%', startangle=90, colors=colors_const)
axes[0].set_title('Construction Status Distribution', fontsize=14, fontweight='bold')
construction_prices = df.groupby('Under_Construction')['Price_Lakhs'].mean()
axes[1].bar(['Ready to Move', 'Under Construction'], construction_prices.values, color=colors_const)
axes[1].set_title('Average Price by Construction Status', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Price (Lakhs)', fontsize=12)
for i, v in enumerate(construction_prices.values):
    axes[1].text(i, v + 2, f'₹{v:.1f}L', ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/06_under_construction_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
viz_count += 1

# 7. PROPERTY TYPE DISTRIBUTION
print(f"  {viz_count+1}. Creating Property Type Distribution...")
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
prop_counts = df['Property_Type'].value_counts()
colors_prop = ['#FF9999', '#66B2FF']
axes[0].pie(prop_counts, labels=prop_counts.index, autopct='%1.1f%%', startangle=90, colors=colors_prop)
axes[0].set_title('Property Type Distribution (Pie)', fontsize=14, fontweight='bold')
prop_counts.plot(kind='bar', ax=axes[1], color=colors_prop)
axes[1].set_title('Property Type Distribution (Bar)', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Property Type', fontsize=12)
axes[1].set_ylabel('Count', fontsize=12)
axes[1].tick_params(axis='x', rotation=45)
for i, v in enumerate(prop_counts.values):
    axes[1].text(i, v + 20, str(v), ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/07_property_type_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
viz_count += 1

# 8. PROPERTY TYPE AVERAGE PRICE
print(f"  {viz_count+1}. Creating Property Type Average Price...")
plt.figure(figsize=(12, 6))
df.groupby('Property_Type')['Price_Lakhs'].mean().plot(kind='bar', color=['#FF6B6B', '#4ECDC4'])
plt.title('Average Price by Property Type', fontsize=16, fontweight='bold')
plt.xlabel('Property Type', fontsize=12)
plt.ylabel('Average Price (Lakhs)', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('visualizations/08_property_type_avg_price.png', dpi=300, bbox_inches='tight')
plt.close()
viz_count += 1

# 9. FURNISHING DISTRIBUTION
print(f"  {viz_count+1}. Creating Furnishing Distribution...")
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
furn_counts = df['Furnishing_Status'].value_counts()
colors_furn = ['#FFB6C1', '#98D8C8', '#F7DC6F']
explode = (0.05, 0, 0)
axes[0].pie(furn_counts, labels=furn_counts.index, autopct='%1.1f%%', startangle=90, colors=colors_furn, explode=explode)
axes[0].set_title('Furnishing Status Distribution (Pie)', fontsize=14, fontweight='bold')
furn_counts.plot(kind='bar', ax=axes[1], color=colors_furn)
axes[1].set_title('Furnishing Status Distribution (Bar)', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Furnishing Status', fontsize=12)
axes[1].set_ylabel('Count', fontsize=12)
axes[1].tick_params(axis='x', rotation=45)
for i, v in enumerate(furn_counts.values):
    axes[1].text(i, v + 20, str(v), ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/09_furnishing_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
viz_count += 1

# 10. FURNISHING PRICING ANALYSIS
print(f"  {viz_count+1}. Creating Furnishing Pricing Analysis...")
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
furn_price = df.groupby('Furnishing_Status')['Price_Lakhs'].agg(['mean', 'median'])
furn_price.plot(kind='bar', ax=axes[0], color=['#FF6B6B', '#4ECDC4'])
axes[0].set_title('Average and Median Price by Furnishing', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Furnishing Status', fontsize=12)
axes[0].set_ylabel('Price (Lakhs)', fontsize=12)
axes[0].tick_params(axis='x', rotation=45)
axes[0].legend(['Mean', 'Median'])
df.boxplot(column='Price_Lakhs', by='Furnishing_Status', ax=axes[1])
axes[1].set_title('Price Distribution by Furnishing (Box Plot)', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Furnishing Status', fontsize=12)
axes[1].set_ylabel('Price (Lakhs)', fontsize=12)
plt.sca(axes[1])
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('visualizations/10_furnishing_pricing.png', dpi=300, bbox_inches='tight')
plt.close()
viz_count += 1

# 11. AREA DISTRIBUTION COMPREHENSIVE
print(f"  {viz_count+1}. Creating Area Distribution Analysis...")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
axes[0,0].hist(df['Area_SqFt'], bins=50, color='teal', alpha=0.7, edgecolor='black')
axes[0,0].set_title('Area Distribution (Histogram)', fontsize=14, fontweight='bold')
axes[0,0].set_xlabel('Area (SqFt)', fontsize=12)
axes[0,0].set_ylabel('Frequency', fontsize=12)
axes[0,0].axvline(df['Area_SqFt'].mean(), color='red', linestyle='--', linewidth=2, label='Mean')
axes[0,0].axvline(df['Area_SqFt'].median(), color='green', linestyle='--', linewidth=2, label='Median')
axes[0,0].legend()
df.boxplot(column='Area_SqFt', ax=axes[0,1])
axes[0,1].set_title('Area Distribution (Box Plot)', fontsize=14, fontweight='bold')
axes[0,1].set_ylabel('Area (SqFt)', fontsize=12)
parts = axes[1,0].violinplot([df['Area_SqFt'].values], positions=[0], showmeans=True, showmedians=True)
axes[1,0].set_title('Area Distribution (Violin Plot)', fontsize=14, fontweight='bold')
axes[1,0].set_ylabel('Area (SqFt)', fontsize=12)
axes[1,0].set_xticks([])
df.groupby('Property_Type')['Area_SqFt'].mean().plot(kind='bar', ax=axes[1,1], color='coral')
axes[1,1].set_title('Average Area by Property Type', fontsize=14, fontweight='bold')
axes[1,1].set_xlabel('Property Type', fontsize=12)
axes[1,1].set_ylabel('Area (SqFt)', fontsize=12)
axes[1,1].tick_params(axis='x', rotation=45)
plt.tight_layout()
plt.savefig('visualizations/11_area_distribution_comprehensive.png', dpi=300, bbox_inches='tight')
plt.close()
viz_count += 1

# 12. PRICE DISTRIBUTION COMPREHENSIVE
print(f"  {viz_count+1}. Creating Price Distribution Analysis...")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
axes[0,0].hist(df['Price_Lakhs'], bins=50, color='gold', alpha=0.7, edgecolor='black')
axes[0,0].set_title('Price Distribution (Histogram)', fontsize=14, fontweight='bold')
axes[0,0].set_xlabel('Price (Lakhs)', fontsize=12)
axes[0,0].set_ylabel('Frequency', fontsize=12)
axes[0,0].axvline(df['Price_Lakhs'].mean(), color='red', linestyle='--', linewidth=2, label='Mean')
axes[0,0].axvline(df['Price_Lakhs'].median(), color='green', linestyle='--', linewidth=2, label='Median')
axes[0,0].legend()
df.boxplot(column='Price_Lakhs', ax=axes[0,1])
axes[0,1].set_title('Price Distribution (Box Plot)', fontsize=14, fontweight='bold')
axes[0,1].set_ylabel('Price (Lakhs)', fontsize=12)
df.boxplot(column='Price_Lakhs', by='Locality_Tier', ax=axes[1,0])
axes[1,0].set_title('Price Distribution by Tier', fontsize=14, fontweight='bold')
axes[1,0].set_xlabel('Locality Tier', fontsize=12)
axes[1,0].set_ylabel('Price (Lakhs)', fontsize=12)
plt.sca(axes[1,0])
plt.xticks(rotation=0)
sorted_prices = np.sort(df['Price_Lakhs'].values)
cumulative = np.arange(1, len(sorted_prices) + 1) / len(sorted_prices)
axes[1,1].plot(sorted_prices, cumulative, linewidth=2, color='blue')
axes[1,1].set_title('Cumulative Price Distribution', fontsize=14, fontweight='bold')
axes[1,1].set_xlabel('Price (Lakhs)', fontsize=12)
axes[1,1].set_ylabel('Cumulative Probability', fontsize=12)
axes[1,1].grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('visualizations/12_price_distribution_comprehensive.png', dpi=300, bbox_inches='tight')
plt.close()
viz_count += 1

# 13. PRICE VS AREA SCATTER (BY BHK)
print(f"  {viz_count+1}. Creating Price vs Area Scatter (by BHK)...")
plt.figure(figsize=(14, 8))
bhk_values = sorted(df['BHK'].unique())
colors = plt.cm.rainbow(np.linspace(0, 1, len(bhk_values)))
for bhk, color in zip(bhk_values, colors):
    bhk_data = df[df['BHK'] == bhk]
    plt.scatter(bhk_data['Area_SqFt'], bhk_data['Price_Lakhs'], alpha=0.6, s=50, c=[color], label=f'{int(bhk)} BHK')
plt.title('Price vs Area (Colored by BHK)', fontsize=16, fontweight='bold')
plt.xlabel('Area (SqFt)', fontsize=12)
plt.ylabel('Price (Lakhs)', fontsize=12)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('visualizations/13_price_vs_area_by_bhk.png', dpi=300, bbox_inches='tight')
plt.close()
viz_count += 1

# 14. PRICE VS AREA SCATTER (BY PROPERTY TYPE)
print(f"  {viz_count+1}. Creating Price vs Area Scatter (by Property Type)...")
plt.figure(figsize=(14, 8))
prop_types = df['Property_Type'].unique()
colors_prop_scatter = ['#FF6B6B', '#4ECDC4']
for prop_type, color in zip(prop_types, colors_prop_scatter):
    prop_data = df[df['Property_Type'] == prop_type]
    plt.scatter(prop_data['Area_SqFt'], prop_data['Price_Lakhs'], alpha=0.6, s=50, c=color, label=prop_type)
plt.title('Price vs Area (Colored by Property Type)', fontsize=16, fontweight='bold')
plt.xlabel('Area (SqFt)', fontsize=12)
plt.ylabel('Price (Lakhs)', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('visualizations/14_price_vs_area_by_property_type.png', dpi=300, bbox_inches='tight')
plt.close()
viz_count += 1

# 15. CORRELATION HEATMAP (NUMERIC FEATURES ONLY)
print(f"  {viz_count+1}. Creating Correlation Heatmap...")
plt.figure(figsize=(10, 8))
numeric_cols = ['Price_Lakhs', 'Area_SqFt', 'BHK']
corr_matrix = df[numeric_cols].corr()
sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm', center=0, square=True, linewidths=1)
plt.title('Correlation Heatmap (Numeric Features)', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/15_correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()
viz_count += 1

# 16. TIER-WISE PRICE COMPARISON
print(f"  {viz_count+1}. Creating Tier-wise Price Comparison...")
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
tier_price = df.groupby('Locality_Tier')['Price_Lakhs'].agg(['mean', 'median', 'std'])
tier_price[['mean', 'median']].plot(kind='bar', ax=axes[0], color=['#FF6B6B', '#4ECDC4'])
axes[0].set_title('Mean and Median Price by Tier', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Locality Tier', fontsize=12)
axes[0].set_ylabel('Price (Lakhs)', fontsize=12)
axes[0].tick_params(axis='x', rotation=0)
axes[0].legend(['Mean', 'Median'])
df.groupby('Locality_Tier')['Price_Lakhs'].apply(list).apply(lambda x: axes[1].violinplot([x], positions=[df['Locality_Tier'].unique().tolist().index(df[df['Price_Lakhs'].isin(x)]['Locality_Tier'].iloc[0])], showmeans=True))
axes[1].set_title('Price Distribution by Tier (Violin)', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Locality Tier', fontsize=12)
axes[1].set_ylabel('Price (Lakhs)', fontsize=12)
axes[1].set_xticks(range(len(df['Locality_Tier'].unique())))
axes[1].set_xticklabels(sorted(df['Locality_Tier'].unique()))
plt.tight_layout()
plt.savefig('visualizations/16_tier_price_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
viz_count += 1

# 17. SELLER TYPE VS PROPERTY TYPE HEATMAP
print(f"  {viz_count+1}. Creating Seller Type vs Property Type Heatmap...")
plt.figure(figsize=(12, 6))
seller_prop = df.groupby(['Seller_Type', 'Property_Type']).size().reset_index(name='count')
pivot_seller_prop = seller_prop.pivot(index='Seller_Type', columns='Property_Type', values='count').fillna(0)
sns.heatmap(pivot_seller_prop, annot=True, fmt='.0f', cmap='RdYlGn', cbar_kws={'label': 'Property Count'})
plt.title('Seller Type vs Property Type Heatmap', fontsize=16, fontweight='bold')
plt.xlabel('Property Type', fontsize=12)
plt.ylabel('Seller Type', fontsize=12)
plt.tight_layout()
plt.savefig('visualizations/17_seller_type_vs_property_type.png', dpi=300, bbox_inches='tight')
plt.close()
viz_count += 1

# 18. TOP 20 LOCALITIES COMPARISON
print(f"  {viz_count+1}. Creating Top 20 Localities Comparison...")
fig, axes = plt.subplots(2, 1, figsize=(16, 12))
top_20_localities = df['Locality'].value_counts().head(20).index
top_20_data = df[df['Locality'].isin(top_20_localities)]
locality_stats = top_20_data.groupby('Locality').agg({'Price_Lakhs': 'mean', 'Area_SqFt': 'mean'}).sort_values('Price_Lakhs', ascending=False)
locality_stats['Price_Lakhs'].plot(kind='barh', ax=axes[0], color='coral')
axes[0].set_title('Top 20 Localities - Average Price', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Average Price (Lakhs)', fontsize=12)
axes[0].set_ylabel('Locality', fontsize=12)
axes[0].invert_yaxis()
locality_stats_area = locality_stats.sort_values('Area_SqFt', ascending=False)
locality_stats_area['Area_SqFt'].plot(kind='barh', ax=axes[1], color='skyblue')
axes[1].set_title('Top 20 Localities - Average Area', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Average Area (SqFt)', fontsize=12)
axes[1].set_ylabel('Locality', fontsize=12)
axes[1].invert_yaxis()
plt.tight_layout()
plt.savefig('visualizations/18_top_20_localities_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
viz_count += 1

# 19. FURNISHING VS PROPERTY TYPE HEATMAP
print(f"  {viz_count+1}. Creating Furnishing vs Property Type Heatmap...")
plt.figure(figsize=(10, 6))
furn_prop = df.groupby(['Furnishing_Status', 'Property_Type']).size().reset_index(name='count')
pivot_furn_prop = furn_prop.pivot(index='Furnishing_Status', columns='Property_Type', values='count').fillna(0)
sns.heatmap(pivot_furn_prop, annot=True, fmt='.0f', cmap='Blues', cbar_kws={'label': 'Property Count'})
plt.title('Furnishing Status vs Property Type Heatmap', fontsize=16, fontweight='bold')
plt.xlabel('Property Type', fontsize=12)
plt.ylabel('Furnishing Status', fontsize=12)
plt.tight_layout()
plt.savefig('visualizations/19_furnishing_vs_property_type.png', dpi=300, bbox_inches='tight')
plt.close()
viz_count += 1

# 20. TIER VS BHK DISTRIBUTION
print(f"  {viz_count+1}. Creating Tier vs BHK Distribution...")
plt.figure(figsize=(12, 8))
tier_bhk = df.groupby(['Locality_Tier', 'BHK']).size().reset_index(name='count')
pivot_tier_bhk = tier_bhk.pivot(index='Locality_Tier', columns='BHK', values='count').fillna(0)
pivot_tier_bhk.plot(kind='bar', stacked=True, colormap='Set3', figsize=(12, 8))
plt.title('Locality Tier vs BHK Distribution (Stacked)', fontsize=16, fontweight='bold')
plt.xlabel('Locality Tier', fontsize=12)
plt.ylabel('Property Count', fontsize=12)
plt.xticks(rotation=0)
plt.legend(title='BHK', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('visualizations/20_tier_vs_bhk_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
viz_count += 1

# 21. COMPREHENSIVE SUMMARY DASHBOARD
print(f"  {viz_count+1}. Creating Comprehensive Summary Dashboard...")
fig = plt.figure(figsize=(20, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# Summary statistics
ax1 = fig.add_subplot(gs[0, :])
ax1.axis('off')
summary_text = f"""
PROPERTY MARKET SUMMARY - AHMEDABAD

Total Properties: {len(df):,} | Unique Localities: {df['Locality'].nunique()} | Property Types: {df['Property_Type'].nunique()}

PRICE STATISTICS:
  Mean: ₹{df['Price_Lakhs'].mean():.2f}L | Median: ₹{df['Price_Lakhs'].median():.2f}L | Min: ₹{df['Price_Lakhs'].min():.2f}L | Max: ₹{df['Price_Lakhs'].max():.2f}L

AREA STATISTICS:
  Mean: {df['Area_SqFt'].mean():.0f} sqft | Median: {df['Area_SqFt'].median():.0f} sqft | Min: {df['Area_SqFt'].min():.0f} sqft | Max: {df['Area_SqFt'].max():.0f} sqft

CONFIGURATION:
  Most Common BHK: {df['BHK'].mode().values[0]:.0f} ({(df['BHK'].value_counts().iloc[0]/len(df)*100):.1f}%)
  Most Common Property Type: {df['Property_Type'].mode().values[0]} ({(df['Property_Type'].value_counts().iloc[0]/len(df)*100):.1f}%)
  Most Common Furnishing: {df['Furnishing_Status'].mode().values[0]} ({(df['Furnishing_Status'].value_counts().iloc[0]/len(df)*100):.1f}%)
"""
ax1.text(0.5, 0.5, summary_text, transform=ax1.transAxes, fontsize=12, verticalalignment='center', 
         horizontalalignment='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5), family='monospace')

# Mini visualizations
ax2 = fig.add_subplot(gs[1, 0])
df['BHK'].value_counts().sort_index().plot(kind='bar', ax=ax2, color='skyblue')
ax2.set_title('BHK Distribution', fontsize=12, fontweight='bold')
ax2.set_xlabel('BHK')
ax2.set_ylabel('Count')

ax3 = fig.add_subplot(gs[1, 1])
df['Property_Type'].value_counts().plot(kind='pie', ax=ax3, autopct='%1.1f%%', colors=['#FF9999', '#66B2FF'])
ax3.set_title('Property Type', fontsize=12, fontweight='bold')
ax3.set_ylabel('')

ax4 = fig.add_subplot(gs[1, 2])
df['Locality_Tier'].value_counts().plot(kind='bar', ax=ax4, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
ax4.set_title('Locality Tier', fontsize=12, fontweight='bold')
ax4.set_xlabel('Tier')
ax4.set_ylabel('Count')
ax4.tick_params(axis='x', rotation=0)

ax5 = fig.add_subplot(gs[2, 0])
ax5.hist(df['Price_Lakhs'], bins=30, color='gold', alpha=0.7, edgecolor='black')
ax5.set_title('Price Distribution', fontsize=12, fontweight='bold')
ax5.set_xlabel('Price (Lakhs)')
ax5.set_ylabel('Frequency')

ax6 = fig.add_subplot(gs[2, 1])
ax6.scatter(df['Area_SqFt'], df['Price_Lakhs'], alpha=0.5, s=20, c='teal')
ax6.set_title('Price vs Area', fontsize=12, fontweight='bold')
ax6.set_xlabel('Area (SqFt)')
ax6.set_ylabel('Price (Lakhs)')
ax6.grid(True, alpha=0.3)

ax7 = fig.add_subplot(gs[2, 2])
top_10_loc = df['Locality'].value_counts().head(10)
top_10_loc.plot(kind='barh', ax=ax7, color='coral')
ax7.set_title('Top 10 Localities', fontsize=12, fontweight='bold')
ax7.set_xlabel('Count')
ax7.set_ylabel('Locality')
ax7.invert_yaxis()

plt.suptitle('COMPREHENSIVE PROPERTY MARKET DASHBOARD', fontsize=18, fontweight='bold', y=0.98)
plt.savefig('visualizations/21_comprehensive_summary_dashboard.png', dpi=300, bbox_inches='tight')
plt.close()
viz_count += 1

# 22. FEATURE IMPORTANCE (FROM BEST MODEL)
print(f"  {viz_count+1}. Creating Feature Importance Chart...")
try:
    import joblib
    
    # Try loading XGBoost model (has feature_importances_)
    try:
        model = joblib.load('models/model_2_xgboost.pkl')
        model_name = 'XGBoost'
    except:
        # Fall back to Random Forest
        try:
            model = joblib.load('models/model_5_randomforest.pkl')
            model_name = 'Random Forest'
        except:
            print("  ⚠️  No compatible model found for feature importance")
            model = None
    
    if model is not None and hasattr(model, 'feature_importances_'):
        # Get feature names (19 features)
        feature_names = ['BHK', 'Area_SqFt', 'Locality', 'Locality_Tier', 'Seller_Type', 
                        'Property_Type', 'Furnishing_Status', 'Under_Construction', 'Amenities_Count',
                        'Area_Per_BHK', 'Is_Large_Apartment', 'Is_Premium_Locality', 'Is_Budget_Locality',
                        'BHK_Area_Combo', 'High_Amenity', 'Construction_Category', 'Locality_Property_Count',
                        'Locality_Median_Area', 'Locality_Common_BHK']
        
        # Get feature importances
        importances = model.feature_importances_
        
        # Create dataframe and sort
        feature_imp_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': importances
        }).sort_values('Importance', ascending=False)
        
        # Plot top 15 features
        plt.figure(figsize=(14, 8))
        top_features = feature_imp_df.head(15)
        
        colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(top_features)))
        bars = plt.barh(range(len(top_features)), top_features['Importance'], color=colors)
        plt.yticks(range(len(top_features)), top_features['Feature'])
        plt.xlabel('Importance Score', fontweight='bold', fontsize=12)
        plt.ylabel('Features', fontweight='bold', fontsize=12)
        plt.title(f'Top 15 Feature Importances ({model_name} Model)', fontsize=16, fontweight='bold', pad=20)
        plt.gca().invert_yaxis()
        
        # Add value labels
        for i, (idx, row) in enumerate(top_features.iterrows()):
            plt.text(row['Importance'], i, f' {row["Importance"]:.4f}', 
                    va='center', fontsize=10, fontweight='bold')
        
        plt.grid(axis='x', alpha=0.3, linestyle='--')
        plt.tight_layout()
        plt.savefig('visualizations/22_feature_importance.png', dpi=300, bbox_inches='tight')
        plt.close()
        viz_count += 1
        
        # Print top 10 features
        print(f"  ✅ Feature importance chart created")
        print(f"\n  📊 Top 10 Most Important Features:")
        for idx, row in feature_imp_df.head(10).iterrows():
            print(f"     {row['Feature']:<25} {row['Importance']:.4f}")
    else:
        print("  ⚠️  Model doesn't support feature importance")
        
except Exception as e:
    print(f"  ⚠️  Could not create feature importance chart: {e}")

print("\n✅ ALL VISUALIZATIONS CREATED!")
print(f"📊 Total: {viz_count} visualizations")
print(f"📁 Location: visualizations/")
print("="*80)
