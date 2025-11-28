"""
Property Brochure Generator using Ollama (Local LLM)
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

class PropertyBrochureGenerator:
    """Generate detailed property brochures using Ollama Local LLM"""
    
    def __init__(self, use_ollama: bool = True, ollama_model: str = "llama2"):
        """
        Initialize the brochure generator with Ollama
        
        Args:
            use_ollama: If True, use Ollama for AI generation (default: True)
            ollama_model: Model to use (default: llama2, options: llama3.1, mistral)
        """
        self.use_ollama = use_ollama
        self.ollama_model = ollama_model
        self.ollama_url = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')
        
        # Check if Ollama is available
        if use_ollama:
            if self._check_ollama_available():
                print("🏠 Using Local Ollama (100% Private, No API needed!)")
                print(f"   Model: {ollama_model}")
            else:
                print("⚠️  Warning: Ollama not running!")
                print("\n💡 To start Ollama:")
                print("   1. Make sure Ollama is installed: https://ollama.ai/")
                print("   2. Add to PATH: $env:PATH += ';$env:LOCALAPPDATA\\Programs\\Ollama'")
                print("   3. Check models: ollama list")
                print("   4. If no models: ollama pull llama2")
                print("\n🔄 Falling back to template mode...")
                self.use_ollama = False
    
    def _check_ollama_available(self) -> bool:
        """Check if Ollama is running locally"""
        try:
            import requests
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def _generate_with_ollama(self, prompt: str, max_length: int = 500) -> str:
        """Generate text using Ollama Local LLM"""
        try:
            import requests
            
            # Use Local Ollama
            API_URL = f"{self.ollama_url}/api/generate"
            
            payload = {
                "model": self.ollama_model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": max_length,
                    "top_p": 0.9
                }
            }
            
            response = requests.post(API_URL, json=payload, timeout=90)
            
            if response.status_code == 200:
                result = response.json()
                content = result.get('response', '')
                if content and len(content.strip()) > 10:
                    return content.strip()
                return ""
            else:
                print(f"⚠️  Ollama Error: Status {response.status_code}")
                return ""
            
        except requests.exceptions.Timeout:
            print("⚠️  Ollama timeout (model might be slow)")
            return ""
        except requests.exceptions.ConnectionError:
            print("⚠️  Ollama connection failed - is it running?")
            return ""
        except ImportError:
            print("⚠️  'requests' module not found")
            return ""
        except Exception as e:
            print(f"⚠️  Ollama error: {str(e)[:50]}")
            return ""
    
    def _generate_with_template(self, prompt: str, property_data: Dict = None) -> str:
        """Fallback template-based generation - property-specific"""
        # This shouldn't be called if templates are working properly
        # Return empty string to use the detailed templates in generate_detailed_brochure
        return ""
    
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
        import random
        
        # Track if AI was actually used
        ai_used = False
        
        # Get additional context if available
        raw_json = property_data.get('Raw_JSON', '')
        description = property_data.get('Description', '')
        context = f"\nAdditional Details: {raw_json[:500]}" if raw_json and len(str(raw_json)) > 50 else ""
        
        # 1. Overview Section - Generate varied descriptions
        
        # Vary the opening phrase
        openings = [
            f"Presenting a {furnishing.lower()} {bhk} BHK {property_type}",
            f"An elegant {bhk} BHK {property_type}",
            f"This spacious {furnishing.lower()} {bhk} BHK home",
            f"A well-designed {bhk} bedroom {property_type}",
            f"Welcome to this {furnishing.lower()} {bhk} BHK residence"
        ]
        
        # Vary the locality description
        locality_desc = {
            'Tier 1': ['prestigious', 'prime', 'sought-after', 'upscale', 'premium'],
            'Tier 2': ['thriving', 'well-connected', 'developing', 'promising', 'growing'],
            'Tier 3': ['emerging', 'value-focused', 'budget-friendly', 'upcoming', 'accessible']
        }
        tier_key = 'Tier 1' if 'Tier 1' in tier else ('Tier 2' if 'Tier 2' in tier else 'Tier 3')
        loc_adj = random.choice(locality_desc[tier_key])
        
        # Vary the value proposition
        value_phrases = [
            f"offers exceptional value at ₹{price} Lakhs",
            f"is priced attractively at ₹{price} Lakhs",
            f"comes at ₹{price} Lakhs",
            f"represents great value at ₹{price} Lakhs",
            f"is available for ₹{price} Lakhs"
        ]
        
        overview_template = (
            f"{random.choice(openings)} in {locality}, a {loc_adj} neighborhood in Ahmedabad. "
            f"Spread across {area} sqft, this property {random.choice(value_phrases)}."
        )
        
        if self.use_ollama:
            prompt = f"""Write a unique, compelling property overview (2-3 sentences) for this real estate listing:

