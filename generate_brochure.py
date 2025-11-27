"""
Interactive Property Brochure Generator
Uses HuggingFace API to generate detailed, professional property brochures
"""

import sys
import pandas as pd
from src.nlp.brochure_generator import PropertyBrochureGenerator

def print_header():
    """Print application header"""
    print("\n" + "=" * 80)
    print(" " * 15 + "🏠 PROPERTY BROCHURE GENERATOR")
    print(" " * 20 + "Powered by HuggingFace AI")
    print("=" * 80)

def get_property_data_from_user():
    """Get property details from user input"""
    print("\n📋 Enter Property Details:")
    print("-" * 80)
    
    property_data = {}
    
    try:
        property_data['BHK'] = int(input("Number of BHK (1/2/3/4/5): ") or "3")
        property_data['Area_SqFt'] = int(input("Area in sqft (e.g., 1500): ") or "1500")
        property_data['Locality'] = input("Locality (e.g., Bopal): ") or "Bopal"
        property_data['Price_Lakhs'] = float(input("Price in Lakhs (e.g., 75): ") or "75")
        
        print("\nProperty Type:")
        print("  1. Apartment")
        print("  2. Independent House")
        print("  3. Villa")
        pt = input("Select (1-3) [default: 1]: ") or "1"
        property_types = {"1": "Apartment", "2": "Independent House", "3": "Villa"}
        property_data['Property_Type'] = property_types.get(pt, "Apartment")
        
        print("\nFurnishing Status:")
        print("  1. Furnished")
        print("  2. Semi-Furnished")
        print("  3. Unfurnished")
        fs = input("Select (1-3) [default: 2]: ") or "2"
        furnishing = {"1": "Furnished", "2": "Semi-Furnished", "3": "Unfurnished"}
        property_data['Furnishing_Status'] = furnishing.get(fs, "Semi-Furnished")
        
        property_data['Amenities_Count'] = int(input("\nNumber of amenities (0-10) [default: 4]: ") or "4")
        
        print("\nLocality Tier:")
        print("  1. Tier 1 (Premium)")
        print("  2. Tier 2 (Mid-Range)")
        print("  3. Tier 3 (Budget-Friendly)")
        lt = input("Select (1-3) [default: 1]: ") or "1"
        tiers = {"1": "Tier 1", "2": "Tier 2", "3": "Tier 3"}
        property_data['Locality_Tier'] = tiers.get(lt, "Tier 1")
        
        print("\nSeller Type:")
        print("  1. Owner")
        print("  2. Builder")
        print("  3. Dealer")
        st = input("Select (1-3) [default: 1]: ") or "1"
        sellers = {"1": "Owner", "2": "Builder", "3": "Dealer"}
        property_data['Seller_Type'] = sellers.get(st, "Owner")
        
        uc = input("\nUnder Construction? (y/n) [default: n]: ") or "n"
        property_data['Under_Construction'] = 1 if uc.lower() == 'y' else 0
        
        return property_data
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Using default values...")
        return get_default_property()

def get_default_property():
    """Return default property for testing"""
    return {
        'BHK': 3,
        'Area_SqFt': 1500,
        'Locality': 'Bopal',
        'Price_Lakhs': 75,
        'Property_Type': 'Apartment',
        'Furnishing_Status': 'Semi-Furnished',
        'Amenities_Count': 4,
        'Locality_Tier': 'Tier 1',
        'Seller_Type': 'Owner',
        'Under_Construction': 0
    }

def get_property_from_dataset():
    """Load a property from the dataset"""
    try:
        df = pd.read_csv('data/cleaned/cleaned_data.csv')
        df = df[df['Locality'] != 'Unknown']
        
        print("\n📊 Loading properties from dataset...")
        print(f"Total properties available: {len(df)}")
        
        # Show top localities
        top_localities = df['Locality'].value_counts().head(10)
        print("\nTop 10 Localities:")
        for i, (loc, count) in enumerate(top_localities.items(), 1):
            print(f"  {i}. {loc} ({count} properties)")
        
        # Ask for selection
        choice = input("\nSelect property by:\n  1. Random\n  2. Specific locality\n  3. Index\nChoice [1]: ") or "1"
        
        if choice == "1":
            # Random property
            sample = df.sample(1).iloc[0]
        elif choice == "2":
            # By locality
            loc = input("Enter locality name: ")
            loc_df = df[df['Locality'].str.contains(loc, case=False, na=False)]
            if len(loc_df) > 0:
                sample = loc_df.sample(1).iloc[0]
            else:
                print("Locality not found, using random...")
                sample = df.sample(1).iloc[0]
        else:
            # By index
            idx = int(input("Enter index (0-{}): ".format(len(df)-1)) or "0")
            sample = df.iloc[idx]
        
        property_data = {
            'BHK': sample.get('BHK', 3),
            'Area_SqFt': sample.get('Area_SqFt', 1500),
            'Locality': sample.get('Locality', 'Unknown'),
            'Price_Lakhs': sample.get('Price_Lakhs', 0),
            'Property_Type': sample.get('Property_Type', 'Apartment'),
            'Furnishing_Status': sample.get('Furnishing_Status', 'Semi-Furnished'),
            'Amenities_Count': sample.get('Amenities_Count', 0),
            'Locality_Tier': sample.get('Locality_Tier', 'Tier 2'),
            'Seller_Type': sample.get('Seller_Type', 'Owner'),
            'Under_Construction': sample.get('Under_Construction', 0)
        }
        
        print("\n✅ Property loaded from dataset")
        return property_data
        
    except Exception as e:
        print(f"\n❌ Error loading dataset: {e}")
        print("Using default property...")
        return get_default_property()

