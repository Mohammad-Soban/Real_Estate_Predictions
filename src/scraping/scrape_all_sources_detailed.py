"""
DETAILED MULTI-SOURCE SCRAPER
Extracts comprehensive property data with all available fields
Maintains separate CSV per source and drops exact duplicates
"""

import time
import random
import pandas as pd
from playwright.sync_api import sync_playwright
from datetime import datetime
import re
import json

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def extract_bedrooms(text):
    """Extract BHK/Bedrooms from text"""
    if not text:
        return None
    match = re.search(r'(\d+)\s*(?:BHK|Bedroom|BR|Bed)', str(text), re.IGNORECASE)
    return int(match.group(1)) if match else None

def extract_bathrooms(text):
    """Extract bathrooms from text"""
    if not text:
        return None
    match = re.search(r'(\d+)\s*(?:Bathroom|Bath|BA)', str(text), re.IGNORECASE)
    return int(match.group(1)) if match else None

def extract_area(text):
    """Extract area in sqft"""
    if not text:
        return None
    # Match patterns like "1200 sqft", "1,200 sq.ft", etc.
    match = re.search(r'(\d+(?:,\d+)?)\s*(?:sq\.?\s*ft|sqft|sq\s*feet)', str(text), re.IGNORECASE)
    if match:
        return int(match.group(1).replace(',', ''))
    return None

def extract_floor(text):
    """Extract floor number"""
    if not text:
        return None
    match = re.search(r'(\d+)(?:st|nd|rd|th)?\s*Floor', str(text), re.IGNORECASE)
    return int(match.group(1)) if match else None

def extract_furnishing(text):
    """Extract furnishing status"""
    if not text:
        return None
    text = str(text).upper()
    if 'SEMI' in text and 'FURNISHED' in text:
        return 'Semi-Furnished'
    elif 'FURNISHED' in text:
        return 'Furnished'
    elif 'UNFURNISHED' in text:
        return 'Unfurnished'
    return None

def clean_price_text(price_text):
    """Clean price text for storage"""
    if not price_text or price_text == "N/A":
        return None
    return str(price_text).strip()

# ============================================================================
# 99ACRES SCRAPER
# ============================================================================

