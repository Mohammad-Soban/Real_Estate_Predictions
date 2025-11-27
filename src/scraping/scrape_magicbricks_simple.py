"""
Simplified Robust Scraper for Ahmedabad Properties
Uses Playwright with better error handling
"""

import time
import pandas as pd
from playwright.sync_api import sync_playwright
from datetime import datetime
import re

print("\n" + "="*70)
print("SIMPLIFIED ROBUST SCRAPER - AHMEDABAD PROPERTIES")
print("="*70)
print("🎯 Target: MagicBricks Ahmedabad")
print("📊 Pages: 50 pages (500+ properties)")
print("="*70)

def clean_price(price_text):
    """Extract price in lakhs"""
    if not price_text:
        return None
    price_text = price_text.lower().replace(',', '')
    nums = re.findall(r'[\d.]+', price_text)
    if not nums:
        return None
    val = float(nums[0])
    if 'cr' in price_text:
        return f"{val} Cr"
    elif 'l' in price_text or 'lac' in price_text:
        return f"{val} L"
    return price_text

def scrape_magicbricks():
    """Scrape MagicBricks Ahmedabad properties"""
    properties = []
    
    with sync_playwright() as p:
        print("\n🌐 Launching browser...")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.set_default_timeout(60000)
        
        base_url = "https://www.magicbricks.com/property-for-sale/residential-real-estate?bedroom=&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName=Ahmedabad"
        
        for page_num in range(1, 51):  # 50 pages
            try:
                print(f"\n📄 Page {page_num}/50...")
                
                if page_num == 1:
                    page.goto(base_url, wait_until="domcontentloaded")
                else:
                    page.goto(f"{base_url}&page={page_num}", wait_until="domcontentloaded")
                
                time.sleep(3)
                
                # Wait for listings
                try:
                    page.wait_for_selector('.mb-srp__card', timeout=10000)
                except:
                    print(f"  ⚠️ No listings found on page {page_num}, skipping...")
                    continue
                
                cards = page.query_selector_all('.mb-srp__card')
                print(f"  Found {len(cards)} listings")
                
                for i, card in enumerate(cards, 1):
                    try:
                        # Extract data with error handling
                        title_elem = card.query_selector('.mb-srp__card__title, .mb-srp__card--title')
                        title = title_elem.inner_text().strip() if title_elem else None
                        
                        price_elem = card.query_selector('.mb-srp__card__price, [class*="price"]')
                        price = price_elem.inner_text().strip() if price_elem else None
                        
                        location_elem = card.query_selector('.mb-srp__card__soc--location, [class*="location"]')
                        location = location_elem.inner_text().strip() if location_elem else None
                        
                        # Get property details
                        details_text = card.inner_text()
                        
                        # Extract BHK
                        bhk_match = re.search(r'(\d+)\s*BHK', details_text, re.IGNORECASE)
                        bhk = bhk_match.group(1) + ' BHK' if bhk_match else None
                        
                        # Extract Area
                        area_match = re.search(r'(\d+(?:,\d+)?)\s*sq\.?\s*ft', details_text, re.IGNORECASE)
                        area = area_match.group(0) if area_match else None
                        
                        # Extract Bathrooms
                        bath_match = re.search(r'(\d+)\s*Bath', details_text, re.IGNORECASE)
                        bathrooms = bath_match.group(1) + ' Bathrooms' if bath_match else None
                        
                        # Extract Furnishing
                        furnishing = None
                        if 'Furnished' in details_text:
                            if 'Semi' in details_text or 'Semi-Furnished' in details_text:
                                furnishing = 'Semi-Furnished'
                            else:
                                furnishing = 'Furnished'
                        elif 'Unfurnished' in details_text:
                            furnishing = 'Unfurnished'
                        
                        # Property type
                        prop_type = None
                        if 'Apartment' in details_text or 'Flat' in details_text:
                            prop_type = 'Apartment'
                        elif 'Villa' in details_text:
                            prop_type = 'Villa'
                        elif 'House' in details_text:
                            prop_type = 'Independent House'
                        
                        properties.append({
                            'Property_Title': title,
                            'Price': clean_price(price) if price else None,
                            'Area_SqFt': area,
                            'BHK': bhk,
                            'Bathrooms': bathrooms,
                            'Furnishing_Status': furnishing,
                            'Property_Type': prop_type,
                            'Locality': location,
                            'Source_Website': 'MagicBricks',
                            'Description': details_text[:500] if details_text else None
                        })
                        
                    except Exception as e:
                        print(f"    ⚠️ Error extracting card {i}: {str(e)[:50]}")
                        continue
                
                print(f"  ✅ Extracted {len(properties)} total properties so far")
                
                # Random delay
                time.sleep(2 + (page_num % 3))
                
            except Exception as e:
                print(f"  ❌ Error on page {page_num}: {str(e)[:100]}")
                continue
        
        browser.close()
    
    return properties

def main():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    print("\n🚀 Starting scraper...")
    properties = scrape_magicbricks()
    
    if properties:
        df = pd.DataFrame(properties)
        
        # Save to raw folder
        output_file = f'data/raw/magicbricks_ahmedabad_{timestamp}.csv'
        df.to_csv(output_file, index=False)
        
        print("\n" + "="*70)
        print("✅ SCRAPING COMPLETE!")
        print("="*70)
        print(f"📊 Total properties: {len(df)}")
        print(f"📁 Saved to: {output_file}")
        
        # Show sample
        print("\n📊 Sample data:")
        print(df[['Property_Title', 'Price', 'BHK', 'Locality']].head(10).to_string(index=False))
        
        # Data completeness
        print("\n📊 Data completeness:")
        for col in ['Property_Title', 'Price', 'Area_SqFt', 'BHK', 'Locality']:
            pct = (df[col].notna().sum() / len(df)) * 100
            print(f"  {col:20s}: {pct:5.1f}%")
        
        return df
    else:
        print("\n❌ No data collected!")
        return None

if __name__ == "__main__":
    df = main()
