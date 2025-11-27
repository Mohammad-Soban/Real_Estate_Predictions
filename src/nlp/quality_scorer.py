"""
Description Quality Scorer
Scores property listings based on:
- Completeness
- Clarity
- Number of amenities mentioned
- Attractiveness
"""

import re
from typing import Dict
from .amenity_extractor import AmenityExtractor

class DescriptionQualityScorer:
    """Score the quality of property descriptions"""
    
    def __init__(self):
        self.amenity_extractor = AmenityExtractor()
        
        # Positive keywords
        self.positive_keywords = [
            'premium', 'luxury', 'spacious', 'modern', 'beautiful', 'stunning',
            'excellent', 'prime', 'elegant', 'contemporary', 'well-maintained',
            'newly', 'renovated', 'upgraded', 'quality', 'best', 'perfect'
        ]
        
        # Negative indicators (vague/unclear)
        self.vague_indicators = [
            'call for details', 'contact for', 'inquire', 'tbd', 'negotiable only'
        ]
    
    def score_completeness(self, property_data: Dict) -> float:
        """
        Score based on how complete the property information is
        Returns: 0-10 score
        """
        score = 0
        total_fields = 0
        
        # Check core fields
        core_fields = ['BHK', 'Area_SqFt', 'Price_Lakhs', 'Locality', 'Property_Type']
        for field in core_fields:
            total_fields += 2  # Weight core fields more
            if field in property_data and property_data[field] and str(property_data[field]) != 'nan':
                score += 2
        
        # Check additional fields
        additional_fields = ['Furnishing_Status', 'Seller_Type', 'Under_Construction', 'Amenities_Count']
        for field in additional_fields:
            total_fields += 1
            if field in property_data and property_data[field] and str(property_data[field]) != 'nan':
                score += 1
        
        # Normalize to 10
        return (score / total_fields) * 10 if total_fields > 0 else 0
    
    def score_clarity(self, description: str) -> float:
        """
        Score based on clarity of description
        Returns: 0-10 score
        """
        if not description or not isinstance(description, str):
            return 0
        
        score = 0
        description_lower = description.lower()
        
        # Length check (not too short, not too long)
        word_count = len(description.split())
        if 20 <= word_count <= 200:
            score += 3
        elif 10 <= word_count < 20 or 200 < word_count <= 300:
            score += 1.5
        elif word_count < 10:
            score += 0.5
        
        # Has proper sentences
        if '. ' in description or '! ' in description:
            score += 2
        
        # Not too many caps (not shouting)
        caps_ratio = sum(1 for c in description if c.isupper()) / len(description) if len(description) > 0 else 0
        if caps_ratio < 0.3:
            score += 2
        
        # Contains numbers (specific details)
        if any(char.isdigit() for char in description):
            score += 1
        
        # Not vague
        vague_count = sum(1 for indicator in self.vague_indicators if indicator in description_lower)
        if vague_count == 0:
            score += 2
        elif vague_count == 1:
            score += 1
        
        return min(score, 10)
    
    def score_amenities(self, description: str) -> float:
        """
        Score based on number of amenities mentioned
        Returns: 0-10 score
        """
        if not description:
            return 0
        
        features = self.amenity_extractor.extract_all_features(description)
        
        amenity_count = features['amenities']['count']
        proximity_count = features['proximity']['count']
        
        total_features = amenity_count + proximity_count
        
        # 6+ features = full score
        if total_features >= 6:
            return 10
        elif total_features >= 4:
            return 8
        elif total_features >= 2:
            return 6
        elif total_features == 1:
            return 4
        else:
            return 2
    
    def score_attractiveness(self, description: str) -> float:
        """
        Score based on how attractive/appealing the description is
        Returns: 0-10 score
        """
        if not description or not isinstance(description, str):
            return 0
        
        score = 0
        description_lower = description.lower()
        
        # Positive keywords count
        positive_count = sum(1 for keyword in self.positive_keywords if keyword in description_lower)
        score += min(positive_count * 1.5, 5)  # Max 5 points
        
        # Has selling points
        features = self.amenity_extractor.extract_selling_points(description)
        selling_points = features['count']
        score += min(selling_points * 1, 3)  # Max 3 points
        
        # Good formatting (bullet points, paragraphs)
        if '\n' in description or '•' in description or '*' in description:
            score += 2
        
        return min(score, 10)
    
    def calculate_overall_score(self, property_data: Dict, description: str = None) -> Dict:
        """
        Calculate overall quality score
        Returns: Dict with all scores and overall rating
        """
        # Get description from property_data if not provided
        if description is None:
            description = property_data.get('Description', '') or property_data.get('Title', '')
        
        completeness = self.score_completeness(property_data)
        clarity = self.score_clarity(description)
        amenities = self.score_amenities(description)
        attractiveness = self.score_attractiveness(description)
        
        # Weighted average (completeness is most important)
        overall = (
            completeness * 0.35 +
            clarity * 0.25 +
            amenities * 0.20 +
            attractiveness * 0.20
        )
        
        # Determine rating
        if overall >= 8:
            rating = "Excellent"
        elif overall >= 6:
            rating = "Good"
        elif overall >= 4:
            rating = "Fair"
        else:
            rating = "Poor"
        
        return {
            'completeness_score': round(completeness, 2),
            'clarity_score': round(clarity, 2),
            'amenities_score': round(amenities, 2),
            'attractiveness_score': round(attractiveness, 2),
            'overall_score': round(overall, 2),
            'rating': rating,
            'score_out_of_100': round(overall * 10, 1)
        }
    
    def get_improvement_suggestions(self, scores: Dict) -> list:
        """Get suggestions to improve listing quality"""
        suggestions = []
        
        if scores['completeness_score'] < 7:
            suggestions.append("📋 Add missing property details (price, area, amenities)")
        
        if scores['clarity_score'] < 6:
            suggestions.append("✍️ Improve description clarity - add proper sentences and details")
        
        if scores['amenities_score'] < 6:
            suggestions.append("🏢 Mention more amenities and nearby facilities")
        
        if scores['attractiveness_score'] < 6:
            suggestions.append("⭐ Use more attractive language and highlight key selling points")
        
        if not suggestions:
            suggestions.append("✅ Great listing! All quality metrics are good")
        
        return suggestions


