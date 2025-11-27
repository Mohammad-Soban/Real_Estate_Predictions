"""
COMPLETE PIPELINE - Everything except scraping
Runs: Simple Preprocessing → Enhanced Preprocessing → Train 10 Models → Generate Visualizations
"""
import subprocess
import sys
import os

print("="*80)
print("COMPLETE PIPELINE - PREPROCESSING + TRAINING + VISUALIZATION")
print("="*80)

# Step 1: Simple Preprocessing
print("\n[1/4] Running Simple Preprocessing...")
print("-" * 80)
result = subprocess.run([sys.executable, "src/preprocessing/preprocess_simple.py"])
if result.returncode != 0:
    print("❌ Simple preprocessing failed!")
    sys.exit(1)

# Step 2: Enhanced Preprocessing
print("\n[2/4] Running Enhanced Preprocessing...")
print("-" * 80)
result = subprocess.run([sys.executable, "src/preprocessing/preprocess_enhanced.py"])
if result.returncode != 0:
    print("❌ Enhanced preprocessing failed!")
    sys.exit(1)

# Step 3: Train All Models
print("\n[3/4] Training 10 Models...")
print("-" * 80)
result = subprocess.run([sys.executable, "src/modeling/train_all.py"])
if result.returncode != 0:
    print("❌ Training failed!")
    sys.exit(1)

# Step 4: Generate Visualizations
print("\n[4/4] Generating Visualizations...")
print("-" * 80)
result = subprocess.run([sys.executable, "src/visualize.py"])
if result.returncode != 0:
    print("❌ Visualization failed!")
    sys.exit(1)

print("\n" + "="*80)
print("✅ PIPELINE COMPLETE!")
print("="*80)
print("📁 Models saved in: models/")
print("📊 Visualizations saved in: visualizations/")
print("📈 Report saved in: reports/model_comparison.csv")
print("="*80)