def main():
    """Main brochure generator interface"""
    print_header()
    
    print("\n🔑 HuggingFace API Setup:")
    print("-" * 80)
    print("To generate AI-powered brochures, you need a HuggingFace API key.")
    print("\n📝 How to get your API key:")
    print("  1. Go to https://huggingface.co/")
    print("  2. Sign up / Log in")
    print("  3. Go to Settings → Access Tokens")
    print("  4. Create a new token (Read permission)")
    print("  5. Copy the token (starts with 'hf_')")
    print("\n💡 Set your API key:")
    print("  PowerShell: $env:HUGGINGFACE_API_KEY='your_token'")
    print("  CMD: set HUGGINGFACE_API_KEY=your_token")
    print("  Linux/Mac: export HUGGINGFACE_API_KEY='your_token'")
    print("\n⚠️  Note: Without API key, template-based generation will be used.")
    
    input("\n⏸️  Press Enter to continue...")
    
    while True:
        print("\n" + "=" * 80)
        print("📋 SELECT INPUT METHOD:")
        print("=" * 80)
        print("  1. Enter property details manually")
        print("  2. Load from dataset")
        print("  3. Use default demo property")
        print("  0. Exit")
        
        choice = input("\n👉 Your choice (0-3): ").strip()
        
        if choice == '0':
            print("\n👋 Goodbye!")
            break
        elif choice == '1':
            property_data = get_property_data_from_user()
        elif choice == '2':
            property_data = get_property_from_dataset()
        elif choice == '3':
            property_data = get_default_property()
            print("\n✅ Using default demo property")
        else:
            print("\n❌ Invalid choice!")
            continue
        
        # Show property summary
        print("\n" + "=" * 80)
        print("📋 PROPERTY SUMMARY:")
        print("=" * 80)
        for key, value in property_data.items():
            print(f"  {key:<25}: {value}")
        
        confirm = input("\n✅ Generate brochure for this property? (y/n) [y]: ") or "y"
        if confirm.lower() != 'y':
            continue
        
        # Initialize generator
        print("\n" + "=" * 80)
        print("🤖 Initializing AI Brochure Generator...")
        print("=" * 80)
        
        generator = PropertyBrochureGenerator(use_hf_api=True)
        
        # Generate brochure
        print("\n⏳ Generating detailed brochure...")
        print("⏳ This may take 10-30 seconds with HuggingFace API...")
        
        try:
            brochure = generator.generate_detailed_brochure(property_data)
            
            # Display brochure
            print("\n" + generator.format_brochure_text(brochure))
            
            # Ask to save
            save = input("\n💾 Save brochure as HTML? (y/n) [y]: ") or "y"
            if save.lower() == 'y':
                filename = input("Enter filename [property_brochure.html]: ") or "property_brochure.html"
                if not filename.endswith('.html'):
                    filename += '.html'
                
                generator.save_brochure_html(brochure, filename)
                print(f"\n✅ Brochure saved successfully!")
                print(f"📂 Location: {filename}")
                print(f"💡 Open in browser to view")
            
            # Ask to save as text
            save_txt = input("\n💾 Save brochure as text file? (y/n) [n]: ") or "n"
            if save_txt.lower() == 'y':
                txt_filename = input("Enter filename [property_brochure.txt]: ") or "property_brochure.txt"
                if not txt_filename.endswith('.txt'):
                    txt_filename += '.txt'
                
                with open(txt_filename, 'w', encoding='utf-8') as f:
                    f.write(generator.format_brochure_text(brochure))
                
                print(f"✅ Text brochure saved: {txt_filename}")
        
        except Exception as e:
            print(f"\n❌ Error generating brochure: {e}")
            print("💡 Make sure your HuggingFace API key is set correctly")
        
        another = input("\n🔄 Generate another brochure? (y/n) [y]: ") or "y"
        if another.lower() != 'y':
            print("\n👋 Thank you for using Property Brochure Generator!")
            break

if __name__ == "__main__":
    main()