def scrape_99acres(pages=10):
    """Scrape 99acres.com with detailed data extraction"""
    print("\n" + "="*70)
    print("SCRAPING 99ACRES.COM")
    print("="*70)
    
    base_url = "https://www.99acres.com/search/property/buy/residential-all/ahmedabad-all?keyword=ahmedabad&preference=S&area_unit=1&res_com=R"
    data_list = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False, 
            slow_mo=1000,
            args=["--disable-blink-features=AutomationControlled", "--start-maximized"]
        )
        
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        
        page = context.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")

        for current_page in range(1, pages + 1):
            url = f"{base_url}&page={current_page}"
            print(f"\n📄 Page {current_page}/{pages}...")
            
            try:
                page.goto(url, timeout=60000, wait_until="domcontentloaded")
                time.sleep(5)
                
                # Remove Gurgaon tags if any
                try:
                    gurgaon_tags = page.locator('div[class*="searchTag"]:has-text("Gurgaon")').all()
                    for tag in gurgaon_tags:
                        tag.locator('i, span, svg').first.click()
                        time.sleep(2)
                except:
                    pass
                
                # Scroll to load content
                for _ in range(3):
                    page.keyboard.press("PageDown")
                    time.sleep(1)
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(3)
                
                # Find property cards
                cards = page.locator('div[class*="srpTuple__card"], div[class*="projectTuple__card"], article').all()
                if len(cards) == 0:
                    cards = page.locator('div:has-text("₹"):has-text("BHK")').all()
                
                print(f"  Found {len(cards)} listings")
                
                for i, card in enumerate(cards):
                    try:
                        text_content = card.inner_text().strip()
                        if not text_content: 
                            continue
                        
                        # Extract all available data
                        property_data = {
                            'Property_Title': None,
                            'Price': None,
                            'Area_SqFt': None,
                            'BHK': None,
                            'Bathrooms': None,
                            'Furnishing_Status': None,
                            'Property_Type': None,
                            'Seller_Type': None,
                            'Project_Name': None,
                            'Locality': None,
                            'Posted_Date': None,
                            'Floor_Number': None,
                            'Source_Website': '99acres',
                            'Raw_JSON': None,
                            'URL': None,
                            'Description': None
                        }
                        
                        # Title
                        title_loc = card.locator('h2, a[class*="title"]').first
                        if title_loc.count() > 0:
                            property_data['Property_Title'] = title_loc.inner_text().strip()
                        
                        # Price
                        price_loc = card.locator('[class*="price"], [id*="price"]').first
                        if price_loc.count() > 0:
                            property_data['Price'] = clean_price_text(price_loc.inner_text())
                        
                        # Location
                        loc_loc = card.locator('[class*="society"], [class*="loc"]').first
                        if loc_loc.count() > 0:
                            property_data['Locality'] = loc_loc.inner_text().strip()
                        
                        # URL
                        link_loc = card.locator('a').first
                        if link_loc.count() > 0:
                            href = link_loc.get_attribute('href')
                            if href:
                                property_data['URL'] = f"https://www.99acres.com{href}" if not href.startswith('http') else href
                        
                        # Extract from full text
                        property_data['BHK'] = extract_bedrooms(text_content)
                        property_data['Bathrooms'] = extract_bathrooms(text_content)
                        property_data['Area_SqFt'] = extract_area(text_content)
                        property_data['Floor_Number'] = extract_floor(text_content)
                        property_data['Furnishing_Status'] = extract_furnishing(text_content)
                        
                        # Property Type
                        if property_data['Property_Title']:
                            title_upper = property_data['Property_Title'].upper()
                            if 'VILLA' in title_upper:
                                property_data['Property_Type'] = 'Villa'
                            elif 'PENTHOUSE' in title_upper:
                                property_data['Property_Type'] = 'Penthouse'
                            elif 'STUDIO' in title_upper:
                                property_data['Property_Type'] = 'Studio Apartment'
                            elif 'PLOT' in title_upper or 'LAND' in title_upper:
                                property_data['Property_Type'] = 'Plot/Land'
                            elif 'INDEPENDENT' in title_upper or 'HOUSE' in title_upper:
                                property_data['Property_Type'] = 'Independent House'
                            else:
                                property_data['Property_Type'] = 'Apartment'
                        
                        # Seller Type
                        if 'OWNER' in text_content.upper():
                            property_data['Seller_Type'] = 'Owner'
                        elif 'BUILDER' in text_content.upper():
                            property_data['Seller_Type'] = 'Builder'
                        elif 'DEALER' in text_content.upper() or 'AGENT' in text_content.upper():
                            property_data['Seller_Type'] = 'Dealer'
                        
                        # Store raw data
                        property_data['Raw_JSON'] = json.dumps(text_content[:500])  # First 500 chars
                        property_data['Description'] = text_content[:200]
                        
                        # Only add if has title or price
                        if property_data['Property_Title'] or property_data['Price']:
                            data_list.append(property_data)
                    
                    except Exception as e:
                        continue
                
                print(f"  ✅ Total collected: {len(data_list)}")
            
            except Exception as e:
                print(f"  ❌ Error: {e}")
        
        browser.close()
    
    print(f"\n🎯 99acres Final: {len(data_list)} properties")
    return data_list

# ============================================================================
# MAGICBRICKS SCRAPER (100 PAGES)
# ============================================================================

