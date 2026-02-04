from app.schemas import BrandProfile, ContentCategory

def validate_output(text_json: dict, profile: BrandProfile, content_category: ContentCategory = None) -> tuple[bool, str]:
    """
    Validates the generated output against the brand profile.
    Checks for:
    - Required fields (headline, caption, hashtags, design_prompt)
    - Forbidden words
    - No placeholders or dummy data
    - Category-specific rules
    
    Returns (is_valid, error_message)
    """
    
    # Check structure
    required_fields = ["headline", "caption", "hashtags", "design_prompt"]
    for field in required_fields:
        if field not in text_json:
            return False, f"Missing field: {field}"

    # Content to check
    full_text = f"{text_json.get('headline', '')} {text_json.get('caption', '')} {text_json.get('cta', '')}".lower()
    
    # Check forbidden words
    for word in profile.forbidden_words:
        if word.lower() in full_text:
            return False, f"Forbidden word found: {word}"
    
    # Check for placeholders (XXXXX, dummy data)
    placeholder_patterns = ['xxxxx', 'xxxx', 'placeholder', 'dummy', '[insert', '[add']
    for pattern in placeholder_patterns:
        if pattern in full_text:
            return False, f"Placeholder text found: {pattern}"
    
    # Category-specific validation
    if content_category == ContentCategory.FESTIVAL_OCCASION:
        # Festival posts should be warm and celebratory, not salesy
        salesy_words = ['buy', 'purchase', 'sale', 'discount', 'offer', 'limited time']
        for word in salesy_words:
            if word in full_text:
                return False, f"Festival post contains selling language: {word}"
    
    # Note: Brand name and phone number are not strictly required in all content categories
    # (e.g., educational posts, engagement posts may not need them)
    # So we don't fail validation if they're missing, but we could log a warning
    
    return True, ""

