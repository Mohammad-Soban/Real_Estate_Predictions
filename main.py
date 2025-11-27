"""
MAIN MENU - Real Estate Price Prediction Pipeline
Interactive menu for all operations
"""
import subprocess
import sys

def print_menu():
    print("\n" + "="*80)
    print("AHMEDABAD REAL ESTATE PRICE PREDICTION - MAIN MENU")
    print("="*80)
    print("\n📋 Available Options:\n")
    print("  1. Run Complete Pipeline (Preprocess + Train + Visualize)")
    print("  2. Run Preprocessing Only (Simple + Enhanced)")
    print("  3. Train Models Only (9 Models)")
    print("  4. Generate Visualizations Only (21 Charts)")
    print("  5. Predict Single Property Price")
    print("  6. Scrape New Data (99acres, MagicBricks, Sulekha)")
    print("  0. Exit")
    print("\n" + "="*80)

def run_complete_pipeline():
    """Run preprocessing, training, and visualization"""
    print("\n🚀 Running Complete Pipeline...")
    print("="*80)
    result = subprocess.run([sys.executable, "main2.py"])
    return result.returncode == 0

def run_preprocessing():
    """Run both simple and enhanced preprocessing"""
    print("\n🔧 Running Preprocessing...")
    print("="*80)
    
    print("\n[1/2] Simple Preprocessing...")
    result = subprocess.run([sys.executable, "src/preprocessing/preprocess_simple.py"])
    if result.returncode != 0:
        print("❌ Simple preprocessing failed!")
        return False
    
    print("\n[2/2] Enhanced Preprocessing...")
    result = subprocess.run([sys.executable, "src/preprocessing/preprocess_enhanced.py"])
    if result.returncode != 0:
        print("❌ Enhanced preprocessing failed!")
        return False
    
    print("\n✅ Preprocessing Complete!")
    return True

def train_models():
    """Train all 9 models"""
    print("\n🎯 Training Models...")
    print("="*80)
    result = subprocess.run([sys.executable, "src/modeling/train_all.py"])
    if result.returncode == 0:
        print("\n✅ Training Complete!")
        return True
    else:
        print("❌ Training failed!")
        return False

def generate_visualizations():
    """Generate all 21 visualizations"""
    print("\n📊 Generating Visualizations...")
    print("="*80)
    result = subprocess.run([sys.executable, "src/visualize.py"])
    if result.returncode == 0:
        print("\n✅ Visualizations Complete!")
        print("📁 Saved in: visualizations/")
        return True
    else:
        print("❌ Visualization failed!")
        return False

def predict_single_property():
    """Predict price for a single property"""
    print("\n🏠 Predicting Property Price...")
    print("="*80)
    result = subprocess.run([sys.executable, "src/predict.py"])
    if result.returncode == 0:
        return True
    else:
        print("❌ Prediction failed!")
        return False

def scrape_data():
    """Scrape new data from all sources"""
    print("\n🌐 Scraping Data...")
    print("="*80)
    print("⚠️  This will take 30-45 minutes!")
    confirm = input("Continue? (y/n): ")
    if confirm.lower() != 'y':
        print("❌ Scraping cancelled.")
        return False
    
    result = subprocess.run([sys.executable, "src/scraping/scrape_all_sources_detailed.py"])
    if result.returncode == 0:
        print("\n✅ Scraping Complete!")
        print("📁 Data saved in: data/raw/")
        return True
    else:
        print("❌ Scraping failed!")
        return False

def main():
    """Main menu loop"""
    while True:
        print_menu()
        try:
            choice = input("\n👉 Enter your choice (0-6): ").strip()
            
            if choice == '0':
                print("\n👋 Goodbye!")
                break
            elif choice == '1':
                run_complete_pipeline()
            elif choice == '2':
                run_preprocessing()
            elif choice == '3':
                train_models()
            elif choice == '4':
                generate_visualizations()
            elif choice == '5':
                predict_single_property()
            elif choice == '6':
                scrape_data()
            else:
                print("\n❌ Invalid choice! Please enter 0-6.")
            
            input("\n⏸️  Press Enter to continue...")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("\n⏸️  Press Enter to continue...")

if __name__ == "__main__":
    main()
