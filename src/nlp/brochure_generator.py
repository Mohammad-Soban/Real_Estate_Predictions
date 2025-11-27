"""
Property Brochure Generator using HuggingFace API
Generates detailed, professional property brochures with:
- Property overview
- Key highlights
- Location advantages
- Amenities details
- Investment analysis
- Target buyer profile
"""

import os
import warnings
from typing import Dict, Optional
warnings.filterwarnings('ignore')

# Try to load from .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file if it exists
except ImportError:
    pass  # dotenv not installed, will use environment variables only

class PropertyBrochureGenerator:
    """Generate detailed property brochures using HuggingFace Inference API"""
    
    def __init__(self, use_hf_api: bool = True, hf_model: str = "mistralai/Mixtral-8x7B-Instruct-v0.1"):
        """
        Initialize the brochure generator
        
        Args:
            use_hf_api: If True, use HuggingFace Inference API (requires API key)
            hf_model: HuggingFace model to use (default: Mixtral-8x7B - supports text-generation)
        """
        self.use_hf_api = use_hf_api
        self.hf_model = hf_model
        self.api_key = os.environ.get('HUGGINGFACE_API_KEY', '')
        
        if use_hf_api and not self.api_key:
            print("⚠️  Warning: HUGGINGFACE_API_KEY not found")
            print("\n💡 Three ways to add your API key:")
            print("   1. Environment Variable (Recommended):")
            print("      PowerShell: $env:HUGGINGFACE_API_KEY='your_key'")
            print("      Linux/Mac: export HUGGINGFACE_API_KEY='your_key'")
            print("\n   2. .env File:")
            print("      Create .env file with: HUGGINGFACE_API_KEY=your_key")
            print("\n   3. Direct in Code:")
            print("      os.environ['HUGGINGFACE_API_KEY'] = 'your_key'")
            print("\n🔑 Get your FREE API key: https://huggingface.co/settings/tokens")
            print("\n🔄 Falling back to template mode (no API needed)...")
            self.use_hf_api = False
    
    def _generate_with_hf_api(self, prompt: str, max_length: int = 500) -> str:
        """Generate text using HuggingFace Inference API"""
        try:
            import requests
            
            API_URL = f"https://api-inference.huggingface.co/models/{self.hf_model}"
            headers = {"Authorization": f"Bearer {self.api_key}"}
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": max_length,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "do_sample": True,
                    "return_full_text": False
                }
            }
            
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                    return generated_text.strip()
                else:
                    return self._generate_with_template(prompt)
            else:
                # Silently fall back to template without printing errors
                return self._generate_with_template(prompt)
            
        except ImportError:
            print("❌ Please install: pip install requests")
            return self._generate_with_template(prompt)
        except Exception as e:
            # Silently fall back to template
            return self._generate_with_template(prompt)
    
    def _generate_with_template(self, prompt: str) -> str:
        """Fallback template-based generation"""
        return "Template-based brochure content (install HuggingFace API for AI-generated content)"
    
    def generate_detailed_brochure(self, property_data: Dict) -> Dict[str, str]:
        """
        Generate a comprehensive property brochure
        
        Args:
            property_data: Dictionary with property details
            
        Returns:
            Dictionary with brochure sections
        """
        bhk = property_data.get('BHK', 'N/A')
        area = property_data.get('Area_SqFt', 'N/A')
        locality = property_data.get('Locality', 'Unknown')
        price = property_data.get('Price_Lakhs', 'N/A')
        property_type = property_data.get('Property_Type', 'Property')
        furnishing = property_data.get('Furnishing_Status', 'Unfurnished')
        amenities_count = property_data.get('Amenities_Count', 0)
        tier = property_data.get('Locality_Tier', 'Unknown')
        seller_type = property_data.get('Seller_Type', 'Unknown')
        under_construction = property_data.get('Under_Construction', 0)
        
        # Calculate price per sqft
        price_per_sqft = (float(price) * 100000 / float(area)) if price != 'N/A' and area != 'N/A' else 0
        
        brochure = {}
        
        # 1. Overview Section
        if self.use_hf_api:
            prompt = f"""Write a compelling property overview (2-3 sentences) for:
{bhk} BHK {property_type} in {locality}, Ahmedabad
Price: ₹{price} Lakhs | Area: {area} sqft | Furnishing: {furnishing}
Tier: {tier}

Overview:"""
            brochure['overview'] = self._generate_with_hf_api(prompt, max_length=150)
        else:
            brochure['overview'] = (
                f"Discover this {furnishing.lower()} {bhk} BHK {property_type} "
                f"in {locality}, one of Ahmedabad's {'premium' if 'Tier 1' in tier else 'sought-after'} localities. "
                f"Spanning {area} sqft, this property offers excellent value at ₹{price} Lakhs."
            )
        
        # 2. Key Highlights
        if self.use_hf_api:
            prompt = f"""List 6 key highlights for this property (bullet points):
Property: {bhk} BHK, {area} sqft, {property_type}
Price: ₹{price} Lakhs (₹{price_per_sqft:.0f}/sqft)
Location: {locality} ({tier})
Furnishing: {furnishing}
Amenities: {amenities_count}
Status: {'Under Construction' if under_construction else 'Ready to Move'}

Key Highlights:"""
            brochure['highlights'] = self._generate_with_hf_api(prompt, max_length=200)
        else:
            brochure['highlights'] = f"""
• Spacious {bhk} BHK configuration with {area} sqft
• Located in {locality} ({tier})
• {furnishing} with modern fittings
• {amenities_count} premium amenities included
• Competitive pricing at ₹{price} Lakhs (₹{price_per_sqft:.0f}/sqft)
• {'Ready to move in' if not under_construction else 'Under construction - attractive pre-launch pricing'}
"""
        
        # 3. Location Advantages
        if self.use_hf_api:
            prompt = f"""Describe location advantages of {locality}, Ahmedabad (3-4 points):
Locality Tier: {tier}
Property Type: {property_type}

Location Advantages:"""
            brochure['location'] = self._generate_with_hf_api(prompt, max_length=200)
        else:
            location_benefits = {
                'Tier 1': [
                    '• Prime residential area with excellent connectivity',
                    '• Close proximity to IT hubs and business centers',
                    '• Well-developed infrastructure with metro access',
                    '• Surrounded by reputed schools, hospitals, and malls'
                ],
                'Tier 2': [
                    '• Emerging locality with strong growth potential',
                    '• Good connectivity to major city areas',
                    '• Developing infrastructure with upcoming amenities',
                    '• Mix of residential and commercial establishments'
                ],
                'Tier 3': [
                    '• Budget-friendly location with growing infrastructure',
                    '• Peaceful residential environment',
                    '• Easy access to main roads and public transport',
                    '• Value-for-money investment opportunity'
                ]
            }
            tier_key = 'Tier 1' if 'Tier 1' in tier else ('Tier 2' if 'Tier 2' in tier else 'Tier 3')
            brochure['location'] = '\n'.join(location_benefits.get(tier_key, location_benefits['Tier 2']))
        
        # 4. Amenities Details
        if self.use_hf_api:
            prompt = f"""List typical amenities for a {property_type} with {amenities_count} amenities (bullet points):

Amenities:"""
            brochure['amenities'] = self._generate_with_hf_api(prompt, max_length=150)
        else:
            common_amenities = [
                '• 24x7 Security with CCTV surveillance',
                '• Covered Car Parking',
                '• Power Backup',
                '• Water Supply',
                '• Lift/Elevator',
                '• Gymnasium',
                '• Swimming Pool',
                '• Children\'s Play Area',
                '• Clubhouse',
                '• Landscaped Gardens'
            ]
            # Select amenities based on count
            amenities_to_show = min(amenities_count + 2, len(common_amenities))
            brochure['amenities'] = '\n'.join(common_amenities[:amenities_to_show])
        
        # 5. Investment Analysis
        if self.use_hf_api:
            prompt = f"""Write investment analysis for this property (3-4 sentences):
Property: {bhk} BHK {property_type}
Price: ₹{price} Lakhs | Area: {area} sqft | Price/sqft: ₹{price_per_sqft:.0f}
Location: {locality} ({tier})

Investment Analysis:"""
            brochure['investment'] = self._generate_with_hf_api(prompt, max_length=200)
        else:
            roi_potential = {
                'Tier 1': 'high appreciation potential and strong rental demand',
                'Tier 2': 'good appreciation prospects and steady rental income',
                'Tier 3': 'excellent value proposition with future growth potential'
            }
            tier_key = 'Tier 1' if 'Tier 1' in tier else ('Tier 2' if 'Tier 2' in tier else 'Tier 3')
            
            brochure['investment'] = (
                f"This property offers {roi_potential[tier_key]}. "
                f"Priced at ₹{price_per_sqft:.0f} per sqft, it presents {'competitive' if 'Tier 1' in tier else 'attractive'} "
                f"value in the {locality} market. "
                f"The {bhk} BHK configuration appeals to {'families and professionals' if int(bhk) >= 3 else 'young professionals and small families'}, "
                f"ensuring {'strong' if 'Apartment' in property_type else 'good'} demand for resale and rentals."
            )
        
        # 6. Target Buyer Profile
        if self.use_hf_api:
            prompt = f"""Identify ideal buyer profile for this property (2-3 sentences):
Property: {bhk} BHK {property_type}
Price: ₹{price} Lakhs
Location: {locality} ({tier})

Target Buyers:"""
            brochure['target_buyers'] = self._generate_with_hf_api(prompt, max_length=150)
        else:
            buyer_profiles = {
                (2, 'Tier 1'): 'young professionals, newly married couples, or small families seeking a premium address',
                (2, 'Tier 2'): 'working professionals and small families looking for good value in a growing area',
                (2, 'Tier 3'): 'first-time homebuyers and budget-conscious families',
                (3, 'Tier 1'): 'established families seeking luxury and convenience in a prime location',
                (3, 'Tier 2'): 'growing families looking for spacious homes with good connectivity',
                (3, 'Tier 3'): 'middle-class families seeking affordable spacious homes',
                (4, 'Tier 1'): 'high-net-worth individuals and large families wanting premium luxury',
                (4, 'Tier 2'): 'affluent families seeking spacious accommodations',
                (4, 'Tier 3'): 'large families or investors looking for value properties'
            }
            
            bhk_int = int(bhk) if str(bhk).isdigit() else 3
            bhk_key = min(bhk_int, 4)
            bhk_key = max(bhk_key, 2)
            tier_key = 'Tier 1' if 'Tier 1' in tier else ('Tier 2' if 'Tier 2' in tier else 'Tier 3')
            
            profile = buyer_profiles.get((bhk_key, tier_key), 'families and individuals seeking quality housing')
            
            brochure['target_buyers'] = (
                f"This property is ideal for {profile}. "
                f"The combination of {bhk} bedrooms, {furnishing.lower()} status, and "
                f"{locality}'s {'established' if 'Tier 1' in tier else 'growing'} infrastructure makes it "
                f"perfect for those seeking {'premium comfort' if 'Tier 1' in tier else 'value and convenience'}."
            )
        
        # 7. Property Details Summary
        brochure['details'] = {
            'Property Type': property_type,
            'Configuration': f'{bhk} BHK',
            'Area': f'{area} sqft',
            'Price': f'₹{price} Lakhs',
            'Price per sqft': f'₹{price_per_sqft:.0f}',
            'Location': f'{locality}, Ahmedabad',
            'Locality Tier': tier,
            'Furnishing': furnishing,
            'Amenities': amenities_count,
            'Seller Type': seller_type,
            'Status': 'Under Construction' if under_construction else 'Ready to Move'
        }
        
        return brochure
    
    def format_brochure_text(self, brochure: Dict) -> str:
        """Format brochure as plain text"""
        output = []
        output.append("=" * 80)
        output.append(" " * 25 + "PROPERTY BROCHURE")
        output.append("=" * 80)
        output.append("")
        
        # Overview
        output.append("📋 PROPERTY OVERVIEW")
        output.append("-" * 80)
        output.append(brochure['overview'])
        output.append("")
        
        # Details
        output.append("📊 PROPERTY DETAILS")
        output.append("-" * 80)
        for key, value in brochure['details'].items():
            output.append(f"  {key:<20}: {value}")
        output.append("")
        
        # Key Highlights
        output.append("⭐ KEY HIGHLIGHTS")
        output.append("-" * 80)
        output.append(brochure['highlights'])
        output.append("")
        
        # Location
        output.append("📍 LOCATION ADVANTAGES")
        output.append("-" * 80)
        output.append(brochure['location'])
        output.append("")
        
        # Amenities
        output.append("🏢 AMENITIES & FACILITIES")
        output.append("-" * 80)
        output.append(brochure['amenities'])
        output.append("")
        
        # Investment
        output.append("💰 INVESTMENT ANALYSIS")
        output.append("-" * 80)
        output.append(brochure['investment'])
        output.append("")
        
        # Target Buyers
        output.append("👥 IDEAL FOR")
        output.append("-" * 80)
        output.append(brochure['target_buyers'])
        output.append("")
        
        output.append("=" * 80)
        output.append(" " * 20 + "Contact for Site Visits & Bookings")
        output.append("=" * 80)
        
        return "\n".join(output)
    
    def save_brochure_html(self, brochure: Dict, filename: str = 'property_brochure.html'):
        """Save brochure as HTML file"""
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Property Brochure</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .brochure {{
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 15px;
        }}
        h2 {{
            color: #2c3e50;
            margin-top: 30px;
            border-left: 4px solid #3498db;
            padding-left: 15px;
        }}
        .details {{
            background: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        .details-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }}
        .detail-item {{
            padding: 8px;
        }}
        .detail-label {{
            font-weight: bold;
            color: #34495e;
        }}
        .section {{
            margin: 25px 0;
            line-height: 1.8;
        }}
        .highlight {{
            background: #fff3cd;
            padding: 15px;
            border-left: 4px solid #ffc107;
            margin: 15px 0;
        }}
        ul {{
            list-style-type: none;
            padding-left: 0;
        }}
        ul li {{
            padding: 8px 0;
            padding-left: 30px;
            position: relative;
        }}
        ul li:before {{
            content: "✓";
            position: absolute;
            left: 0;
            color: #27ae60;
            font-weight: bold;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #3498db;
            color: #7f8c8d;
        }}
    </style>
