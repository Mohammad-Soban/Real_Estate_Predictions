"""
Property Summary Generator using Open-Source LLMs
Uses DeepSeek or Hugging Face models to generate:
- Clean short summaries
- Marketing-style descriptions
- Investor-focused summaries
"""

import os
from typing import Dict, Optional
import warnings
warnings.filterwarnings('ignore')

class PropertySummaryGenerator:
    """Generate property summaries using open-source LLMs"""
    
    def __init__(self, model_name: str = "deepseek-ai/deepseek-llm-7b-chat", use_local: bool = False):
        """
        Initialize the summary generator
        
        Args:
            model_name: HuggingFace model name (default: DeepSeek-7B)
            use_local: If True, use local model. If False, use HF API (requires API key)
        """
        self.model_name = model_name
        self.use_local = use_local
        self.model = None
        self.tokenizer = None
        
        # Check if we should initialize the model
        if use_local:
            self._init_local_model()
    
    def _init_local_model(self):
        """Initialize local transformer model (memory intensive)"""
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM
            import torch
            
            print(f"🔄 Loading {self.model_name}...")
            print("⚠️  This may take a few minutes and requires ~8GB RAM")
            
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None,
                low_cpu_mem_usage=True
            )
            
            print("✅ Model loaded successfully!")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            print("💡 Tip: Use use_local=False for API-based generation (no local resources needed)")
            self.use_local = False
    
    def _generate_with_local_model(self, prompt: str, max_length: int = 200) -> str:
        """Generate text using local model"""
        if not self.model or not self.tokenizer:
            return "Error: Model not initialized"
        
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
            
            if hasattr(self.model, 'device'):
                inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
            
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_length,
                temperature=0.7,
                do_sample=True,
                top_p=0.9,
                num_return_sequences=1
            )
            
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Remove the prompt from output
            if prompt in generated_text:
                generated_text = generated_text.replace(prompt, "").strip()
            
            return generated_text
            
        except Exception as e:
            return f"Generation error: {e}"
    
    def _generate_with_template(self, property_data: Dict, template_type: str) -> str:
        """
        Generate summary using template-based approach (no LLM required)
        Fallback method for when LLM is not available
        """
        bhk = property_data.get('BHK', 'N/A')
        area = property_data.get('Area_SqFt', 'N/A')
        locality = property_data.get('Locality', 'Unknown')
        price = property_data.get('Price_Lakhs', 'N/A')
        property_type = property_data.get('Property_Type', 'Property')
        furnishing = property_data.get('Furnishing_Status', 'Unfurnished')
        amenities = property_data.get('Amenities_Count', 0)
        
        if template_type == "clean":
            return (f"{bhk} BHK {property_type} in {locality}, Ahmedabad. "
                   f"Covering {area} sqft, this {furnishing.lower()} property is priced at ₹{price} Lakhs. "
                   f"Features {amenities} amenities.")
        
        elif template_type == "marketing":
            quality_words = ["Stunning", "Beautiful", "Exceptional", "Premium", "Elegant"]
            quality = quality_words[int(bhk) % len(quality_words)] if isinstance(bhk, (int, float)) else "Beautiful"
            
            return (f"{quality} {bhk} BHK {property_type} in the heart of {locality}! "
                   f"Spanning {area} sqft of thoughtfully designed space. "
                   f"This {furnishing.lower()} home offers {amenities} modern amenities. "
                   f"Available at an attractive price of ₹{price} Lakhs. "
                   f"Perfect for families looking for comfort and convenience!")
        
        elif template_type == "investor":
            price_sqft = float(price) * 100000 / float(area) if price != 'N/A' and area != 'N/A' else 0
            
            return (f"Investment Opportunity: {bhk} BHK {property_type} in {locality}. "
                   f"Property size: {area} sqft | Price: ₹{price} Lakhs | "
                   f"Price per sqft: ₹{price_sqft:.0f}. "
                   f"Located in {'a premium' if 'Tier 1' in str(property_data.get('Locality_Tier', '')) else 'an emerging'} area. "
                   f"{furnishing} status with {amenities} amenities. "
                   f"{'High rental potential' if property_type == 'Apartment' else 'Strong appreciation potential'}.")
        
        return "Summary not available"
    
    def generate_clean_summary(self, property_data: Dict) -> str:
        """Generate a clean, factual summary"""
        if not self.use_local or not self.model:
            return self._generate_with_template(property_data, "clean")
        
        prompt = f"""Summarize this property in 2-3 sentences (factual, clean):
Property: {property_data.get('BHK')} BHK, {property_data.get('Area_SqFt')} sqft
Location: {property_data.get('Locality')}, Ahmedabad
Price: ₹{property_data.get('Price_Lakhs')} Lakhs
Type: {property_data.get('Property_Type')}
Furnishing: {property_data.get('Furnishing_Status')}
Amenities: {property_data.get('Amenities_Count')}

Clean Summary:"""
        
        return self._generate_with_local_model(prompt, max_length=100)
    
    def generate_marketing_summary(self, property_data: Dict) -> str:
        """Generate an attractive marketing-style description"""
        if not self.use_local or not self.model:
            return self._generate_with_template(property_data, "marketing")
        
        prompt = f"""Write an attractive marketing description for this property (3-4 sentences, emotional):
Property: {property_data.get('BHK')} BHK, {property_data.get('Area_SqFt')} sqft
Location: {property_data.get('Locality')}, Ahmedabad
Price: ₹{property_data.get('Price_Lakhs')} Lakhs
Type: {property_data.get('Property_Type')}
Amenities: {property_data.get('Amenities_Count')}

Marketing Description:"""
        
        return self._generate_with_local_model(prompt, max_length=150)
    
    def generate_investor_summary(self, property_data: Dict) -> str:
        """Generate an investor-focused analysis"""
        if not self.use_local or not self.model:
            return self._generate_with_template(property_data, "investor")
        
        prompt = f"""Write an investor-focused analysis for this property (ROI, appreciation, rental potential):
Property: {property_data.get('BHK')} BHK, {property_data.get('Area_SqFt')} sqft
Location: {property_data.get('Locality')}, Ahmedabad (Tier: {property_data.get('Locality_Tier')})
Price: ₹{property_data.get('Price_Lakhs')} Lakhs
Type: {property_data.get('Property_Type')}

Investor Analysis:"""
        
        return self._generate_with_local_model(prompt, max_length=150)
    
    def generate_all_summaries(self, property_data: Dict) -> Dict[str, str]:
        """Generate all three types of summaries"""
        return {
            'clean_summary': self.generate_clean_summary(property_data),
            'marketing_summary': self.generate_marketing_summary(property_data),
            'investor_summary': self.generate_investor_summary(property_data)
        }


