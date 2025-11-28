"""
Real Estate Property Chatbot using Ollama
Ask questions about your entire property dataset!
"""

import pandas as pd
import requests
import json
from datetime import datetime

class PropertyChatbot:
    """Chatbot for querying property dataset using Ollama"""
    
    def __init__(self, csv_path: str, ollama_url: str = "http://localhost:11434", model: str = "llama2"):
        """
        Initialize chatbot with property dataset
        
        Args:
            csv_path: Path to your property CSV file
            ollama_url: Ollama server URL
            model: Ollama model to use (llama2, llama3.1, mistral)
        """
        self.csv_path = csv_path
        self.ollama_url = ollama_url
        self.model = model
        
        # Load dataset
        print(f"📊 Loading dataset from: {csv_path}")
        self.df = pd.read_csv(csv_path)
        print(f"✅ Loaded {len(self.df)} properties")
        
        # Create dataset summary for context
        self.dataset_summary = self._create_dataset_summary()
        
        # Check Ollama
        if not self._check_ollama():
            raise ConnectionError("Ollama is not running! Please start it first.")
        
        print(f"🏠 Chatbot ready with {model} model!")
    
    def _check_ollama(self) -> bool:
        """Check if Ollama is available"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def _create_dataset_summary(self) -> str:
        """Create a summary of the dataset for context"""
        summary = f"""
Dataset Overview:
- Total Properties: {len(self.df)}
- Columns: {', '.join(self.df.columns.tolist())}

Property Statistics:
- BHK Range: {self.df['BHK'].min()} to {self.df['BHK'].max()}
- Price Range: ₹{self.df['Price_Lakhs'].min():.1f}L to ₹{self.df['Price_Lakhs'].max():.1f}L
- Area Range: {self.df['Area_SqFt'].min():.0f} to {self.df['Area_SqFt'].max():.0f} sqft
- Localities: {self.df['Locality'].nunique()} unique locations
- Top Localities: {', '.join(self.df['Locality'].value_counts().head(5).index.tolist())}

Property Types: {', '.join(self.df['Property_Type'].value_counts().index.tolist())}
"""
        return summary
    
    def _get_relevant_data(self, question: str) -> str:
        """Extract relevant data based on the question"""
        question_lower = question.lower()
        
        # Initialize result
        relevant_info = []
        
        # Check what the question is about
        if any(word in question_lower for word in ['cheapest', 'affordable', 'budget', 'lowest price']):
            cheap_props = self.df.nsmallest(5, 'Price_Lakhs')[['BHK', 'Locality', 'Price_Lakhs', 'Area_SqFt']]
            relevant_info.append(f"Top 5 Most Affordable Properties:\n{cheap_props.to_string()}")
        
        if any(word in question_lower for word in ['expensive', 'luxury', 'premium', 'highest price']):
            exp_props = self.df.nlargest(5, 'Price_Lakhs')[['BHK', 'Locality', 'Price_Lakhs', 'Area_SqFt']]
            relevant_info.append(f"Top 5 Most Expensive Properties:\n{exp_props.to_string()}")
        
        if any(word in question_lower for word in ['average', 'mean']):
            avg_stats = f"""
Average Statistics:
- Average Price: ₹{self.df['Price_Lakhs'].mean():.2f} Lakhs
- Average Area: {self.df['Area_SqFt'].mean():.0f} sqft
- Average Price/sqft: ₹{self.df['Price_Per_SqFt'].mean():.0f}
"""
            relevant_info.append(avg_stats)
        
        # Check for specific localities
        for locality in self.df['Locality'].unique():
            if locality.lower() in question_lower:
                loc_data = self.df[self.df['Locality'] == locality]
                loc_info = f"""
{locality} Statistics:
- Total Properties: {len(loc_data)}
- Price Range: ₹{loc_data['Price_Lakhs'].min():.1f}L to ₹{loc_data['Price_Lakhs'].max():.1f}L
- Average Price: ₹{loc_data['Price_Lakhs'].mean():.2f}L
- BHK Options: {sorted(loc_data['BHK'].unique())}
"""
                relevant_info.append(loc_info)
                
                # Show sample properties
                sample = loc_data.head(3)[['BHK', 'Price_Lakhs', 'Area_SqFt', 'Furnishing_Status']]
                relevant_info.append(f"Sample Properties:\n{sample.to_string()}")
                break
        
        # Check for BHK-specific questions
        for bhk in [1, 2, 3, 4, 5]:
            if f'{bhk} bhk' in question_lower or f'{bhk}bhk' in question_lower:
                bhk_data = self.df[self.df['BHK'] == bhk]
                if len(bhk_data) > 0:
                    bhk_info = f"""
{bhk} BHK Properties:
- Total Available: {len(bhk_data)}
- Price Range: ₹{bhk_data['Price_Lakhs'].min():.1f}L to ₹{bhk_data['Price_Lakhs'].max():.1f}L
- Average Price: ₹{bhk_data['Price_Lakhs'].mean():.2f}L
- Best Localities: {', '.join(bhk_data['Locality'].value_counts().head(3).index.tolist())}
"""
                    relevant_info.append(bhk_info)
        
        # If no specific data found, return general summary
        if not relevant_info:
            return self.dataset_summary
        
        return "\n\n".join(relevant_info)
    
    def ask(self, question: str) -> str:
        """
        Ask a question about the properties
        
        Args:
            question: Your question about the dataset
            
        Returns:
            AI-generated answer
        """
        # Get relevant data
        relevant_data = self._get_relevant_data(question)
        
        # Create prompt for Ollama
        prompt = f"""You are a helpful real estate assistant. Answer the user's question based on the property data provided.