</head>
<body>
    <div class="brochure">
        <h1>🏠 Property Brochure</h1>
        
        <div class="section">
            <h2>📋 Overview</h2>
            <p>{brochure['overview']}</p>
        </div>
        
        <div class="details">
            <h2>📊 Property Details</h2>
            <div class="details-grid">
"""
        
        for key, value in brochure['details'].items():
            html += f"""
                <div class="detail-item">
                    <span class="detail-label">{key}:</span> {value}
                </div>
"""
        
        html += f"""
            </div>
        </div>
        
        <div class="section">
            <h2>⭐ Key Highlights</h2>
            <div class="highlight">
                {brochure['highlights'].replace(chr(10), '<br>')}
            </div>
        </div>
        
        <div class="section">
            <h2>📍 Location Advantages</h2>
            {brochure['location'].replace(chr(10), '<br>')}
        </div>
        
        <div class="section">
            <h2>🏢 Amenities & Facilities</h2>
            {brochure['amenities'].replace(chr(10), '<br>')}
        </div>
        
        <div class="section">
            <h2>💰 Investment Analysis</h2>
            <p>{brochure['investment']}</p>
        </div>
        
        <div class="section">
            <h2>👥 Ideal For</h2>
            <p>{brochure['target_buyers']}</p>
        </div>
        
        <div class="footer">
            <p><strong>Contact for Site Visits & Bookings</strong></p>
            <p>Generated by RealEstateSense AI</p>
        </div>
    </div>