if __name__ == "__main__":
    # Test the generator (template mode - no LLM needed)
    generator = PropertySummaryGenerator(use_local=False)
    
    test_property = {
        'BHK': 3,
        'Area_SqFt': 1500,
        'Locality': 'Bopal',
        'Price_Lakhs': 75,
        'Property_Type': 'Apartment',
        'Furnishing_Status': 'Semi-Furnished',
        'Amenities_Count': 4,
        'Locality_Tier': 'Tier 1'
    }
    
    print("="*80)
    print("PROPERTY SUMMARY GENERATOR TEST (Template Mode)")
    print("="*80)
    print(f"\nProperty Details:")
    for key, value in test_property.items():
        print(f"  {key}: {value}")
    
    print("\n" + "="*80)
    print("GENERATED SUMMARIES")
    print("="*80)
    
    summaries = generator.generate_all_summaries(test_property)
    
    print("\n📄 Clean Summary:")
    print(f"   {summaries['clean_summary']}")
    
    print("\n📣 Marketing Summary:")
    print(f"   {summaries['marketing_summary']}")
    
    print("\n💼 Investor Summary:")
    print(f"   {summaries['investor_summary']}")
    
    print("\n" + "="*80)
    print("💡 Tip: Set use_local=True to use DeepSeek LLM (requires 8GB+ RAM)")
    print("="*80)