def scrape_magicbricks(pages=100):
    """Scrape MagicBricks.com with detailed data extraction - 100 pages"""
    print("\n" + "="*70)
    print("SCRAPING MAGICBRICKS.COM - 100 PAGES")
    print("="*70)
    
    data_list = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            slow_mo=500,
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        
        page = context.new_page()
        
        for page_num in range(1, pages + 1):
            url = f"https://www.magicbricks.com/property-for-sale/residential-real-estate?bedroom=&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName=Ahmedabad&page={page_num}"
            
            print(f"\n📄 Page {page_num}/{pages}...")
            
            try:
                page.goto(url, timeout=60000, wait_until="domcontentloaded")
                time.sleep(4)
                
                # Scroll to load content
                page.evaluate("window.scrollTo(0, document.body.scrollHeight/2);")
                time.sleep(2)
                page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                
                # Find property cards
                cards = page.locator("div.mb-srp__card").all()
                
                if len(cards) == 0:
                    print(f"  ⚠️ No cards found - may have reached end")
                    break
                
                print(f"  Found {len(cards)} listings")
                
                for card in cards:
                    try:
                        text_content = card.inner_text()
                        
                        property_data = {
                            'Property_Title': None,
                            'Price': None,
                            'Area_SqFt': None,
                            'BHK': None,
                            'Bathrooms': None,
                            'Furnishing_Status': None,
                            'Property_Type': None,
                            'Seller_Type': None,
                            'Project_Name': None,
                            'Locality': None,
                            'Posted_Date': None,
                            'Floor_Number': None,
                            'Source_Website': 'MagicBricks',
                            'Raw_JSON': None,
                            'URL': None,
                            'Description': None
                        }
                        
                        # Title
                        title_elem = card.locator("h2.mb-srp__card--title").first
                        if title_elem.count() > 0:
                            property_data['Property_Title'] = title_elem.inner_text().strip()
                        
                        # Price
                        price_elem = card.locator("div.mb-srp__card__price--amount").first
                        if price_elem.count() > 0:
                            property_data['Price'] = clean_price_text(price_elem.inner_text())
                        
                        # Locality
                        locality_elem = card.locator("span.mb-srp__card__summary--value").first
                        if locality_elem.count() > 0:
                            property_data['Locality'] = locality_elem.inner_text().strip()
                        
                        # Property Type
                        prop_type_elem = card.locator("span.mb-srp__card__summary--value").nth(1)
                        if prop_type_elem.count() > 0:
                            property_data['Property_Type'] = prop_type_elem.inner_text().strip()
                        
                        # Extract from text
                        property_data['BHK'] = extract_bedrooms(text_content)
                        property_data['Bathrooms'] = extract_bathrooms(text_content)
                        property_data['Area_SqFt'] = extract_area(text_content)
                        property_data['Floor_Number'] = extract_floor(text_content)
                        property_data['Furnishing_Status'] = extract_furnishing(text_content)
                        
                        # Seller Type
                        if 'OWNER' in text_content.upper():
                            property_data['Seller_Type'] = 'Owner'
                        elif 'BUILDER' in text_content.upper():
                            property_data['Seller_Type'] = 'Builder'
                        elif 'DEALER' in text_content.upper() or 'AGENT' in text_content.upper():
                            property_data['Seller_Type'] = 'Dealer'
                        
                        # Posted date
                        posted_elem = card.locator("div.mb-srp__card__posted--text").first
                        if posted_elem.count() > 0:
                            property_data['Posted_Date'] = posted_elem.inner_text().strip()
                        
                        # URL
                        link_elem = card.locator("a.mb-srp__card__link").first
                        if link_elem.count() > 0:
                            href = link_elem.get_attribute('href')
                            if href:
                                property_data['URL'] = f"https://www.magicbricks.com{href}" if not href.startswith('http') else href
                        
                        # Raw data
                        property_data['Raw_JSON'] = json.dumps(text_content[:500])
                        property_data['Description'] = text_content[:200]
                        
                        if property_data['Property_Title'] and property_data['Price']:
                            data_list.append(property_data)
                    
                    except Exception as e:
                        continue
                
                print(f"  ✅ Total collected: {len(data_list)}")
                
                # Small delay between pages
                time.sleep(2)
            
            except Exception as e:
                print(f"  ❌ Error: {e}")
        
        browser.close()
    
    print(f"\n🎯 MagicBricks Final: {len(data_list)} properties")
    return data_list

