# 🚀 File Execution Guide - Run Different Components

## 📁 Quick Reference: What Each File Does

| File | Purpose | Execution Time | When to Use |
|------|---------|----------------|-------------|
| `property_finder.py` | Interactive property search | 2 mins | **Demo/Daily use** |
| `chatbot.py` | Q&A about properties | Instant | Quick queries |
| `main_phase2.py` | Batch AI processing | 3-5 hrs (all) | Generate insights |
| `main.py` | Train ML model | 2 mins | After data changes |
| `src/predict.py` | Single property prediction | Instant | Price estimation |
| `remove_duplicates.py` | Clean duplicate data | 5 secs | Data maintenance |

---

## 🎯 Scenario-Based Execution Guide

### Scenario 1: "I want to find properties for myself"

**Use**: `property_finder.py`

```powershell
# Run interactive property finder
python property_finder.py
```

**What happens**:
1. Loads 1,940 properties
2. Asks 6 questions (budget, BHK, locality, etc.)
3. Shows top 10 matches with scores
4. Displays detailed property cards

**Sample interaction**:
```
💰 Budget? → 50 80
🏠 BHK? → 3
📍 Localities? → Bopal, Gota
🛋️ Furnishing? → Semi-Furnished
✨ Amenities? → 2
🏢 Type? → Apartment

→ Shows 10 best matches with "Why this property?"
```

**Output**: Terminal display only (no files created)

**When to use**:
- Live demo in presentation
- Personal property search
- Quick recommendations

---

### Scenario 2: "I want to ask specific questions"

**Use**: `chatbot.py`

```powershell
# Run AI chatbot
python chatbot.py
```

**What happens**:
1. Loads property database
2. Waits for your questions
3. Answers using property data
4. Type 'exit' to quit

**Sample questions**:
```
You: Show me cheapest 3 BHK properties
Bot: [Lists 5 cheapest properties]

You: Which localities have most amenities?
Bot: Bopal (avg 4.2), SG Highway (avg 3.8)...

You: Properties in Bopal under 80 lakhs?
Bot: [Filtered list]

You: exit
```

**Output**: Terminal display only

**When to use**:
- Exploratory data analysis
- Answer specific queries
- Quick statistics

---

### Scenario 3: "I want AI-generated insights for properties"

**Use**: `main_phase2.py`

```powershell
# Make sure Ollama is running first
$env:PATH += ";$env:LOCALAPPDATA\Programs\Ollama"

# Run Phase 2 processing
python main_phase2.py
```

**What happens**:
1. Menu appears with 2 options
2. Select option 1 (Generate AI insights)
3. Choose number of properties:
   - `10` = 30 minutes
   - `50` = 2.5 hours
   - `100` = 5 hours
   - `all` = 10-12 hours
4. Processes in batches of 10
5. Saves results to CSV

**Sample run**:
```
========================================
   REAL ESTATE AI INSIGHTS GENERATOR
========================================

Choose an option:
1. Generate AI Property Insights (Brochures, Analysis)
2. Interactive Chatbot (Ask questions)

Enter 1 or 2: 1

How many properties to process? (Enter number or 'all'): 10

Processing batch 1/1 (properties 1-10)...
Progress: [##########] 100%
✅ Completed in 28 minutes

Results saved to: data/results/buyer_focused_analysis_complete_20251128_*.csv
```

**Output Files**:
- `data/results/buyer_focused_analysis_complete_*.csv` - Full report with:
  - AI-generated brochures
  - Quality scores
  - Amenity analysis
  - Locality insights
  - Unique Property_IDs

**When to use**:
- Generate marketing brochures
- Create comprehensive property reports
- Add AI insights to dataset
- First-time setup (run on all properties once)