Property: {bhk} BHK {property_type} in {locality}, Ahmedabad
Price: ₹{price} Lakhs | Area: {area} sqft | Furnishing: {furnishing}
Locality Tier: {tier}
Status: {'Under Construction' if under_construction else 'Ready to Move'}{context}

Write a professional, buyer-focused overview highlighting what makes this property special. Be specific and unique."""
            ai_result = self._generate_with_ollama(prompt, max_length=150)
            if ai_result:
                brochure['overview'] = ai_result
                ai_used = True
            else:
                brochure['overview'] = overview_template
        else:
            brochure['overview'] = overview_template
        
        # 2. Key Highlights
        highlights_template = f"""
• Spacious {bhk} BHK configuration with {area} sqft
• Located in {locality} ({tier})
• {furnishing} with modern fittings
• {amenities_count} premium amenities included
• Competitive pricing at ₹{price} Lakhs (₹{price_per_sqft:.0f}/sqft)
• {'Ready to move in' if not under_construction else 'Under construction - attractive pre-launch pricing'}
"""
        
        if self.use_ollama:
            prompt = f"""List 6 key highlights for this property (bullet points):
Property: {bhk} BHK, {area} sqft, {property_type}
Price: ₹{price} Lakhs (₹{price_per_sqft:.0f}/sqft)
Location: {locality} ({tier})
Furnishing: {furnishing}
Amenities: {amenities_count}
Status: {'Under Construction' if under_construction else 'Ready to Move'}

Key Highlights:"""
            ai_result = self._generate_with_ollama(prompt, max_length=200)
            if ai_result:
                brochure['highlights'] = ai_result
                ai_used = True
            else:
                brochure['highlights'] = highlights_template
        else:
            brochure['highlights'] = highlights_template
        
        # 3. Location Advantages
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
        location_template = '\n'.join(location_benefits.get(tier_key, location_benefits['Tier 2']))
        
        if self.use_ollama:
            prompt = f"""Describe location advantages of {locality}, Ahmedabad (3-4 points):
Locality Tier: {tier}
Property Type: {property_type}

Location Advantages:"""
            ai_result = self._generate_with_ollama(prompt, max_length=200)
            if ai_result:
                brochure['location'] = ai_result
                ai_used = True
            else:
                brochure['location'] = location_template
        else:
            brochure['location'] = location_template
        
        # 4. Amenities Details
        if self.use_ollama:
            prompt = f"""List typical amenities for a {property_type} with {amenities_count} amenities (bullet points):

Amenities:"""
            ai_result = self._generate_with_ollama(prompt, max_length=150)
            if ai_result:
                brochure['amenities'] = ai_result
                ai_used = True
        
        if not self.use_ollama or not brochure.get('amenities'):
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
        
        # 5. Investment Analysis - Generate varied analysis
        roi_phrases = {
            'Tier 1': [
                'strong capital appreciation and premium rental yields',
                'excellent investment potential with high returns',
                'robust appreciation prospects in an established market',
                'premium returns and strong resale value'
            ],
            'Tier 2': [
                'solid growth potential with developing infrastructure',
                'promising appreciation in an emerging locality',
                'balanced investment opportunity with steady returns',
                'good capital gains as the area develops'
            ],
            'Tier 3': [
                'high ROI potential in an undervalued market',
                'exceptional value with significant upside',
                'attractive entry point for long-term investors',
                'strong future growth as infrastructure improves'
            ]
        }
        tier_key = 'Tier 1' if 'Tier 1' in tier else ('Tier 2' if 'Tier 2' in tier else 'Tier 3')
        
        # Vary the market positioning
        market_phrases = [
            f"At ₹{price_per_sqft:.0f} per sqft, this represents",
            f"The pricing of ₹{price_per_sqft:.0f}/sqft offers",
            f"Priced competitively at ₹{price_per_sqft:.0f} per sqft, it provides",
            f"With a rate of ₹{price_per_sqft:.0f}/sqft, buyers get"
        ]
        
        # Vary the demand statement
        bhk_int = int(float(bhk)) if str(bhk).replace('.', '').isdigit() else 3
        demand_phrases = {
            2: ['appeals to young couples and professionals', 'attracts first-time buyers and small families', 'suits working professionals and starter homes'],
            3: ['perfect for established families', 'ideal for growing families', 'suits medium-sized families well'],
            4: ['caters to large families and executives', 'appeals to affluent buyers', 'targets premium homebuyers'],
            5: ['designed for spacious living needs', 'perfect for multi-generational families', 'suits luxury segment buyers']
        }
        bhk_key = min(max(bhk_int, 2), 5)
        
        investment_template = (
            f"This property promises {random.choice(roi_phrases[tier_key])}. "
            f"{random.choice(market_phrases)} competitive positioning in {locality}. "
            f"The {bhk} BHK layout {random.choice(demand_phrases.get(bhk_key, demand_phrases[3]))}, "
            f"ensuring consistent rental demand and resale liquidity."
        )
        
        if self.use_ollama:
            prompt = f"""Write a detailed investment analysis (3-4 sentences) for this property:

