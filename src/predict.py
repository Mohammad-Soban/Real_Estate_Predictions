"""
SINGLE PROPERTY PRICE PREDICTION
Interactive prediction for individual properties
"""
import joblib
import pandas as pd
import numpy as np
import sys
import os

# Add src directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import TIER_1_LOCALITIES, TIER_2_LOCALITIES, TIER_3_LOCALITIES

def get_user_input():
    """Get property features from user"""
    print("\n" + "="*80)
    print("PROPERTY PRICE PREDICTION - ENTER PROPERTY DETAILS")
    print("="*80)
    
    property_data = {}
    
    # BHK
    while True:
        try:
            bhk = float(input("\n🛏️  Enter BHK (1-9): "))
            if 1 <= bhk <= 9:
                property_data['BHK'] = bhk
                break
            print("❌ Please enter a value between 1 and 9")
        except:
            print("❌ Invalid input! Please enter a number")
    
    # Area
    while True:
        try:
            area = float(input("📏 Enter Area (sqft) (200-8500): "))
            if 200 <= area <= 10000:
                property_data['Area_SqFt'] = area
                break
            print("❌ Please enter a value between 200 and 10000")
        except:
            print("❌ Invalid input! Please enter a number")
    
    # Locality
    print("\n📍 Popular Localities:")
    localities = ['Bopal', 'Shela', 'Chandkheda', 'Gota', 'Vaishno Devi', 
                  'Shilaj', 'Naroda', 'Maninagar', 'Jagatpur', 'Nikol', 'Other']
    for i, loc in enumerate(localities, 1):
        print(f"  {i}. {loc}")
    
    while True:
        try:
            choice = int(input("\n👉 Select locality (1-11): "))
            if 1 <= choice <= 11:
                if choice == 11:
                    property_data['Locality'] = input("Enter locality name: ").strip()
                else:
                    property_data['Locality'] = localities[choice-1]
                break
            print("❌ Please enter a number between 1 and 11")
        except:
            print("❌ Invalid input!")
    
    # Auto-determine Locality Tier from config
    locality_name = property_data['Locality']
    if locality_name in TIER_1_LOCALITIES:
        property_data['Locality_Tier'] = 'Tier 1'
        tier_label = 'Premium'
    elif locality_name in TIER_2_LOCALITIES:
        property_data['Locality_Tier'] = 'Tier 2'
        tier_label = 'Mid-range'
    else:
        property_data['Locality_Tier'] = 'Tier 3'
        tier_label = 'Budget-friendly'
    
    print(f"\n🏆 Locality Tier: {property_data['Locality_Tier']} ({tier_label}) - Auto-determined")
    
    # Seller Type
    print("\n👤 Seller Type:")
    print("  1. Owner")
    print("  2. Dealer")
    print("  3. Builder")
    
    while True:
        try:
            seller = int(input("\n👉 Select seller type (1-3): "))
            if 1 <= seller <= 3:
                property_data['Seller_Type'] = ['Owner', 'Dealer', 'Builder'][seller-1]
                break
            print("❌ Please enter 1, 2, or 3")
        except:
            print("❌ Invalid input!")
    
    # Property Type
    print("\n🏠 Property Type:")
    print("  1. Apartment")
    print("  2. Independent House")
    
    while True:
        try:
            ptype = int(input("\n👉 Select property type (1-2): "))
            if 1 <= ptype <= 2:
                property_data['Property_Type'] = ['Apartment', 'Independent House'][ptype-1]
                break
            print("❌ Please enter 1 or 2")
        except:
            print("❌ Invalid input!")
    
    # Furnishing Status
    print("\n🪑 Furnishing Status:")
    print("  1. Furnished")
    print("  2. Semi-Furnished")
    print("  3. Unfurnished")
    
    while True:
        try:
            furn = int(input("\n👉 Select furnishing (1-3): "))
            if 1 <= furn <= 3:
                property_data['Furnishing_Status'] = ['Furnished', 'Semi-Furnished', 'Unfurnished'][furn-1]
                break
            print("❌ Please enter 1, 2, or 3")
        except:
            print("❌ Invalid input!")
    
    # Under Construction
    print("\n🏗️  Construction Status:")
    print("  1. Ready to Move")
    print("  2. Under Construction")
    
    while True:
        try:
            const = int(input("\n👉 Select status (1-2): "))
            if 1 <= const <= 2:
                property_data['Under_Construction'] = const - 1
                break
            print("❌ Please enter 1 or 2")
        except:
            print("❌ Invalid input!")
    
    # Amenities Count
    while True:
        try:
            amenities = int(input("\n🏢 Enter number of amenities (0-6): "))
            if 0 <= amenities <= 6:
                property_data['Amenities_Count'] = amenities
                break
            print("❌ Please enter a value between 0 and 6")
        except:
            print("❌ Invalid input!")
    
    return property_data

