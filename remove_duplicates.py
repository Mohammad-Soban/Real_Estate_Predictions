"""
Remove duplicates from cleaned_data.csv
"""
import pandas as pd

print("📂 Loading cleaned_data.csv...")
df = pd.read_csv('data/cleaned/cleaned_data.csv')
print(f"✅ Total rows: {len(df)}")

# Check for duplicates
duplicates = df.duplicated(subset=['BHK', 'Area_SqFt', 'Locality', 'Price_Lakhs']).sum()
print(f"🔍 Found {duplicates} duplicates")

if duplicates > 0:
    # Remove duplicates, keeping first occurrence
    df_clean = df.drop_duplicates(subset=['BHK', 'Area_SqFt', 'Locality', 'Price_Lakhs'], keep='first')
    print(f"🧹 After removing duplicates: {len(df_clean)} unique rows")
    
    # Save back to the same file
    df_clean.to_csv('data/cleaned/cleaned_data.csv', index=False)
    print(f"✅ Saved cleaned data without duplicates")
    print(f"   Removed: {duplicates} duplicate rows")
    print(f"   Remaining: {len(df_clean)} unique properties")
else:
    print("✅ No duplicates found!")