Property: {bhk} BHK {property_type}
Price: ₹{price} Lakhs | Area: {area} sqft | Price/sqft: ₹{price_per_sqft:.0f}
Location: {locality} ({tier})
Furnishing: {furnishing}
Amenities: {amenities_count}{context}

Analyze investment potential, ROI prospects, rental demand, and capital appreciation. Be specific to this property and location."""
            ai_result = self._generate_with_ollama(prompt, max_length=200)
            if ai_result:
                brochure['investment'] = ai_result
                ai_used = True
            else:
                brochure['investment'] = investment_template
        else:
            brochure['investment'] = investment_template
        
        # 6. Target Buyer Profile - Generate varied profiles
        buyer_profiles = {
            (2, 'Tier 1'): [
                'young professionals seeking a prestigious address',
                'newly married couples wanting premium amenities',
                'executives preferring central locations',
                'small families in the luxury segment'
            ],
            (2, 'Tier 2'): [
                'working professionals balancing quality and affordability',
                'first-time homebuyers in growing localities',
                'small families seeking good connectivity',
                'young couples looking for value'
            ],
            (2, 'Tier 3'): [
                'budget-conscious first-time buyers',
                'investors seeking rental income',
                'families prioritizing affordability',
                'starter home seekers'
            ],
            (3, 'Tier 1'): [
                'established families wanting luxury living',
                'senior executives seeking premium comfort',
                'families prioritizing top-tier amenities',
                'affluent buyers in prime locations'
            ],
            (3, 'Tier 2'): [
                'growing families needing more space',
                'middle-income families in developing areas',
                'families seeking balanced value',
                'buyers wanting good infrastructure'
            ],
            (3, 'Tier 3'): [
                'large families on a budget',
                'value-focused homebuyers',
                'families seeking spacious affordable homes',
                'investors eyeing appreciation'
            ],
            (4, 'Tier 1'): [
                'high-net-worth individuals',
                'luxury home seekers',
                'large families wanting premium amenities',
                'business owners and top executives'
            ],
            (4, 'Tier 2'): [
                'affluent families needing extra space',
                'multi-generational families',
                'successful professionals',
                'families wanting spacious living'
            ],
            (4, 'Tier 3'): [
                'extended families seeking value',
                'investors in emerging markets',
                'buyers wanting maximum space per rupee',
                'families prioritizing size over location'
            ]
        }
        
        bhk_int = int(float(bhk)) if str(bhk).replace('.', '').isdigit() else 3
        bhk_key = min(max(bhk_int, 2), 4)
        tier_key = 'Tier 1' if 'Tier 1' in tier else ('Tier 2' if 'Tier 2' in tier else 'Tier 3')
        
        profile = random.choice(buyer_profiles.get((bhk_key, tier_key), buyer_profiles[(3, 'Tier 2')]))
        
        # Vary the reasoning
        reasons = [
            f"With {bhk} bedrooms and {furnishing.lower()} interiors in {locality}, it matches their lifestyle needs perfectly",
            f"The {area} sqft layout in {locality}'s {'premium' if 'Tier 1' in tier else 'developing'} setting aligns with their requirements",
            f"Its {locality} location combined with {furnishing.lower()} status offers exactly what they're looking for",
            f"The property's configuration and {locality}'s infrastructure cater specifically to their preferences"
        ]
        
        target_buyers_template = f"Best suited for {profile}. {random.choice(reasons)}."
        
        if self.use_ollama:
            prompt = f"""Identify the ideal buyer profile for this property (2-3 sentences):

Property: {bhk} BHK {property_type}
Price: ₹{price} Lakhs | Area: {area} sqft
Location: {locality} ({tier})
Furnishing: {furnishing}
Amenities: {amenities_count}

Describe who would benefit most from this property. Be specific about demographics, lifestyle, and needs."""
            ai_result = self._generate_with_ollama(prompt, max_length=150)
            if ai_result:
                brochure['target_buyers'] = ai_result
                ai_used = True
            else:
                brochure['target_buyers'] = target_buyers_template
        else:
            brochure['target_buyers'] = target_buyers_template
        
        # Mark whether AI was successfully used for content generation
        brochure['ai_generated'] = ai_used
        
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