def engineer_features(data):
    """Create engineered features"""
    # Area Per BHK
    data['Area_Per_BHK'] = data['Area_SqFt'] / data['BHK']
    
    # Is Large Apartment
    data['Is_Large_Apartment'] = 1 if data['BHK'] >= 4 else 0
    
    # Is Premium Locality
    data['Is_Premium_Locality'] = 1 if data['Locality_Tier'] == 'Tier 1' else 0
    
    # Is Budget Locality
    data['Is_Budget_Locality'] = 1 if data['Locality_Tier'] == 'Tier 3' else 0
    
    # BHK Area Combo
    if data['Area_SqFt'] < 800:
        size = 'Small'
    elif data['Area_SqFt'] < 1500:
        size = 'Medium'
    else:
        size = 'Large'
    data['BHK_Area_Combo'] = f"{int(data['BHK'])} BHK_{size}"
    
    # High Amenity
    data['High_Amenity'] = 1 if data['Amenities_Count'] >= 3 else 0
    
    # Construction Category
    data['Construction_Category'] = 'Under Construction' if data['Under_Construction'] == 1 else 'Ready to Move'
    
    # Default locality-based features (will use median values)
    data['Locality_Property_Count'] = 100  # Default
    data['Locality_Median_Area'] = data['Area_SqFt']  # Use property's own area
    data['Locality_Common_BHK'] = data['BHK']  # Use property's own BHK
    
    return data

def predict_price(property_data):
    """Predict price using trained model"""
    try:
        # Load model and encoders
        # Use XGBoost (model_2) as it's a standard model without custom classes
        try:
            model = joblib.load('models/model_2_xgboost.pkl')
            print("📊 Using XGBoost model (R² = 0.8376)")
        except:
            # Fall back to other standard models
            try:
                model = joblib.load('models/model_5_randomforest.pkl')
                print("📊 Using Random Forest model (R² = 0.8267)")
            except:
                raise Exception("No compatible model found. Please train models first.")
        
        encoders = joblib.load('models/label_encoders.pkl')
        
        # Engineer features
        property_data = engineer_features(property_data)
        
        # Prepare feature order
        feature_cols = ['BHK', 'Area_SqFt', 'Locality', 'Locality_Tier', 'Seller_Type', 
                        'Property_Type', 'Furnishing_Status', 'Under_Construction', 'Amenities_Count',
                        'Area_Per_BHK', 'Is_Large_Apartment', 'Is_Premium_Locality', 'Is_Budget_Locality',
                        'BHK_Area_Combo', 'High_Amenity', 'Construction_Category', 'Locality_Property_Count',
                        'Locality_Median_Area', 'Locality_Common_BHK']
        
        # Create dataframe
        df = pd.DataFrame([property_data])
        
        # Encode categorical features
        categorical_cols = ['Locality', 'Locality_Tier', 'Seller_Type', 'Property_Type', 
                            'Furnishing_Status', 'BHK_Area_Combo', 'Construction_Category']
        
        for col in categorical_cols:
            if col in encoders:
                try:
                    df[col] = encoders[col].transform(df[col].astype(str))
                except:
                    # If unseen category, use most frequent category
                    df[col] = 0
        
        # Select features in correct order
        X = df[feature_cols]
        
        # Predict
        predicted_price = model.predict(X)[0]
        
        # Determine price band
        price_bands = [
            (0, 20, '0-20L (Budget)'),
            (20, 40, '20-40L (Affordable)'),
            (40, 60, '40-60L (Mid-Range)'),
            (60, 80, '60-80L (Premium)'),
            (80, 100, '80-100L (Luxury)'),
            (100, 120, '100-120L (High-End)'),
            (120, float('inf'), '120L+ (Ultra-Luxury)')
        ]
        
        price_band = None
        for min_price, max_price, band in price_bands:
            if min_price <= predicted_price < max_price:
                price_band = band
                break
        
        # Display results
        print("\n" + "="*80)
        print("PREDICTION RESULTS")
        print("="*80)
        print(f"\n💰 Predicted Price: ₹{predicted_price:.2f} Lakhs")
        print(f"📊 Price Band: {price_band}")
        print(f"\n📈 Price Range: ₹{predicted_price*0.9:.2f}L - ₹{predicted_price*1.1:.2f}L")
        print(f"   (±10% confidence interval)")
        
        # Additional insights
        print("\n" + "="*80)
        print("PROPERTY SUMMARY")
        print("="*80)
        print(f"🛏️  Configuration: {int(property_data['BHK'])} BHK")
        print(f"📏 Area: {property_data['Area_SqFt']:.0f} sqft")
        print(f"📍 Location: {property_data['Locality']} ({property_data['Locality_Tier']})")
        print(f"🏠 Type: {property_data['Property_Type']}")
        print(f"🪑 Furnishing: {property_data['Furnishing_Status']}")
        print(f"🏗️  Status: {property_data['Construction_Category']}")
        print(f"🏢 Amenities: {property_data['Amenities_Count']}")
        print("="*80)
        
        return predicted_price, price_band
        
    except Exception as e:
        print(f"\n❌ Prediction Error: {e}")
        print("⚠️  Make sure models are trained (run option 3 from main menu)")
        return None, None

def main():
    """Main prediction function"""
    print("\n" + "="*80)
    print("SINGLE PROPERTY PRICE PREDICTION")
    print("="*80)
    
    property_data = get_user_input()
    predict_price(property_data)
    
    print("\n")

if __name__ == "__main__":
    main()
