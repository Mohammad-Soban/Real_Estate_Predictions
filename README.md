# Ahmedabad Real Estate Price Prediction

Complete ML pipeline for predicting property prices in Ahmedabad using XGBoost, LightGBM, and CatBoost.

## 🎯 Results

**Dataset**: 2,783 properties from 91 localities  
**Features**: 19 engineered features

| Rank | Model | R² Score | RMSE | MAE |
|------|-------|----------|------|-----|
| 🥇 #1 | **XGBoost** | **0.8357** | **27.63L** | **14.73L** |
| 🥈 #2 | CatBoost | 0.8055 | 30.07L | 18.50L |
| 🥉 #3 | LightGBM | 0.8055 | 30.07L | 18.50L |

## 📁 Project Structure

```
Capstone_Project/
├── data/
│   ├── raw/              # Scraped data (5,223 properties)
│   ├── cleaned/          # Preprocessed data (2,801 properties)
│   └── training/         # Enhanced training data (2,783 properties)
├── models/
│   ├── best_model.pkl           # Best model (XGBoost)
│   ├── model_1_xgboost.pkl      # XGBoost
│   ├── model_2_catboost.pkl     # CatBoost
│   ├── model_3_lightgbm.pkl     # LightGBM
│   └── label_encoders.pkl       # Encoders for categorical features
├── src/
│   ├── preprocessing/
│   │   ├── preprocess_simple.py    # Basic preprocessing
│   │   └── preprocess_enhanced.py  # Feature engineering
│   ├── scraping/
│   │   └── scrape_all_sources_detailed.py
│   ├── config.py
│   ├── predict.py       # Make predictions
│   └── visualize.py     # Generate charts
├── train.py             # Train all 3 models
├── run.py               # Full pipeline (scrape → preprocess → train)
└── README.md
```

## 🚀 Quick Start

### 1. Train Models (using existing data)
```bash
python train.py
```

### 2. Run Complete Pipeline (scrape + preprocess + train)
```bash
python run.py
```

### 3. Make Predictions
```python
import joblib
import pandas as pd

# Load model
model = joblib.load('models/best_model.pkl')
encoders = joblib.load('models/label_encoders.pkl')

# Prepare data (example)
data = {
    'BHK': 3,
    'Area_SqFt': 1500,
    'Locality': 'Bopal',
    'Locality_Tier': 'Tier 2',
    'Seller_Type': 'Owner',
    'Property_Type': 'Apartment',
    'Furnishing_Status': 'Semi-Furnished',
    'Under_Construction': 0,
    'Amenities_Count': 2,
    # ... add other features
}

# Encode and predict
df = pd.DataFrame([data])
for col, encoder in encoders.items():
    df[col] = encoder.transform(df[col].astype(str))

price = model.predict(df)[0]
print(f"Predicted Price: ₹{price:.2f} Lakhs")
```

## 🔧 Features (19 total)

### Core Features (9)
1. **BHK** - Number of bedrooms
2. **Area_SqFt** - Property area in square feet
3. **Locality** - Location (91 unique localities)
4. **Locality_Tier** - Tier 1 (premium) / Tier 2 / Tier 3 (budget)
5. **Seller_Type** - Owner / Dealer / Builder
6. **Property_Type** - Apartment / Independent House
7. **Furnishing_Status** - Furnished / Semi-Furnished / Unfurnished
8. **Under_Construction** - 0 (ready) / 1 (under construction)
9. **Amenities_Count** - Number of amenities (0-6)

### Engineered Features (10)
10. **Area_Per_BHK** - Area per bedroom
11. **Is_Large_Apartment** - BHK ≥ 4
12. **Is_Premium_Locality** - Tier 1 locality
13. **Is_Budget_Locality** - Tier 3 locality
14. **BHK_Area_Combo** - Combination of BHK and area size
15. **High_Amenity** - Has ≥3 amenities
16. **Construction_Category** - Text version of construction status
17. **Locality_Property_Count** - Number of properties in locality
18. **Locality_Median_Area** - Median area in locality
19. **Locality_Common_BHK** - Most common BHK in locality

## 📊 Data Processing

### Locality Filtering
- Keeps localities with ≥3 properties (91 localities)
- Marks localities with <3 properties as 'Unknown' (filtered out)
- Uses **median** instead of mean (robust to outliers)

### Price Bucketing
- 19 buckets with 20L intervals (0-20L, 20-40L, ..., 360-380L)
- Most properties: 40-60L (591), 60-80L (564), 80-100L (374)

### Outlier Removal
- Price: Kept 8L - 368L (removed 144 outliers)
- Area: Kept 200 - 8,500 sqft (all valid)

## 📈 Performance Improvements

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **Dataset Size** | 2,475 | 2,783 | +12% |
| **R² Score** | 0.7892 | **0.8357** | **+6%** |
| **RMSE** | 34.41L | **27.63L** | **-20%** |
| **MAE** | 17.75L | **14.73L** | **-17%** |

## 🔍 Top Localities (by property count)

1. Bopal (240)
2. Shela (216)
3. Chandkheda (164)
4. Gota (136)
5. Vaishno Devi (115)

## 📦 Dependencies

```bash
pip install pandas numpy scikit-learn xgboost lightgbm catboost playwright beautifulsoup4 matplotlib seaborn
```

## 🎓 Model Details

### XGBoost (Best Model)
- **n_estimators**: 400
- **learning_rate**: 0.05
- **max_depth**: 7
- **R² Score**: 0.8357
- **RMSE**: 27.63 Lakhs
- **MAE**: 14.73 Lakhs

### Hyperparameters
- Trees: 400 (balanced speed vs accuracy)
- Learning Rate: 0.05 (prevents overfitting)
- Max Depth: 7 (captures complexity without overfitting)

---

**Last Updated**: November 27, 2025  
**Dataset**: 2,783 properties from 91 Ahmedabad localities
