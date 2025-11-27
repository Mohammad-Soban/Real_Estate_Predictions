"""
Amenity & Feature Extraction Module
Extracts amenities, proximity info, keywords from property descriptions
Uses simple NLP techniques with pattern matching
"""

import re
import json
from typing import Dict, List, Set

class AmenityExtractor:
    """Extract amenities and features from property descriptions"""
    
    def __init__(self):
        # Define amenity keywords
        self.amenities = {
            'gym': ['gym', 'gymnasium', 'fitness', 'workout'],
            'swimming_pool': ['pool', 'swimming', 'swim'],
            'parking': ['parking', 'car park', 'covered parking', 'parking space'],
            'security': ['security', '24x7 security', 'gated', 'cctv'],
            'garden': ['garden', 'lawn', 'green space', 'landscaped'],
            'clubhouse': ['clubhouse', 'club house', 'community hall'],
            'lift': ['lift', 'elevator'],
            'power_backup': ['power backup', 'generator', 'backup power'],
            'water_supply': ['water supply', '24x7 water', 'water tank'],
            'kids_play_area': ['play area', 'playground', 'kids area', 'children play'],
            'intercom': ['intercom', 'video door'],
            'fire_safety': ['fire safety', 'fire alarm', 'sprinkler'],
            'visitors_parking': ['visitor parking', 'guest parking'],
            'maintenance_staff': ['maintenance', 'housekeeping', 'staff']
        }
        
        # Proximity keywords
        self.proximity = {
            'metro': ['metro', 'metro station', 'subway'],
            'hospital': ['hospital', 'medical', 'clinic', 'healthcare'],
            'school': ['school', 'college', 'university', 'education'],
            'mall': ['mall', 'shopping', 'shopping center'],
            'market': ['market', 'bazaar', 'shopping area'],
            'airport': ['airport', 'international airport'],
            'railway': ['railway', 'train station', 'railway station'],
            'highway': ['highway', 'express', 'expressway', 'main road']
        }
        
        # Selling keywords
        self.selling_points = {
            'spacious': ['spacious', 'large', 'big', 'huge'],
            'modern': ['modern', 'contemporary', 'latest', 'new'],
            'luxury': ['luxury', 'premium', 'high-end', 'luxurious'],
            'affordable': ['affordable', 'budget', 'economical', 'value'],
            'prime_location': ['prime location', 'prime', 'central', 'heart of'],
            'peaceful': ['peaceful', 'quiet', 'serene', 'calm'],
            'well_connected': ['well connected', 'connectivity', 'accessible'],
            'family_friendly': ['family', 'families', 'family-friendly']
        }
        
        # View/Facing keywords
        self.views = {
            'park_view': ['park view', 'facing park', 'park facing'],
            'road_facing': ['road facing', 'main road', 'road view'],
            'corner': ['corner', 'corner plot', 'corner property'],
            'east_facing': ['east facing', 'east', 'morning sun'],
            'north_facing': ['north facing', 'north'],
            'vastu': ['vastu', 'vastu compliant', 'as per vastu']
        }
    
    def extract_amenities(self, description: str) -> Dict[str, List[str]]:
        """Extract all amenities from description"""
        if not description or not isinstance(description, str):
            return {'amenities': [], 'count': 0}
        
        description_lower = description.lower()
        found_amenities = []
        
        for amenity_name, keywords in self.amenities.items():
            for keyword in keywords:
                if keyword in description_lower:
                    found_amenities.append(amenity_name.replace('_', ' ').title())
                    break
        
        return {
            'amenities': list(set(found_amenities)),
            'count': len(set(found_amenities))
        }
    
    def extract_proximity(self, description: str) -> Dict[str, List[str]]:
        """Extract proximity information"""
        if not description or not isinstance(description, str):
            return {'nearby': [], 'count': 0}
        
        description_lower = description.lower()
        found_proximity = []
        
        for place_type, keywords in self.proximity.items():
            for keyword in keywords:
                if keyword in description_lower:
                    found_proximity.append(place_type.replace('_', ' ').title())
                    break
        
        return {
            'nearby': list(set(found_proximity)),
            'count': len(set(found_proximity))
        }
    
    def extract_selling_points(self, description: str) -> Dict[str, List[str]]:
        """Extract selling points/keywords"""
        if not description or not isinstance(description, str):
            return {'selling_points': [], 'count': 0}
        
        description_lower = description.lower()
        found_points = []
        
        for point_name, keywords in self.selling_points.items():
            for keyword in keywords:
                if keyword in description_lower:
                    found_points.append(point_name.replace('_', ' ').title())
                    break
        
        return {
            'selling_points': list(set(found_points)),
            'count': len(set(found_points))
        }
    
    def extract_views(self, description: str) -> Dict[str, List[str]]:
        """Extract view/facing information"""
        if not description or not isinstance(description, str):
            return {'views': [], 'facing': None}
        
        description_lower = description.lower()
        found_views = []
        
        for view_name, keywords in self.views.items():
            for keyword in keywords:
                if keyword in description_lower:
                    found_views.append(view_name.replace('_', ' ').title())
                    break
        
        return {
            'views': list(set(found_views)),
            'facing': found_views[0] if found_views else None
        }
    
    def extract_all_features(self, description: str) -> Dict:
        """Extract all features at once"""
        return {
            'amenities': self.extract_amenities(description),
            'proximity': self.extract_proximity(description),
            'selling_points': self.extract_selling_points(description),
            'views': self.extract_views(description)
        }
    
    def get_feature_summary(self, description: str) -> str:
        """Get a text summary of all extracted features"""
        features = self.extract_all_features(description)
        
        summary_parts = []
        
        # Amenities
        if features['amenities']['count'] > 0:
            amenities_str = ', '.join(features['amenities']['amenities'])
            summary_parts.append(f"🏢 Amenities: {amenities_str}")
        
        # Proximity
        if features['proximity']['count'] > 0:
            proximity_str = ', '.join(features['proximity']['nearby'])
            summary_parts.append(f"📍 Nearby: {proximity_str}")
        
        # Selling Points
        if features['selling_points']['count'] > 0:
            selling_str = ', '.join(features['selling_points']['selling_points'])
            summary_parts.append(f"⭐ Highlights: {selling_str}")
        
        # Views
        if features['views']['facing']:
            summary_parts.append(f"👁️ View: {features['views']['facing']}")
        
        return '\n'.join(summary_parts) if summary_parts else "No features extracted"


if __name__ == "__main__":
    # Test the extractor
    extractor = AmenityExtractor()
    
    test_desc = """
    Luxurious 3 BHK apartment in prime location near metro station. 
    Features include gymnasium, swimming pool, 24x7 security, and covered parking.
    Close to schools and hospitals. Spacious and modern design. East facing with park view.
    Well connected to highway and airport.
    """
    
    print("="*80)
    print("AMENITY & FEATURE EXTRACTION TEST")
    print("="*80)
    print(f"\nDescription:\n{test_desc}\n")
    print("="*80)
    print("\nExtracted Features:")
    print("="*80)
    print(extractor.get_feature_summary(test_desc))
    print("="*80)