</body>
</html>
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Brochure saved as {filename}")
        return filename


if __name__ == "__main__":
    # Test the brochure generator
    print("=" * 80)
    print(" " * 20 + "PROPERTY BROCHURE GENERATOR TEST")
    print("=" * 80)
    
    # Sample property data
    test_property = {
        'BHK': 3,
        'Area_SqFt': 1500,
        'Locality': 'Bopal',
        'Price_Lakhs': 75,
        'Property_Type': 'Apartment',
        'Furnishing_Status': 'Semi-Furnished',
        'Amenities_Count': 5,
        'Locality_Tier': 'Tier 1',
        'Seller_Type': 'Owner',
        'Under_Construction': 0
    }
    
    print("\n📋 Property Input:")
    for key, value in test_property.items():
        print(f"  {key}: {value}")
    
    print("\n" + "=" * 80)
    print("Generating detailed brochure...")
    print("=" * 80)
    
    # Initialize generator (will use template mode if no API key)
    generator = PropertyBrochureGenerator(use_hf_api=True)
    
    # Generate brochure
    brochure = generator.generate_detailed_brochure(test_property)
    
    # Print formatted brochure
    print("\n" + generator.format_brochure_text(brochure))
    
    # Save as HTML
    html_file = generator.save_brochure_html(brochure, 'test_brochure.html')
    print(f"\n💾 HTML version saved: {html_file}")
    
    print("\n" + "=" * 80)
    print("💡 Tips:")
    print("  1. Set HUGGINGFACE_API_KEY for AI-generated content")
    print("  2. Template mode works without API (fast & free)")
    print("  3. Use save_brochure_html() for professional HTML output")
    print("=" * 80)
