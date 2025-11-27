"""
Locality-Level Summary Generation
Aggregates property data by locality and generates:
- Average prices and statistics
- Common amenities
- Popular BHK sizes
- Target audience identification
- Locality personality/character
"""

import pandas as pd
import numpy as np
from typing import Dict, List
from collections import Counter

class LocalityAnalyzer:
    """Analyze and generate summaries for localities"""
    
    def __init__(self, data_path: str = 'data/cleaned/cleaned_data.csv'):
        """Initialize with cleaned property data"""
        try:
            self.df = pd.read_csv(data_path)
            # Filter out Unknown localities
            self.df = self.df[self.df['Locality'] != 'Unknown'].copy()
            print(f"✅ Loaded {len(self.df)} properties from {self.df['Locality'].nunique()} localities")
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            self.df = pd.DataFrame()
    
    def get_locality_stats(self, locality: str) -> Dict:
        """Get statistical summary for a locality"""
        locality_data = self.df[self.df['Locality'] == locality]
        
        if len(locality_data) == 0:
            return {'error': f'No data found for {locality}'}
        
        stats = {
            'locality': locality,
            'total_properties': len(locality_data),
            'avg_price_lakhs': round(locality_data['Price_Lakhs'].mean(), 2),
            'median_price_lakhs': round(locality_data['Price_Lakhs'].median(), 2),
            'min_price_lakhs': round(locality_data['Price_Lakhs'].min(), 2),
            'max_price_lakhs': round(locality_data['Price_Lakhs'].max(), 2),
            'avg_area_sqft': round(locality_data['Area_SqFt'].mean(), 0),
            'median_area_sqft': round(locality_data['Area_SqFt'].median(), 0),
            'locality_tier': locality_data['Locality_Tier'].mode().values[0] if 'Locality_Tier' in locality_data.columns else 'Unknown'
        }
        
        return stats
    
    def get_common_bhk(self, locality: str) -> List[tuple]:
        """Get most common BHK configurations"""
        locality_data = self.df[self.df['Locality'] == locality]
        
        if len(locality_data) == 0:
            return []
        
        bhk_counts = locality_data['BHK'].value_counts()
        total = len(locality_data)
        
        result = []
        for bhk, count in bhk_counts.head(3).items():
            percentage = (count / total) * 100
            result.append((int(bhk), count, round(percentage, 1)))
        
        return result
    
    def get_common_amenities(self, locality: str) -> List[str]:
        """Get most common amenities in the locality"""
        locality_data = self.df[self.df['Locality'] == locality]
        
        if len(locality_data) == 0 or 'Amenities_Count' not in locality_data.columns:
            return []
        
        # Based on amenities count distribution
        avg_amenities = locality_data['Amenities_Count'].mean()
        
        amenities_list = []
        if avg_amenities >= 4:
            amenities_list = ['Gym', 'Swimming Pool', 'Security', 'Parking', 'Garden', 'Clubhouse']
        elif avg_amenities >= 2:
            amenities_list = ['Security', 'Parking', 'Lift', 'Power Backup']
        else:
            amenities_list = ['Basic Security', 'Parking']
        
        return amenities_list
    
    def identify_target_audience(self, locality: str) -> List[str]:
        """Identify target audience based on property characteristics"""
        locality_data = self.df[self.df['Locality'] == locality]
        
        if len(locality_data) == 0:
            return ['General Buyers']
        
        audience = []
        
        # Check BHK distribution
        bhk_mode = locality_data['BHK'].mode().values[0] if len(locality_data['BHK'].mode()) > 0 else 2
        
        if bhk_mode >= 4:
            audience.append('Large Families')
        elif bhk_mode == 3:
            audience.append('Families')
        elif bhk_mode == 2:
            audience.append('Small Families / Working Professionals')
        else:
            audience.append('Students / Bachelors')
        
        # Check price range
        avg_price = locality_data['Price_Lakhs'].mean()
        if avg_price >= 100:
            audience.append('High-Income Buyers')
        elif avg_price >= 60:
            audience.append('Upper-Middle Class')
        elif avg_price >= 40:
            audience.append('Middle Class')
        else:
            audience.append('Budget Buyers')
        
        # Check property type
        if 'Property_Type' in locality_data.columns:
            apt_ratio = (locality_data['Property_Type'] == 'Apartment').sum() / len(locality_data)
            if apt_ratio > 0.8:
                audience.append('Apartment Seekers')
            elif apt_ratio < 0.3:
                audience.append('Independent House Seekers')
        
        return audience
    
    def determine_locality_personality(self, locality: str) -> Dict[str, str]:
        """Determine locality character/personality"""
        locality_data = self.df[self.df['Locality'] == locality]
        
        if len(locality_data) == 0:
            return {'personality': 'Unknown', 'description': 'No data available'}
        
        stats = self.get_locality_stats(locality)
        avg_price = stats['avg_price_lakhs']
        tier = stats['locality_tier']
        property_count = stats['total_properties']
        
        personality = []
        description_parts = []
        
        # Price-based personality
        if tier == 'Tier 1' or avg_price >= 100:
            personality.append('Premium')
            description_parts.append('high-end residential area')
        elif tier == 'Tier 2' or avg_price >= 50:
            personality.append('Mid-Range')
            description_parts.append('well-established residential locality')
        else:
            personality.append('Budget-Friendly')
            description_parts.append('affordable housing option')
        
        # Activity level
        if property_count >= 100:
            personality.append('Highly Active')
            description_parts.append('high market activity')
        elif property_count >= 50:
            personality.append('Active')
            description_parts.append('good market activity')
        else:
            personality.append('Emerging')
            description_parts.append('developing area')
        
        # Amenities level
        avg_amenities = locality_data['Amenities_Count'].mean() if 'Amenities_Count' in locality_data.columns else 0
        if avg_amenities >= 4:
            personality.append('Amenity-Rich')
            description_parts.append('excellent amenities')
        elif avg_amenities >= 2:
            personality.append('Well-Facilitated')
            description_parts.append('good basic facilities')
        
        # Size preference
        avg_area = stats['avg_area_sqft']
        if avg_area >= 1500:
            personality.append('Spacious')
            description_parts.append('larger properties')
        elif avg_area >= 1000:
            personality.append('Comfortable')
            description_parts.append('moderately-sized properties')
        else:
            personality.append('Compact')
            description_parts.append('compact living spaces')
        
        return {
            'personality': ' & '.join(personality),
            'description': f"A {', '.join(description_parts)}",
            'character_tags': personality
        }
    
    def generate_locality_summary(self, locality: str, use_llm: bool = False) -> str:
        """
        Generate comprehensive locality summary
        
        Args:
            locality: Locality name
            use_llm: If True, use LLM for generation (requires setup)
        """
        stats = self.get_locality_stats(locality)
        
        if 'error' in stats:
            return stats['error']
        
        bhk_distribution = self.get_common_bhk(locality)
        amenities = self.get_common_amenities(locality)
        target_audience = self.identify_target_audience(locality)
        personality = self.determine_locality_personality(locality)
        
        # Build summary
        summary = f"""
{'='*80}
LOCALITY ANALYSIS: {locality.upper()}
{'='*80}

📊 MARKET STATISTICS:
  • Total Properties: {stats['total_properties']}
  • Average Price: ₹{stats['avg_price_lakhs']} Lakhs
  • Price Range: ₹{stats['min_price_lakhs']}L - ₹{stats['max_price_lakhs']}L
  • Median Price: ₹{stats['median_price_lakhs']} Lakhs
  • Average Area: {stats['avg_area_sqft']} sqft
  • Locality Tier: {stats['locality_tier']}

🏠 POPULAR CONFIGURATIONS:
"""
        for bhk, count, percentage in bhk_distribution:
            summary += f"  • {bhk} BHK: {count} properties ({percentage}%)\n"
        
        summary += f"""
🏢 COMMON AMENITIES:
  • {', '.join(amenities)}

👥 TARGET AUDIENCE:
  • {', '.join(target_audience)}

✨ LOCALITY PERSONALITY:
  • Character: {personality['personality']}
  • Description: {personality['description']}
  • Tags: {', '.join(personality['character_tags'])}

{'='*80}
"""
        return summary
    
    def compare_localities(self, locality1: str, locality2: str) -> str:
        """Compare two localities"""
        stats1 = self.get_locality_stats(locality1)
        stats2 = self.get_locality_stats(locality2)
        
        if 'error' in stats1 or 'error' in stats2:
            return "Error: One or both localities not found"
        
        comparison = f"""
{'='*80}
LOCALITY COMPARISON: {locality1.upper()} vs {locality2.upper()}
{'='*80}

📊 PRICE COMPARISON:
  {locality1}: ₹{stats1['avg_price_lakhs']}L (avg) | ₹{stats1['median_price_lakhs']}L (median)
  {locality2}: ₹{stats2['avg_price_lakhs']}L (avg) | ₹{stats2['median_price_lakhs']}L (median)
  
  Price Difference: ₹{abs(stats1['avg_price_lakhs'] - stats2['avg_price_lakhs'])}L
  {'⬆️ ' + locality1 if stats1['avg_price_lakhs'] > stats2['avg_price_lakhs'] else '⬆️ ' + locality2} is more expensive

📏 AREA COMPARISON:
  {locality1}: {stats1['avg_area_sqft']} sqft (avg)
  {locality2}: {stats2['avg_area_sqft']} sqft (avg)

🏆 TIER COMPARISON:
  {locality1}: {stats1['locality_tier']}
  {locality2}: {stats2['locality_tier']}

📈 MARKET ACTIVITY:
  {locality1}: {stats1['total_properties']} properties
  {locality2}: {stats2['total_properties']} properties

{'='*80}
"""
        return comparison
    
    def get_top_localities_by_metric(self, metric: str = 'price', top_n: int = 10) -> pd.DataFrame:
        """Get top localities by a specific metric"""
        if metric == 'price':
            return self.df.groupby('Locality')['Price_Lakhs'].agg(['mean', 'median', 'count']).sort_values('mean', ascending=False).head(top_n)
        elif metric == 'area':
            return self.df.groupby('Locality')['Area_SqFt'].agg(['mean', 'median', 'count']).sort_values('mean', ascending=False).head(top_n)
        elif metric == 'activity':
            return self.df.groupby('Locality').size().sort_values(ascending=False).head(top_n)
        else:
            return pd.DataFrame()


if __name__ == "__main__":
    # Test the analyzer
    print("="*80)
    print("LOCALITY ANALYZER TEST")
    print("="*80)
    
    analyzer = LocalityAnalyzer()
    
    if not analyzer.df.empty:
        # Get a sample locality
        sample_locality = analyzer.df['Locality'].value_counts().index[0]
        
        print(f"\nGenerating summary for: {sample_locality}")
        print(analyzer.generate_locality_summary(sample_locality))
        
        # Show top 5 localities by price
        print("\n" + "="*80)
        print("TOP 5 LOCALITIES BY AVERAGE PRICE")
        print("="*80)
        top_localities = analyzer.get_top_localities_by_metric('price', 5)
        print(top_localities)
        print("="*80)
