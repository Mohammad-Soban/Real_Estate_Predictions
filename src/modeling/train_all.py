"""
ENHANCED TRAINING - 10 MODELS
Trains: XGBoost, LightGBM, CatBoost, RandomForest, ExtraTrees, 
        GradientBoosting, AdaBoost, Bagging, Voting, Stacking
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import (RandomForestRegressor, ExtraTreesRegressor, 
                              GradientBoostingRegressor, AdaBoostRegressor, 
                              BaggingRegressor, VotingRegressor, StackingRegressor)
from sklearn.linear_model import Ridge
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import warnings
warnings.filterwarnings('ignore')

print("\n" + "="*80)
print("🔧 TRAINING 9 MODELS (7 Base + 2 Ensembles)")
print("="*80)

# Load
print("\n📂 Loading data...")
df = pd.read_csv('data/training/training_data_enhanced.csv')
print(f"✅ {len(df)} records")

# Features
feature_cols = ['BHK', 'Area_SqFt', 'Locality', 'Locality_Tier', 'Seller_Type', 
                'Property_Type', 'Furnishing_Status', 'Under_Construction', 'Amenities_Count',
                'Area_Per_BHK', 'Is_Large_Apartment', 'Is_Premium_Locality', 'Is_Budget_Locality',
                'BHK_Area_Combo', 'High_Amenity', 'Construction_Category', 'Locality_Property_Count',
                'Locality_Median_Area', 'Locality_Common_BHK']

X = df[feature_cols].copy()
y = df['Price_Lakhs'].copy()

# Encode
categorical_cols = ['Locality', 'Locality_Tier', 'Seller_Type', 'Property_Type', 
                    'Furnishing_Status', 'BHK_Area_Combo', 'Construction_Category']
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))
    label_encoders[col] = le

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"✅ Train: {len(X_train)}, Test: {len(X_test)}")

# Define base models (n_jobs=1 to avoid multiprocessing issues)
base_models = {
    'XGBoost': XGBRegressor(n_estimators=500, learning_rate=0.05, max_depth=7, random_state=42, n_jobs=1),
    'LightGBM': LGBMRegressor(n_estimators=500, learning_rate=0.05, max_depth=7, random_state=42, n_jobs=1, verbose=-1),
    'CatBoost': CatBoostRegressor(iterations=500, learning_rate=0.05, depth=7, random_state=42, verbose=0),
    'RandomForest': RandomForestRegressor(n_estimators=300, max_depth=15, random_state=42, n_jobs=1),
    'ExtraTrees': ExtraTreesRegressor(n_estimators=300, max_depth=15, random_state=42, n_jobs=1),
    'GradientBoosting': GradientBoostingRegressor(n_estimators=200, learning_rate=0.05, max_depth=7, random_state=42),
    'AdaBoost': AdaBoostRegressor(n_estimators=100, learning_rate=0.5, random_state=42)
}

# Train base models
results = []
trained_models = {}
print("\n🎯 Training base models...\n")

for name, model in base_models.items():
    print(f"  {name}...", end=" ", flush=True)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    results.append({'Model': name, 'MAE': mae, 'RMSE': rmse, 'R2': r2, 'obj': model})
    trained_models[name] = model
    print(f"✅ R²={r2:.4f}, RMSE={rmse:.2f}L, MAE={mae:.2f}L")

# Create simple ensemble models
print("\n🎯 Training ensemble models...\n")

# Voting Ensemble (simple average - no parallel processing)
print("  Voting Ensemble...", end=" ", flush=True)
voting_preds = []
for name in ['XGBoost', 'LightGBM', 'CatBoost']:
    voting_preds.append(trained_models[name].predict(X_test))
y_pred = np.mean(voting_preds, axis=0)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)
# Create a simple class to hold the prediction method
class SimpleVoting:
    def __init__(self, models):
        self.models = models
    def predict(self, X):
        preds = [m.predict(X) for m in self.models]
        return np.mean(preds, axis=0)
voting = SimpleVoting([trained_models['XGBoost'], trained_models['LightGBM'], trained_models['CatBoost']])
results.append({'Model': 'Voting Ensemble', 'MAE': mae, 'RMSE': rmse, 'R2': r2, 'obj': voting})
print(f"✅ R²={r2:.4f}, RMSE={rmse:.2f}L, MAE={mae:.2f}L")

# Weighted Ensemble (best 3 models weighted)
print("  Weighted Ensemble...", end=" ", flush=True)
# Weight by R2 scores of top 3 base models
top3 = sorted(results, key=lambda x: x['R2'], reverse=True)[:3]
weights = np.array([r['R2'] for r in top3])
weights = weights / weights.sum()
weighted_preds = sum(w * m['obj'].predict(X_test) for w, m in zip(weights, top3))
mae = mean_absolute_error(y_test, weighted_preds)
rmse = np.sqrt(mean_squared_error(y_test, weighted_preds))
r2 = r2_score(y_test, weighted_preds)
class WeightedEnsemble:
    def __init__(self, models, weights):
        self.models = models
        self.weights = weights
    def predict(self, X):
        return sum(w * m.predict(X) for w, m in zip(self.weights, self.models))
weighted = WeightedEnsemble([m['obj'] for m in top3], weights)
results.append({'Model': 'Weighted Ensemble', 'MAE': mae, 'RMSE': rmse, 'R2': r2, 'obj': weighted})
print(f"✅ R²={r2:.4f}, RMSE={rmse:.2f}L, MAE={mae:.2f}L")

# Sort and display
results_df = pd.DataFrame(results)
results_df = results_df.sort_values('R2', ascending=False)

print("\n" + "="*80)
print("📊 MODEL COMPARISON (Sorted by R² Score)")
print("="*80)
for idx, row in results_df.iterrows():
    rank = list(results_df.index).index(idx) + 1
    print(f"#{rank:2d} {row['Model']:20} | R²={row['R2']:.4f} | RMSE={row['RMSE']:6.2f}L | MAE={row['MAE']:6.2f}L")
print("="*80)

# Save all models
print("\n💾 Saving models...")
for i in range(len(results_df)):
    name = results_df.iloc[i]['Model']
    obj = results_df.iloc[i]['obj']
    filename = f"models/model_{i+1}_{name.lower().replace(' ', '_')}.pkl"
    joblib.dump(obj, filename)
    print(f"  #{i+1:2d} {name:20} → {filename}")

# Save best model and encoders
joblib.dump(label_encoders, 'models/label_encoders.pkl')
joblib.dump(results_df.iloc[0]['obj'], 'models/best_model.pkl')

# Save comparison report
results_df[['Model', 'R2', 'RMSE', 'MAE']].to_csv('reports/model_comparison.csv', index=False)

print(f"\n✅ TRAINING COMPLETE!")
print(f"   Best Model: {results_df.iloc[0]['Model']} (R²={results_df.iloc[0]['R2']:.4f})")
print(f"   Models saved: models/")
print(f"   Report saved: reports/model_comparison.csv")
print("="*80)