# ============================================================================
# SULEKHA SCRAPER
# ============================================================================

def scrape_sulekha(pages=10):
    """Scrape Sulekha.com with detailed data extraction"""
    print("\n" + "="*70)
    print("SCRAPING SULEKHA.COM")
    print("="*70)
    
    data_list = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            slow_mo=500,
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        
        page = context.new_page()
        
        base_url = "https://www.sulekha.com/real-estate-agents/ahmedabad"
        
        for page_num in range(1, pages + 1):
            url = base_url if page_num == 1 else f"{base_url}?page={page_num}"
            
            print(f"\n📄 Page {page_num}/{pages}...")
            
            try:
                page.goto(url, timeout=60000, wait_until="domcontentloaded")
                time.sleep(4)
                
                page.evaluate("window.scrollTo(0, document.body.scrollHeight/2);")
                time.sleep(2)
                
                # Find property cards
                cards = page.locator("div.propcard, div[class*='property']").all()
                
                if len(cards) == 0:
                    print(f"  ⚠️ No cards found")
                    break
                
                print(f"  Found {len(cards)} listings")
                
                for card in cards:
                    try:
                        text_content = card.inner_text()
                        
                        if len(text_content) < 15:
                            continue
                        
                        property_data = {
                            'Property_Title': None,
                            'Price': None,
                            'Area_SqFt': None,
                            'BHK': None,
                            'Bathrooms': None,
                            'Furnishing_Status': None,
                            'Property_Type': None,
                            'Seller_Type': None,
                            'Project_Name': None,
                            'Locality': None,
                            'Posted_Date': None,
                            'Floor_Number': None,
                            'Source_Website': 'Sulekha',
                            'Raw_JSON': None,
                            'URL': None,
                            'Description': None
                        }
                        
                        lines = text_content.split('\n')
                        
                        # Title (first line)
                        property_data['Property_Title'] = lines[0].strip() if lines else None
                        
                        # Price (find line with ₹ or Lac or Cr)
                        price_line = next((l for l in lines if '₹' in l or 'Lac' in l or 'Cr' in l), None)
                        if price_line:
                            property_data['Price'] = clean_price_text(price_line)
                        
                        # Locality
                        property_data['Locality'] = lines[1].strip() if len(lines) > 1 else None
                        
                        # Extract from text
                        property_data['BHK'] = extract_bedrooms(text_content)
                        property_data['Bathrooms'] = extract_bathrooms(text_content)
                        property_data['Area_SqFt'] = extract_area(text_content)
                        property_data['Floor_Number'] = extract_floor(text_content)
                        property_data['Furnishing_Status'] = extract_furnishing(text_content)
                        
                        # Property Type
                        if property_data['Property_Title']:
                            title_upper = property_data['Property_Title'].upper()
                            if 'VILLA' in title_upper:
                                property_data['Property_Type'] = 'Villa'
                            elif 'PLOT' in title_upper:
                                property_data['Property_Type'] = 'Plot/Land'
                            elif 'INDEPENDENT' in title_upper:
                                property_data['Property_Type'] = 'Independent House'
                            else:
                                property_data['Property_Type'] = 'Apartment'
                        
                        # Seller Type
                        property_data['Seller_Type'] = 'Agent'  # Sulekha is mostly agents
                        
                        # URL
                        property_data['URL'] = page.url
                        
                        # Raw data
                        property_data['Raw_JSON'] = json.dumps(text_content[:500])
                        property_data['Description'] = text_content[:200]
                        
                        if property_data['Property_Title']:
                            data_list.append(property_data)
                    
                    except Exception as e:
                        continue
                
                print(f"  ✅ Total collected: {len(data_list)}")
            
            except Exception as e:
                print(f"  ❌ Error: {e}")
        
        browser.close()
    
    print(f"\n🎯 Sulekha Final: {len(data_list)} properties")
    return data_list

# ============================================================================
# MAIN FUNCTION
# ============================================================================

