"""
Property Q&A System (Simple RAG-like approach)
Answers natural language questions about properties
"""

import pandas as pd
from typing import Dict, List
import re

class PropertyQASystem:
    """Answer questions about properties using rule-based approach"""
    
    def __init__(self, data_path: str = 'data/cleaned/cleaned_data.csv'):
        """Initialize with property data"""
        try:
            self.df = pd.read_csv(data_path)
            self.df = self.df[self.df['Locality'] != 'Unknown'].copy()
            print(f"✅ Loaded {len(self.df)} properties for Q&A")
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            self.df = pd.DataFrame()
    
    def answer_question(self, question: str) -> str:
        """Answer a question about properties"""
        question_lower = question.lower()
        
        # Price-related questions
        if any(word in question_lower for word in ['cheap', 'affordable', 'budget', 'cheapest']):
            return self._answer_cheapest_properties(question_lower)
        
        elif any(word in question_lower for word in ['expensive', 'costly', 'premium', 'luxury']):
            return self._answer_expensive_properties(question_lower)
        
        elif 'average price' in question_lower or 'avg price' in question_lower:
            return self._answer_average_price(question_lower)
        
        # Locality-related questions
        elif 'locality' in question_lower or 'area' in question_lower or 'location' in question_lower:
            if 'best' in question_lower or 'top' in question_lower:
                return self._answer_best_localities()
            elif 'compare' in question_lower:
                return self._answer_compare_localities(question_lower)
        
        # BHK-related questions
        elif 'bhk' in question_lower:
            return self._answer_bhk_query(question_lower)
        
        # Area-related questions
        elif 'sqft' in question_lower or 'area' in question_lower or 'size' in question_lower:
            return self._answer_area_query(question_lower)
        
        # General stats
        elif 'how many' in question_lower or 'total' in question_lower:
            return self._answer_count_query(question_lower)
        
        else:
            return "I can answer questions about:\n• Prices (cheapest, expensive, average)\n• Localities (best, compare)\n• BHK configurations\n• Property sizes\n• Total counts and statistics"
    
    def _answer_cheapest_properties(self, question: str) -> str:
        """Find cheapest properties"""
        # Extract locality if mentioned
        localities = self.df['Locality'].unique()
        mentioned_locality = None
        for loc in localities:
            if loc.lower() in question:
                mentioned_locality = loc
                break
        
        if mentioned_locality:
            filtered_df = self.df[self.df['Locality'] == mentioned_locality]
            title = f"Cheapest properties in {mentioned_locality}"
        else:
            filtered_df = self.df
            title = "Cheapest properties overall"
        
        top_5 = filtered_df.nsmallest(5, 'Price_Lakhs')[['BHK', 'Area_SqFt', 'Price_Lakhs', 'Locality', 'Property_Type']]
        
        result = f"\n{title}:\n\n"
        for idx, row in top_5.iterrows():
            result += f"• {int(row['BHK'])} BHK {row['Property_Type']} in {row['Locality']}\n"
            result += f"  Price: ₹{row['Price_Lakhs']}L | Area: {int(row['Area_SqFt'])} sqft\n\n"
        
        return result
    
    def _answer_expensive_properties(self, question: str) -> str:
        """Find most expensive properties"""
        top_5 = self.df.nlargest(5, 'Price_Lakhs')[['BHK', 'Area_SqFt', 'Price_Lakhs', 'Locality', 'Property_Type']]
        
        result = "\nMost expensive properties:\n\n"
        for idx, row in top_5.iterrows():
            result += f"• {int(row['BHK'])} BHK {row['Property_Type']} in {row['Locality']}\n"
            result += f"  Price: ₹{row['Price_Lakhs']}L | Area: {int(row['Area_SqFt'])} sqft\n\n"
        
        return result
    
    def _answer_average_price(self, question: str) -> str:
        """Calculate average prices"""
        overall_avg = self.df['Price_Lakhs'].mean()
        overall_median = self.df['Price_Lakhs'].median()
        
        result = f"\n💰 Price Statistics:\n\n"
        result += f"• Overall Average: ₹{overall_avg:.2f} Lakhs\n"
        result += f"• Overall Median: ₹{overall_median:.2f} Lakhs\n"
        result += f"• Price Range: ₹{self.df['Price_Lakhs'].min()}L - ₹{self.df['Price_Lakhs'].max()}L\n\n"
        
        # By tier
        if 'Locality_Tier' in self.df.columns:
            result += "By Locality Tier:\n"
            for tier in ['Tier 1', 'Tier 2', 'Tier 3']:
                tier_avg = self.df[self.df['Locality_Tier'] == tier]['Price_Lakhs'].mean()
                result += f"• {tier}: ₹{tier_avg:.2f}L (avg)\n"
        
        return result
    
    def _answer_best_localities(self) -> str:
        """Show best localities by different metrics"""
        result = "\n🏆 Top Localities:\n\n"
        
        # By average price (premium)
        result += "Most Premium (Highest Avg Price):\n"
        top_by_price = self.df.groupby('Locality')['Price_Lakhs'].mean().nlargest(5)
        for loc, price in top_by_price.items():
            result += f"• {loc}: ₹{price:.2f}L\n"
        
        # By property count (most active)
        result += "\nMost Active (Most Properties):\n"
        top_by_count = self.df['Locality'].value_counts().head(5)
        for loc, count in top_by_count.items():
            result += f"• {loc}: {count} properties\n"
        
        return result
    
    def _answer_compare_localities(self, question: str) -> str:
        """Compare localities mentioned in question"""
        # Simple: just show top 3 localities comparison
        top_3 = self.df.groupby('Locality').agg({
            'Price_Lakhs': 'mean',
            'Area_SqFt': 'mean',
            'BHK': 'mean'
        }).nlargest(3, 'Price_Lakhs')
        
        result = "\n📊 Locality Comparison (Top 3):\n\n"
        for loc, data in top_3.iterrows():
            result += f"• {loc}:\n"
            result += f"  Avg Price: ₹{data['Price_Lakhs']:.2f}L\n"
            result += f"  Avg Area: {data['Area_SqFt']:.0f} sqft\n"
            result += f"  Avg BHK: {data['BHK']:.1f}\n\n"
        
        return result
    
    def _answer_bhk_query(self, question: str) -> str:
        """Answer BHK-related questions"""
        result = "\n🏠 BHK Distribution:\n\n"
        
        bhk_counts = self.df['BHK'].value_counts().sort_index()
        total = len(self.df)
        
        for bhk, count in bhk_counts.items():
            percentage = (count / total) * 100
            avg_price = self.df[self.df['BHK'] == bhk]['Price_Lakhs'].mean()
            result += f"• {int(bhk)} BHK: {count} properties ({percentage:.1f}%) | Avg Price: ₹{avg_price:.2f}L\n"
        
        return result
    
    def _answer_area_query(self, question: str) -> str:
        """Answer area/size-related questions"""
        result = "\n📏 Property Size Statistics:\n\n"
        
        result += f"• Average Area: {self.df['Area_SqFt'].mean():.0f} sqft\n"
        result += f"• Median Area: {self.df['Area_SqFt'].median():.0f} sqft\n"
        result += f"• Range: {self.df['Area_SqFt'].min():.0f} - {self.df['Area_SqFt'].max():.0f} sqft\n\n"
        
        # By BHK
        result += "Average Area by BHK:\n"
        for bhk in sorted(self.df['BHK'].unique()):
            avg_area = self.df[self.df['BHK'] == bhk]['Area_SqFt'].mean()
            result += f"• {int(bhk)} BHK: {avg_area:.0f} sqft\n"
        
        return result
    
    def _answer_count_query(self, question: str) -> str:
        """Answer counting questions"""
        result = "\n📊 Dataset Statistics:\n\n"
        result += f"• Total Properties: {len(self.df)}\n"
        result += f"• Unique Localities: {self.df['Locality'].nunique()}\n"
        
        if 'Property_Type' in self.df.columns:
            result += f"\nBy Property Type:\n"
            for ptype, count in self.df['Property_Type'].value_counts().items():
                result += f"• {ptype}: {count}\n"
        
        return result


if __name__ == "__main__":
    # Test the Q&A system
    qa = PropertyQASystem()
    
    print("="*80)
    print("PROPERTY Q&A SYSTEM TEST")
    print("="*80)
    
    test_questions = [
        "What are the cheapest properties?",
        "Show me the average price",
        "Which are the best localities?",
        "Tell me about BHK distribution"
    ]
    
    for question in test_questions:
        print(f"\n❓ Question: {question}")
        print(qa.answer_question(question))
        print("-"*80)