{relevant_data}

User Question: {question}

Provide a clear, helpful answer based on the data above. If asked for recommendations, explain your reasoning. Be specific with numbers and details."""
        
        print("\n🤔 Thinking...")
        
        try:
            # Call Ollama
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 500
                    }
                },
                timeout=90
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get('response', '')
                return answer.strip()
            else:
                return f"Error: Ollama returned status {response.status_code}"
                
        except requests.exceptions.Timeout:
            return "Error: Request timed out. The model might be processing..."
        except Exception as e:
            return f"Error: {str(e)}"
    
    def chat(self):
        """Start interactive chat session"""
        print("\n" + "="*80)
        print(" "*20 + "🏠 PROPERTY CHATBOT 🤖")
        print("="*80)
        print(f"\n✅ Connected to dataset: {len(self.df)} properties")
        print(f"🏠 Using Ollama model: {self.model}")
        print("\n💡 Example questions:")
        print("   - What are the cheapest 3 BHK apartments?")
        print("   - Show me properties in Vastrapur")
        print("   - What's the average price per sqft?")
        print("   - Which locality has most properties?")
        print("   - Recommend a good property for first-time buyer")
        print("\nType 'exit' or 'quit' to end the conversation.")
        print("="*80 + "\n")
        
        conversation_history = []
        
        while True:
            # Get user question
            question = input("\n👤 You: ").strip()
            
            if not question:
                continue
            
            if question.lower() in ['exit', 'quit', 'bye']:
                print("\n👋 Thank you for using Property Chatbot! Goodbye!\n")
                break
            
            # Get answer
            answer = self.ask(question)
            
            # Print answer
            print(f"\n🤖 Chatbot:\n{answer}")
            
            # Save to history
            conversation_history.append({
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'question': question,
                'answer': answer
            })
    
    def save_conversation(self, conversation_history: list, filename: str = None):
        """Save conversation history to file"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'data/results/chatbot_conversation_{timestamp}.txt'
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("PROPERTY CHATBOT CONVERSATION HISTORY\n")
            f.write("="*80 + "\n\n")
            
            for entry in conversation_history:
                f.write(f"[{entry['timestamp']}]\n")
                f.write(f"Q: {entry['question']}\n")
                f.write(f"A: {entry['answer']}\n")
                f.write("\n" + "-"*80 + "\n\n")
        
        print(f"\n💾 Conversation saved to: {filename}")


def main():
    """Main function to run the chatbot"""
    import sys
    
    print("\n" + "="*80)
    print(" "*20 + "🏠 PROPERTY DATASET CHATBOT")
    print("="*80)
    
    # Choose dataset file
    print("\n📂 Available dataset files:")
    print("  1. data/cleaned/cleaned_data.csv (Main dataset - 2,783 properties)")
    print("  2. data/results/buyer_analysis_*.csv (AI-analyzed dataset with insights)")
    print("  3. Custom path")
    
    choice = input("\nSelect dataset (1/2/3): ").strip()
    
    if choice == '1':
        csv_path = 'data/cleaned/cleaned_data.csv'
    elif choice == '2':
        # Find the latest buyer analysis file
        import glob
        files = glob.glob('data/results/buyer_analysis_*.csv')
        if files:
            csv_path = sorted(files)[-1]  # Get the latest
            print(f"\n📊 Using: {csv_path}")
        else:
            print("\n❌ No buyer analysis files found. Using main dataset.")
            csv_path = 'data/cleaned/cleaned_data.csv'
    else:
        csv_path = input("Enter CSV path: ").strip()
    
    # Choose model
    print("\n🤖 Available Ollama models:")
    print("  1. llama2 (Fast, 4GB)")
    print("  2. llama3.1 (Best quality, 7GB)")
    print("  3. mistral (Balanced, 4GB)")
    
    model_choice = input("\nSelect model (1/2/3, default=1): ").strip()
    
    model_map = {
        '1': 'llama2',
        '2': 'llama3.1',
        '3': 'mistral',
        '': 'llama2'
    }
    
    model = model_map.get(model_choice, 'llama2')
    
    try:
        # Initialize chatbot
        chatbot = PropertyChatbot(csv_path, model=model)
        
        # Start chat
        chatbot.chat()
        
    except FileNotFoundError:
        print(f"\n❌ Error: File not found: {csv_path}")
        print("Please check the file path and try again.")
    except ConnectionError as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 To fix:")
        print("   $env:PATH += ';$env:LOCALAPPDATA\\Programs\\Ollama'")
        print("   ollama list")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