if __name__ == "__main__":
    # Test the scorer
    scorer = DescriptionQualityScorer()
    
    test_property = {
        'BHK': 3,
        'Area_SqFt': 1500,
        'Price_Lakhs': 75,
        'Locality': 'Bopal',
        'Property_Type': 'Apartment',
        'Furnishing_Status': 'Semi-Furnished',
        'Seller_Type': 'Owner',
        'Under_Construction': 0,
        'Amenities_Count': 4
    }
    
    test_description = """
    Luxurious 3 BHK apartment in the prime location of Bopal. 
    Spanning 1500 sqft with modern amenities including gymnasium, swimming pool, 
    24x7 security, and covered parking. Close to metro station and schools. 
    Perfect for families looking for a premium lifestyle!
    """
    
    print("="*80)
    print("DESCRIPTION QUALITY SCORER TEST")
    print("="*80)
    print(f"\nDescription:\n{test_description}")
    print("\n" + "="*80)
    print("QUALITY SCORES")
    print("="*80)
    
    scores = scorer.calculate_overall_score(test_property, test_description)
    
    print(f"\n📊 Completeness Score: {scores['completeness_score']}/10")
    print(f"📝 Clarity Score: {scores['clarity_score']}/10")
    print(f"🏢 Amenities Score: {scores['amenities_score']}/10")
    print(f"⭐ Attractiveness Score: {scores['attractiveness_score']}/10")
    print(f"\n🎯 Overall Score: {scores['overall_score']}/10 ({scores['score_out_of_100']}/100)")
    print(f"📈 Rating: {scores['rating']}")
    
    print("\n" + "="*80)
    print("IMPROVEMENT SUGGESTIONS")
    print("="*80)
    suggestions = scorer.get_improvement_suggestions(scores)
    for suggestion in suggestions:
        print(f"  {suggestion}")
    print("="*80)
