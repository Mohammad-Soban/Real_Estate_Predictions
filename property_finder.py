"""
Interactive Property Finder - CLI
Personalized property recommendations based on user preferences
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional
import os
import sys

class PropertyFinder:
    """Interactive property recommendation system"""
    
    def __init__(self, data_file: str = 'data/cleaned/cleaned_data.csv'):
        """Initialize with cleaned data"""
        print("\n" + "="*80)
        print("  🏠 PROPERTY FINDER - Your Personalized Real Estate Assistant")
        print("="*80)
        print("\n📂 Loading property database...")
        
        self.df = pd.read_csv(data_file)
        
        # Remove duplicates
        original_count = len(self.df)
        self.df = self.df.drop_duplicates(
            subset=['BHK', 'Area_SqFt', 'Locality', 'Price_Lakhs'],
            keep='first'
        )
        duplicates_removed = original_count - len(self.df)
        
        print(f"✅ Loaded {len(self.df)} unique properties")
        if duplicates_removed > 0:
            print(f"   🧹 Removed {duplicates_removed} duplicates")
        
        # Add unique Property_ID if not exists
        if 'Property_ID' not in self.df.columns:
            self.df['Property_ID'] = ['PROP_' + str(i+1).zfill(6) for i in range(len(self.df))]
        
        self.user_preferences = {}
    
    def ask_questions(self):
        """Interactive question flow to gather user preferences"""
        print("\n" + "="*80)
        print("  📋 TELL US YOUR PREFERENCES")
        print("="*80)
        print("\nAnswer a few questions to get personalized recommendations.\n")
        
        # Question 1: Budget
        print("─" * 80)
        print("💰 QUESTION 1/6: What's your budget?")
        print("─" * 80)
        while True:
            try:
                budget_input = input("Enter minimum and maximum in Lakhs (e.g., '50 80'): ").strip()
                min_budget, max_budget = map(float, budget_input.split())
                if min_budget > max_budget:
                    print("⚠️  Minimum should be less than maximum. Try again.")
                    continue
                self.user_preferences['budget_min'] = min_budget
                self.user_preferences['budget_max'] = max_budget
                print(f"✅ Budget set: ₹{min_budget}L - ₹{max_budget}L")
                break
            except:
                print("⚠️  Invalid input. Please enter two numbers separated by space (e.g., '50 80')")
        
        # Question 2: BHK
        print("\n" + "─" * 80)
        print("🛏️  QUESTION 2/6: How many bedrooms (BHK)?")
        print("─" * 80)
        available_bhks = sorted(self.df['BHK'].dropna().unique())
        print(f"Available options: {', '.join(map(str, map(int, available_bhks)))}")
        while True:
            bhk_input = input("Enter number (e.g., '3') or 'any': ").strip().lower()
            if bhk_input == 'any':
                self.user_preferences['bhk'] = None
                print("✅ BHK: Any")
                break
            try:
                bhk = float(bhk_input)
                if bhk in available_bhks:
                    self.user_preferences['bhk'] = bhk
                    print(f"✅ BHK: {int(bhk)}")
                    break
                else:
                    print(f"⚠️  No properties with {int(bhk)} BHK available. Try: {', '.join(map(str, map(int, available_bhks)))}")
            except:
                print("⚠️  Invalid input. Enter a number or 'any'")
        
        # Question 3: Locality
        print("\n" + "─" * 80)
        print("📍 QUESTION 3/6: Preferred localities?")
        print("─" * 80)
        
        # Filter by budget first to show relevant localities
        budget_filtered = self.df[
            (self.df['Price_Lakhs'] >= self.user_preferences['budget_min']) &
            (self.df['Price_Lakhs'] <= self.user_preferences['budget_max'])
        ]
        
        if len(budget_filtered) > 0:
            localities = sorted(budget_filtered['Locality'].unique())
            print(f"\nLocalities in your budget ({len(localities)} available):")
            
            # Show first 20 localities
            display_localities = localities[:20]
            for i in range(0, len(display_localities), 4):
                row = display_localities[i:i+4]
                print("  " + ", ".join(row))
            
            if len(localities) > 20:
                print(f"  ... and {len(localities) - 20} more")
        
        locality_input = input("\nEnter comma-separated localities or 'any': ").strip().lower()
        if locality_input == 'any':
            self.user_preferences['localities'] = None
            print("✅ Localities: Any")
        else:
            localities_list = [loc.strip().title() for loc in locality_input.split(',')]
            self.user_preferences['localities'] = localities_list
            print(f"✅ Preferred localities: {', '.join(localities_list)}")
        
        # Question 4: Furnishing
        print("\n" + "─" * 80)
        print("🪑 QUESTION 4/6: Furnishing preference?")
        print("─" * 80)
        furnishing_options = self.df['Furnishing_Status'].dropna().unique()
        print(f"Options: {', '.join(furnishing_options)}, Any")
        while True:
            furnishing_input = input("Your choice: ").strip().title()
            if furnishing_input.lower() == 'any':
                self.user_preferences['furnishing'] = None
                print("✅ Furnishing: Any")
                break
            elif furnishing_input in furnishing_options:
                self.user_preferences['furnishing'] = furnishing_input
                print(f"✅ Furnishing: {furnishing_input}")
                break
            else:
                print(f"⚠️  Invalid. Choose from: {', '.join(furnishing_options)}, Any")
        
        # Question 5: Amenities (skip for simplicity, can be added later)
        print("\n" + "─" * 80)
        print("✨ QUESTION 5/6: Minimum number of amenities?")
        print("─" * 80)
        print("Properties have 0-6 amenities")
        while True:
            try:
                amenity_input = input("Enter minimum (0-6) or 'any': ").strip().lower()
                if amenity_input == 'any':
                    self.user_preferences['min_amenities'] = 0
                    print("✅ Amenities: Any")
                    break
                amenity_count = int(amenity_input)
                if 0 <= amenity_count <= 6:
                    self.user_preferences['min_amenities'] = amenity_count
                    print(f"✅ Minimum amenities: {amenity_count}")
                    break
                else:
                    print("⚠️  Enter a number between 0-6")
            except:
                print("⚠️  Invalid input")
        
        # Question 6: Property Type
        print("\n" + "─" * 80)
        print("🏢 QUESTION 6/6: Property type?")
        print("─" * 80)
        property_types = self.df['Property_Type'].dropna().unique()
        print(f"Options: {', '.join(property_types)}, Any")
        while True:
            type_input = input("Your choice: ").strip().title()
            if type_input.lower() == 'any':
                self.user_preferences['property_type'] = None
                print("✅ Property type: Any")
                break
            elif type_input in property_types:
                self.user_preferences['property_type'] = type_input
                print(f"✅ Property type: {type_input}")
                break
            else:
                print(f"⚠️  Invalid. Choose from: {', '.join(property_types)}, Any")
        
        print("\n" + "="*80)
        print("  ✅ PREFERENCES CAPTURED!")
        print("="*80)
    
    def filter_properties(self) -> pd.DataFrame:
        """Filter properties based on user preferences"""
        print("\n🔍 Filtering properties...")
        
        filtered_df = self.df.copy()
        
        # Budget filter
        filtered_df = filtered_df[
            (filtered_df['Price_Lakhs'] >= self.user_preferences['budget_min']) &
            (filtered_df['Price_Lakhs'] <= self.user_preferences['budget_max'])
        ]
        print(f"   After budget filter: {len(filtered_df)} properties")
        
        # BHK filter
        if self.user_preferences['bhk'] is not None:
            filtered_df = filtered_df[filtered_df['BHK'] == self.user_preferences['bhk']]
            print(f"   After BHK filter: {len(filtered_df)} properties")
        
        # Locality filter
        if self.user_preferences['localities'] is not None:
            filtered_df = filtered_df[filtered_df['Locality'].isin(self.user_preferences['localities'])]
            print(f"   After locality filter: {len(filtered_df)} properties")
        
        # Furnishing filter
        if self.user_preferences['furnishing'] is not None:
            filtered_df = filtered_df[filtered_df['Furnishing_Status'] == self.user_preferences['furnishing']]
            print(f"   After furnishing filter: {len(filtered_df)} properties")
        
        # Amenities filter
        if self.user_preferences['min_amenities'] > 0:
            filtered_df = filtered_df[filtered_df['Amenities_Count'] >= self.user_preferences['min_amenities']]
            print(f"   After amenities filter: {len(filtered_df)} properties")
        
        # Property type filter
        if self.user_preferences['property_type'] is not None:
            filtered_df = filtered_df[filtered_df['Property_Type'] == self.user_preferences['property_type']]
            print(f"   After property type filter: {len(filtered_df)} properties")
        
        return filtered_df
    
    def calculate_match_score(self, property_row: pd.Series) -> float:
        """Calculate how well a property matches user preferences (0-100)"""
        score = 100.0
        
        # Budget match (30% weight) - already filtered, so always perfect
        # Just check if it's in sweet spot (middle 50% of budget range)
        budget_range = self.user_preferences['budget_max'] - self.user_preferences['budget_min']
        budget_middle_min = self.user_preferences['budget_min'] + budget_range * 0.25
        budget_middle_max = self.user_preferences['budget_max'] - budget_range * 0.25
        
        if budget_middle_min <= property_row['Price_Lakhs'] <= budget_middle_max:
            score += 5  # Bonus for being in sweet spot
        
        # BHK exact match bonus (already filtered if specified)
        if self.user_preferences['bhk'] is not None:
            score += 10  # Exact match bonus
        
        # Locality preference bonus
        if self.user_preferences['localities'] is not None:
            if property_row['Locality'] in self.user_preferences['localities']:
                score += 15  # Preferred locality bonus
        
        # Furnishing exact match bonus
        if self.user_preferences['furnishing'] is not None:
            if property_row['Furnishing_Status'] == self.user_preferences['furnishing']:
                score += 10  # Exact match bonus
        
        # Amenities bonus (more is better)
        amenity_score = (property_row.get('Amenities_Count', 0) / 6.0) * 10
        score += amenity_score
        
        # Property type exact match bonus
        if self.user_preferences['property_type'] is not None:
            if property_row['Property_Type'] == self.user_preferences['property_type']:
                score += 10  # Exact match bonus
        
        # Locality tier bonus
        if property_row.get('Locality_Tier') == 'Tier 1':
            score += 8
        elif property_row.get('Locality_Tier') == 'Tier 2':
            score += 5
        
        # Area bonus (more sqft = better, but diminishing returns)
        area_score = min((property_row.get('Area_SqFt', 1000) / 3000.0) * 5, 5)
        score += area_score
        
        return min(score, 100)  # Cap at 100
    
    def display_recommendations(self, recommendations_df: pd.DataFrame):
        """Display top 10 recommendations with detailed cards"""
        print("\n" + "="*80)
        print("        🎯 TOP 10 PROPERTY RECOMMENDATIONS FOR YOU")
        print("="*80)
        
        # Show user preferences summary
        print("\n📋 Your Preferences:")
        print(f"   ✓ Budget: ₹{self.user_preferences['budget_min']}L - ₹{self.user_preferences['budget_max']}L")
        print(f"   ✓ BHK: {int(self.user_preferences['bhk']) if self.user_preferences['bhk'] else 'Any'}")
        print(f"   ✓ Localities: {', '.join(self.user_preferences['localities']) if self.user_preferences['localities'] else 'Any'}")
        print(f"   ✓ Furnishing: {self.user_preferences['furnishing'] if self.user_preferences['furnishing'] else 'Any'}")
        print(f"   ✓ Minimum Amenities: {self.user_preferences['min_amenities']}")
        print(f"   ✓ Property Type: {self.user_preferences['property_type'] if self.user_preferences['property_type'] else 'Any'}")
        
        print("\n" + "="*80 + "\n")
        
        # Display each property
        for rank, (idx, prop) in enumerate(recommendations_df.head(10).iterrows(), 1):
            medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}"
            
            print(f"{medal} RANK {rank} - Match Score: {prop['match_score']:.0f}/100")
            print("="*80)
            
            # Basic info
            bhk = int(prop['BHK']) if pd.notna(prop['BHK']) else '?'
            print(f"\n📍 {bhk} BHK {prop.get('Property_Type', 'Property')} in {prop['Locality']}")
            
            price_per_sqft = prop['Price_Lakhs'] * 100000 / prop['Area_SqFt'] if prop['Area_SqFt'] > 0 else 0
            print(f"💰 Price: ₹{prop['Price_Lakhs']:.1f} Lakhs (₹{price_per_sqft:,.0f}/sqft)")
            print(f"📐 Area: {prop['Area_SqFt']:.0f} sqft")
            
            furnishing = prop.get('Furnishing_Status', 'Unknown')
            construction = 'Ready to Move' if prop.get('Under_Construction', 0) == 0 else 'Under Construction'
            print(f"🏠 {furnishing} | {construction}")
            
            tier = prop.get('Locality_Tier', 'Unknown')
            print(f"🎯 Locality: {tier}")
            
            # Amenities
            amenity_count = int(prop.get('Amenities_Count', 0))
            print(f"\n✨ Amenities: {amenity_count} available")
            
            # Why this property?
            print(f"\n💡 Why this property?")
            reasons = []
            
            # Budget match
            if self.user_preferences['budget_min'] <= prop['Price_Lakhs'] <= self.user_preferences['budget_max']:
                reasons.append("✓ Perfect budget match")
            
            # BHK match
            if self.user_preferences['bhk'] and prop['BHK'] == self.user_preferences['bhk']:
                reasons.append(f"✓ Exactly {int(self.user_preferences['bhk'])} BHK as requested")
            
            # Locality match
            if self.user_preferences['localities'] and prop['Locality'] in self.user_preferences['localities']:
                reasons.append(f"✓ In your preferred locality ({prop['Locality']})")
            
            # Furnishing match
            if self.user_preferences['furnishing'] and prop.get('Furnishing_Status') == self.user_preferences['furnishing']:
                reasons.append(f"✓ {self.user_preferences['furnishing']} as preferred")
            
            # Amenities
            if amenity_count >= self.user_preferences['min_amenities']:
                if amenity_count >= 4:
                    reasons.append(f"✓ Well-facilitated ({amenity_count} amenities)")
            
            # Tier bonus
            if prop.get('Locality_Tier') == 'Tier 1':
                reasons.append("✓ Premium Tier 1 locality")
            
            # High match score
            if prop['match_score'] >= 95:
                reasons.append(f"✓ Excellent match score ({prop['match_score']:.0f}/100)")
            
            for reason in reasons[:5]:  # Show top 5 reasons
                print(f"   {reason}")
            
            print(f"\n🔗 Property ID: {prop.get('Property_ID', 'N/A')}")
            
            print("\n" + "─"*80 + "\n")
        
        print("="*80)
        print(f"\n💾 Want to save these recommendations? Copy Property IDs for reference.")
        print("📞 Contact real estate agents with these Property IDs for more details.\n")
    
    def run(self):
        """Main execution flow"""
        try:
            # Ask questions
            self.ask_questions()
            
            # Filter properties
            filtered_df = self.filter_properties()
            
            if len(filtered_df) == 0:
                print("\n❌ No properties found matching your criteria.")
                print("💡 Try adjusting your preferences (e.g., wider budget range, more localities)")
                return
            
            print(f"\n✅ Found {len(filtered_df)} properties matching your criteria!")
            
            # Calculate match scores
            print("\n📊 Calculating match scores...")
            filtered_df['match_score'] = filtered_df.apply(self.calculate_match_score, axis=1)
            
            # Sort by match score
            recommendations = filtered_df.sort_values('match_score', ascending=False)
            
            # Remove any remaining duplicates
            recommendations = recommendations.drop_duplicates(
                subset=['Property_ID'],
                keep='first'
            )
            
            # Display top 10
            self.display_recommendations(recommendations)
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Process interrupted by user.")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()


def main():
    """Entry point"""
    finder = PropertyFinder()
    finder.run()


if __name__ == "__main__":
    main()