def remove_exact_duplicates(df):
    """Remove exact duplicates ignoring Source_Website column"""
    print("\n🔄 Removing exact duplicates (ignoring source)...")
    
    initial_count = len(df)
    
    # Create subset without Source_Website for duplicate detection
    columns_for_dup = [col for col in df.columns if col != 'Source_Website']
    
    # Drop duplicates based on all columns except Source_Website
    df_dedup = df.drop_duplicates(subset=columns_for_dup, keep='first')
    
    final_count = len(df_dedup)
    removed = initial_count - final_count
    
    print(f"  ✅ Removed {removed} exact duplicates")
    print(f"  📊 Kept {final_count} unique properties")
    
    return df_dedup

def main():
    print("\n" + "="*70)
    print("DETAILED MULTI-SOURCE SCRAPER")
    print("="*70)
    print("🎯 Sources: 99acres (50 pages), MagicBricks (150 pages), Sulekha (10 pages)")
    print("📊 Extract: All available property features")
    print("🗂️  Output: Separate CSV per source + Combined CSV")
    print("="*70)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Scrape each source
    all_data = {}
    
    # 99acres
    acres_data = scrape_99acres(pages=50)
    if acres_data:
        df_99acres = pd.DataFrame(acres_data)
        filename = f'data/raw/99acres_{timestamp}.csv'
        df_99acres.to_csv(filename, index=False)
        print(f"✅ Saved: {filename} ({len(df_99acres)} records)")
        all_data['99acres'] = df_99acres
    
    # MagicBricks (150 pages)
    mb_data = scrape_magicbricks(pages=150)
    if mb_data:
        df_mb = pd.DataFrame(mb_data)
        filename = f'data/raw/magicbricks_{timestamp}.csv'
        df_mb.to_csv(filename, index=False)
        print(f"✅ Saved: {filename} ({len(df_mb)} records)")
        all_data['MagicBricks'] = df_mb
    
    # Sulekha
    sulekha_data = scrape_sulekha(pages=10)
    if sulekha_data:
        df_sulekha = pd.DataFrame(sulekha_data)
        filename = f'data/raw/sulekha_{timestamp}.csv'
        df_sulekha.to_csv(filename, index=False)
        print(f"✅ Saved: {filename} ({len(df_sulekha)} records)")
        all_data['Sulekha'] = df_sulekha
    
    # Combine all sources
    if all_data:
        df_combined = pd.concat(all_data.values(), ignore_index=True)
        
        print("\n" + "="*70)
        print("COMBINED DATA SUMMARY")
        print("="*70)
        print(f"📊 Total records before deduplication: {len(df_combined)}")
        print(f"\n📊 By Source:")
        print(df_combined['Source_Website'].value_counts().to_string())
        
        # Remove exact duplicates (ignoring source)
        df_dedup = remove_exact_duplicates(df_combined)
        
        # Save combined file
        combined_filename = f'data/raw/all_sources_detailed_{timestamp}.csv'
        df_dedup.to_csv(combined_filename, index=False)
        
        print("\n" + "="*70)
        print("SCRAPING COMPLETED!")
        print("="*70)
        print(f"📁 Combined file: {combined_filename}")
        print(f"📊 Total unique properties: {len(df_dedup)}")
        print(f"\n📊 Final distribution by source:")
        print(df_dedup['Source_Website'].value_counts().to_string())
        
        # Show data quality
        print(f"\n📊 Data Completeness:")
        for col in ['Property_Title', 'Price', 'Area_SqFt', 'BHK', 'Bathrooms', 'Furnishing_Status', 'Property_Type', 'Locality']:
            non_null = df_dedup[col].notna().sum()
            pct = (non_null / len(df_dedup)) * 100
            print(f"  {col:25s}: {non_null:4d} / {len(df_dedup)} ({pct:5.1f}%)")
        
        print("="*70)
        
        return df_dedup
    else:
        print("\n❌ No data collected!")
        return None

if __name__ == "__main__":
    df = main()
    
    if df is not None:
        print("\n🔄 Next: python src/preprocessing/preprocess_detailed.py")
