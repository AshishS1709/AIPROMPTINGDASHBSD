import re
import json


def generate_text(prompt: str) -> dict:
    """
    Generates text using the Groq API. Returns a dictionary with the structured output.
    """
    try:
        from groq import Groq
        from app.config import settings
        
        key = settings.GROQ_API_KEY 
        masked_key = f"{key[:4]}...{key[-4:]}" if key and len(key) > 8 else "None"
        print(f"Using Groq API Key: {masked_key}")
        
        if not key:
            print("Error: GROQ_API_KEY is not set.")
            return {
                "headline": "",
                "caption": "",
                "cta": "",
                "hashtags": [],
                "design_prompt": ""
            }

        client = Groq(api_key=key)
        
        print(f"\n{'='*60}")
        print("SENDING PROMPT TO GROQ API")
        print(f"{'='*60}")
        print(f"Prompt length: {len(prompt)} characters")
        print(f"Model: llama-3.3-70b-versatile")
        print(f"{'='*60}\n")
        
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1024,
        )
        
        content = completion.choices[0].message.content
        
        print(f"\n{'='*60}")
        print("RAW RESPONSE FROM GROQ API")
        print(f"{'='*60}")
        print(content)
        print(f"{'='*60}\n")
        
        # Parse the response
        parsed = parse_structured_text(content)
        
        print(f"\n{'='*60}")
        print("PARSED RESULT")
        print(f"{'='*60}")
        print(f"Headline: {parsed.get('headline', 'MISSING')}")
        print(f"Caption: {parsed.get('caption', 'MISSING')[:100]}...")
        print(f"CTA: {parsed.get('cta', 'MISSING')}")
        print(f"Hashtags: {parsed.get('hashtags', [])}")
        print(f"Design Prompt: {parsed.get('design_prompt', 'MISSING')[:100]}...")
        print(f"{'='*60}\n")
        
        return parsed
        
    except Exception as e:
        import traceback
        print(f"\n{'='*60}")
        print("ERROR IN TEXT GENERATION")
        print(f"{'='*60}")
        print(f"Error: {e}")
        traceback.print_exc()
        print(f"{'='*60}\n")
        return {
            "headline": "",
            "caption": "",
            "cta": "",
            "hashtags": [],
            "design_prompt": ""
        }


def parse_structured_text(content: str) -> dict:
    """
    Parses the structured text format into a dictionary.
    Handles various formatting styles (same-line, next-line, case differences).
    """
    result = {
        "headline": "",
        "caption": "",
        "cta": "",
        "hashtags": [],
        "design_prompt": ""
    }
    
    # Strip all input content to handle leading/trailing newlines
    content = content.strip()
    
    print(f"\n{'='*60}")
    print("PARSING STRUCTURED TEXT")
    print(f"{'='*60}")
    print(f"Content length: {len(content)} characters")
    print(f"{'='*60}\n")
    
    # Define patterns for each field
    # These patterns are designed to be flexible and handle various formats
    patterns = {
        "headline": r"Headline:\s*(.*?)(?=\n(?:Caption:|CTA:|Hashtags:|IMAGE PROMPT:?)|$)",
        "caption": r"Caption:\s*(.*?)(?=\n(?:CTA:|Hashtags:|IMAGE PROMPT:?)|$)",
        "cta": r"CTA:\s*(.*?)(?=\n(?:Hashtags:|IMAGE PROMPT:?)|$)",
        "hashtags": r"Hashtags:\s*(.*?)(?=\n(?:IMAGE PROMPT:?)|$)",
        "design_prompt": r"IMAGE PROMPT:?\s*(.*)"
    }
    
    try:
        for key, pattern in patterns.items():
            # Using re.DOTALL to match across newlines and re.IGNORECASE for case-insensitive matching
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                value = match.group(1).strip()
                
                if key == "hashtags":
                    # Clean up hashtags: remove #, split by space/newline/comma
                    raw_tags = re.split(r'[\s,]+', value.replace('\n', ' '))
                    result["hashtags"] = [t.strip().lstrip('#') for t in raw_tags if t.strip() and t.strip() != '#']
                else:
                    # For other fields, clean up extra whitespace and newlines
                    value = ' '.join(value.split())
                    result[key] = value
                
                print(f"✓ Parsed {key}: {result[key] if key != 'hashtags' else result[key]}")
            else:
                print(f"✗ Failed to parse {key}")
        
        # Validation: Check if we got at least some content
        if not result["headline"] and not result["caption"] and not result["design_prompt"]:
            print("\n⚠ WARNING: No content was parsed successfully!")
            print("This might indicate a format mismatch between the prompt and the AI response.")
            print("\nAttempting fallback parsing...")
            
            # Fallback: Try to extract any text that looks like content
            lines = content.split('\n')
            for i, line in enumerate(lines):
                line = line.strip()
                if line and not any(keyword in line.upper() for keyword in ['POST TEXT', 'HEADLINE:', 'CAPTION:', 'CTA:', 'HASHTAGS:', 'IMAGE PROMPT']):
                    if not result["headline"]:
                        result["headline"] = line
                        print(f"Fallback: Set headline to: {line}")
                    elif not result["caption"]:
                        result["caption"] = line
                        print(f"Fallback: Set caption to: {line}")
        
        print(f"\n{'='*60}")
        print("FINAL PARSED RESULT")
        print(f"{'='*60}")
        for key, value in result.items():
            if key == "hashtags":
                print(f"{key}: {value}")
            else:
                display_value = value[:100] + "..." if len(str(value)) > 100 else value
                print(f"{key}: {display_value}")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"\n{'='*60}")
        print("ERROR PARSING STRUCTURED TEXT")
        print(f"{'='*60}")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        print(f"{'='*60}\n")
    
    return result


if __name__ == "__main__":
    print("text_gen.py loaded successfully")
    print(f"generate_text function: {generate_text}")
    print(f"parse_structured_text function: {parse_structured_text}")