**⚠️ Important**:
- **Small test**: Use 10 properties (30 mins)
- **Full dataset**: Use 'all' overnight (10-12 hours)
- **Ollama must be running** (check: http://localhost:11434)

---

### Scenario 4: "I want to train/retrain the ML model"

**Use**: `main.py`

```powershell
# Train ML model from scratch
python main.py
```

**What happens**:
1. Loads cleaned_data.csv
2. Engineers 19 features
3. Trains XGBoost model
4. Evaluates on test set
5. Saves model to `models/xgboost_price_model.pkl`

**Sample output**:
```
Loading data from data/cleaned/cleaned_data.csv
Loaded 1940 properties

Engineering features...
Created 19 features

Training XGBoost model...
Training completed in 12.3 seconds

Model Performance:
- R² Score: 0.8357
- MAE: ₹8.2 Lakhs
- RMSE: ₹11.5 Lakhs

Top 5 Feature Importance:
1. Price_per_SqFt: 45.2%
2. Locality_Tier: 23.1%
3. BHK_Category: 18.4%
4. Area_SqFt: 7.8%
5. Amenities_Score: 5.5%

Model saved to: models/xgboost_price_model.pkl
```

**Output Files**:
- `models/xgboost_price_model.pkl` - Trained model
- `reports/model_comparison.csv` - Performance metrics

**When to use**:
- After adding new properties
- After changing features
- After cleaning duplicates
- To improve model (hyperparameter tuning)

**⚠️ Important**:
- Only needed if you change the dataset
- Model already trained (no need to run again)

---

### Scenario 5: "I want to predict price for a single property"

**Use**: `src/predict.py`

```powershell
# Predict price for custom input
python src/predict.py
```

**What happens**:
1. Loads trained model
2. Asks for property details
3. Predicts fair price
4. Shows comparison with listed price

**Sample interaction**:
```
Enter property details:

BHK: 3
Area (sq ft): 1500
Locality: Bopal
Furnishing (Furnished/Semi-Furnished/Unfurnished): Semi-Furnished
Property Type (Apartment/House): Apartment
Amenities (comma-separated): Gym,Pool,Garden,Security
Listed Price (Lakhs): 85

═══════════════════════════════════════
📊 PRICE PREDICTION RESULT
═══════════════════════════════════════

🏠 Property: 3 BHK, 1500 sq ft, Bopal
💰 Predicted Fair Value: ₹78.5 Lakhs
💵 Listed Price: ₹85 Lakhs
📉 Difference: ₹6.5 Lakhs (7.6% overpriced)

💡 Recommendation: Negotiate down by ₹5-7 Lakhs

Key Factors:
✓ Price per sq ft: ₹5,233 (within market range)
✓ Locality: Tier 1 (premium area)
✓ Amenities: 4/6 (good)
⚠ Area: Slightly below average for Bopal 3 BHK
```

**Output**: Terminal display only

**When to use**:
- Evaluate a specific listing
- Negotiation preparation
- Quick price check

---

### Scenario 6: "I want to clean duplicate data"

**Use**: `remove_duplicates.py`

```powershell
# Remove duplicates from dataset
python remove_duplicates.py
```

**What happens**:
1. Loads `data/cleaned/cleaned_data.csv`
2. Detects duplicates (BHK + Area + Locality + Price)
3. Removes duplicates (keeps first occurrence)
4. Saves cleaned file back

**Sample output**:
```
Loading data from: data/cleaned/cleaned_data.csv
Original count: 2801 properties

Detecting duplicates...
Found 861 duplicates (30.7%)

Removing duplicates...
Remaining: 1940 unique properties

Saving cleaned data...
✅ Saved to: data/cleaned/cleaned_data.csv

Summary:
- Removed: 861 duplicates
- Kept: 1940 unique properties
- Reduction: 30.7%
```

**Output Files**:
- Overwrites `data/cleaned/cleaned_data.csv`

**When to use**:
- After scraping new data
- If you suspect duplicates
- Data maintenance

**⚠️ Important**:
- Already run (dataset is clean)
- Only run if you add new data

---

## 🔄 Complete Workflow: From Scratch to Recommendation

### Full Pipeline (First Time Setup)

```powershell
# Step 1: Clean duplicates (5 seconds)
python remove_duplicates.py
# Result: 2,801 → 1,940 unique properties

# Step 2: Train ML model (2 minutes)
python main.py
# Result: model saved to models/xgboost_price_model.pkl

# Step 3: Generate AI insights (10-12 hours - Optional)
$env:PATH += ";$env:LOCALAPPDATA\Programs\Ollama"
python main_phase2.py
# Choose: 1 → Enter: all
# Result: AI insights saved to data/results/

# Step 4: Find properties (2 minutes)
python property_finder.py
# Result: Top 10 recommendations
```

**Total time**: 
- Without AI insights: ~2 minutes
- With AI insights: ~10-12 hours (run overnight)

---

### Quick Demo Workflow (Presentation)

```powershell
# Option A: Interactive Property Search (RECOMMENDED)
python property_finder.py
# Answer 6 questions → Show top 10

# Option B: Chatbot Q&A
python chatbot.py
# Ask: "Show me cheapest 3 BHK"

# Option C: Price Prediction
python src/predict.py
# Enter property details → Show prediction
```

**Time**: 2-5 minutes per demo

---

### Daily Use Workflow

```powershell
# For users searching properties
python property_finder.py

# For specific queries
python chatbot.py

# For price checking
python src/predict.py
```

---

## 📊 Comparison: Which File to Use?

### I want to...

**"Find properties matching my preferences"**
```powershell
→ python property_finder.py
✓ Interactive, 2 mins, top 10 results
```

**"Ask 'What's the cheapest 3 BHK?'"**
```powershell
→ python chatbot.py
✓ Natural language, instant answers
```

**"Check if ₹85L for a 3 BHK in Bopal is fair"**
```powershell
→ python src/predict.py
✓ Single property focus, instant
```

**"Generate brochures for 100 properties"**
```powershell
→ python main_phase2.py (Option 1)
✓ Batch processing, 5 hours
```

**"Retrain model with new data"**
```powershell
→ python main.py
✓ Full training, 2 mins
```

**"Clean duplicate properties"**
```powershell
→ python remove_duplicates.py
✓ Data cleaning, 5 secs
```

---

## 🎬 Execution for Different Audiences

### For Evaluators (Technical Presentation)

**Demo 1: Property Finder (Live)**
```powershell
python property_finder.py
# Show real-time filtering and scoring
# Time: 2 minutes
```

**Demo 2: ML Prediction**
```powershell
python src/predict.py
# Show price prediction accuracy
# Time: 1 minute
```

**Optional: Show AI Processing**
```powershell
python main_phase2.py
# Select 10 properties (if time permits)
# Time: 30 minutes (run beforehand, show results)
```

**Total**: 3-5 minutes of live demos

---

### For End Users (Product Demo)

**Demo: Property Search Journey**
```powershell
# Step 1: Find properties
python property_finder.py
Budget: 50 80
BHK: 3
Localities: Bopal, Gota
[... answer remaining questions ...]

# Step 2: Ask follow-up
python chatbot.py
You: Tell me more about Bopal locality
Bot: [Locality analysis]

# Step 3: Price check
python src/predict.py
[Enter details of top match]
[Show if price is fair]
```

**Total**: 5-7 minutes

---

### For Developers (Code Walkthrough)

**Show Architecture**
```powershell
# 1. Data layer
Get-Content data/cleaned/cleaned_data.csv | Select-Object -First 5

# 2. ML layer
python main.py
# Show training process

# 3. AI layer
python main_phase2.py
# Explain Ollama integration

# 4. Application layer
python property_finder.py
# Show user interface
```

**Total**: 10-15 minutes

---

## ⚡ Quick Commands Reference Card

```powershell
# === MOST USED COMMANDS ===

# 1. Find properties (Interactive) ⭐ USE FOR DEMO
python property_finder.py

# 2. Ask questions (Quick queries)
python chatbot.py

# 3. Predict price (Single property)
python src/predict.py

# === SETUP/MAINTENANCE ===

# 4. Train ML model (After data changes)
python main.py

# 5. Generate AI insights (Batch processing)
python main_phase2.py

# 6. Clean duplicates (Data maintenance)
python remove_duplicates.py

# === OLLAMA SETUP ===

# Check if Ollama is running
Invoke-RestMethod http://localhost:11434/api/tags

# Start Ollama (if not running)
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" serve

# Add Ollama to PATH (for main_phase2.py)
$env:PATH += ";$env:LOCALAPPDATA\Programs\Ollama"
```

---

## 🐛 Troubleshooting Common Issues

### Issue 1: "Ollama not found"

**Error**: `ConnectionError: Could not connect to Ollama`

**Solution**:
```powershell
# Check if Ollama is installed
Test-Path "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe"

# If False, install from: https://ollama.ai/download

# If True, start Ollama
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" serve

# Verify it's running
Invoke-RestMethod http://localhost:11434/api/tags
```

---

### Issue 2: "Module not found"

**Error**: `ModuleNotFoundError: No module named 'pandas'`

**Solution**:
```powershell
# Install required packages
pip install -r requirements.txt

# Or install individually
pip install pandas numpy scikit-learn xgboost requests
```

---

### Issue 3: "File not found: cleaned_data.csv"

**Error**: `FileNotFoundError: data/cleaned/cleaned_data.csv`

**Solution**:
```powershell
# Check if file exists
Test-Path data/cleaned/cleaned_data.csv

# If False, data might be in different location
# Copy from raw to cleaned
Copy-Item data/raw/all_sources_detailed_*.csv data/cleaned/cleaned_data.csv

# Then clean duplicates
python remove_duplicates.py
```

---

### Issue 4: "Property finder shows 0 results"

**Error**: `No properties match your criteria`

**Solution**:
- This shouldn't happen due to progressive filtering
- But if it does:
  1. Relax budget range (e.g., 30-100 instead of 75-80)
  2. Select "Any" for BHK, Furnishing, Type
  3. Skip locality filter (press Enter without typing)

---

### Issue 5: "main_phase2.py is too slow"

**Issue**: Processing 1,940 properties takes 10-12 hours

**Solution**:
```powershell
# Option 1: Process fewer properties
python main_phase2.py
# Enter: 10 (only 30 minutes)

# Option 2: Run overnight
# Start before leaving office/going to sleep

# Option 3: Use faster model (if available)
# Edit src/nlp/brochure_generator.py
# Change model to 'mistral' (faster than llama2)
```

---

## 📝 Execution Checklist for Presentation

### Before Presentation

- [ ] Test property_finder.py (ensure it works)
- [ ] Prepare sample inputs (budget: 50-80, BHK: 3, localities: Bopal, Gota)
- [ ] Test chatbot.py (ask 2-3 sample questions)
- [ ] Test src/predict.py (have property details ready)
- [ ] Ensure Ollama is running (if demoing main_phase2.py)
- [ ] Have data/cleaned/cleaned_data.csv ready (check row count: 1,940)
- [ ] Have model trained (models/xgboost_price_model.pkl exists)
- [ ] Pre-generate AI insights for 10 properties (if showing CSV output)

### During Presentation

**Primary Demo** (2 minutes):
```powershell
python property_finder.py
# Show full flow → Top 10 results
```

**Backup Demo 1** (if property_finder.py fails):
```powershell
python chatbot.py
# Ask pre-prepared questions
```

**Backup Demo 2** (if both fail):
```powershell
# Show CSV outputs
Get-Content data/results/buyer_focused_analysis_complete_*.csv | Select-Object -First 5
```

---

## 🎯 Best Practices

1. **For demos**: Always use `property_finder.py` (fastest, most impressive)

2. **For testing**: Use `main_phase2.py` with 10 properties first

3. **For development**: Run `main.py` after every data change

4. **For data quality**: Run `remove_duplicates.py` weekly

5. **For price checks**: Use `src/predict.py` for individual properties

6. **For exploration**: Use `chatbot.py` for quick insights

---

## 📚 Further Reading

- **Architecture**: See `PRESENTATION_GUIDE.md` for WHY questions
- **Phase 1 Details**: See `PHASE1_COMPLETE_GUIDE.md` (ML pipeline)
- **Phase 2 Details**: See `PHASE2_COMPLETE_GUIDE.md` (AI pipeline)
- **Recent Changes**: See `IMPROVEMENTS_SUMMARY.md`

---

**Quick Help**:
```powershell
# Show help for any script
python property_finder.py --help
python chatbot.py --help
python main.py --help
```

**Got stuck? Check**:
1. Is Python installed? `python --version`
2. Are packages installed? `pip list`
3. Is Ollama running? `Invoke-RestMethod http://localhost:11434/api/tags`
4. Is data present? `Test-Path data/cleaned/cleaned_data.csv`

---

**Ready to run! 🚀**
