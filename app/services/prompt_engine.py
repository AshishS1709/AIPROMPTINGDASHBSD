from app.schemas import BrandProfile, ContentBrief, AgencyInstructions, ContentCategory

def assemble_prompt(profile: BrandProfile, brief: ContentBrief, instructions: AgencyInstructions = None) -> str:
    """
    Assembles the final prompt for the AI model based on the brand profile, content brief, and instructions.
    This prompt implements the exact requirements from the user specification.
    """
    
    # Build category-specific behavior instructions (internal logic)
    category_behavior = get_category_behavior(brief.content_category, brief.cta_enabled)
    
    # Build festival-specific instructions if applicable
    festival_instructions = ""
    if brief.content_category == ContentCategory.FESTIVAL_OCCASION:
        festival_instructions = f"""
FESTIVAL DETAILS:
Festival Name: {brief.festival_name}
Festival Type: {brief.festival_type}
CTA Enabled: {"Yes" if brief.cta_enabled else "No"}
"""
    
    prompt = f"""You are a senior social media strategist and creative director
working inside a professional social media marketing platform.

Your job is to generate HIGH-QUALITY, ACCURATE, READY-TO-USE
social media content for brands.

STRICT RULES (NON-NEGOTIABLE):
1. You MUST ALWAYS generate TWO THINGS:
   a) Post text content
   b) Image generation prompt

2. You must NEVER generate images.
3. You must NEVER return JSON.
4. You must NEVER explain your output.
5. You must NEVER include placeholders like XXXXX or dummy numbers.
6. Follow the brand details EXACTLY as provided.
7. Do NOT modify brand name, phone number, or CTA text.
8. Adapt tone, writing style, and visuals strictly based on Content Category.
9. Avoid spam, exaggeration, clickbait, or excessive emojis.
10. Output must be clean, professional, and ready to copy-paste.

BRAND DETAILS:
Brand Name: {profile.name}
Industry: {profile.industry}
Primary Service: {profile.primary_service}
Target Audience: {profile.target_audience}
Brand Tone: {profile.tone}
Phone Number / CTA Contact: {profile.phone}
CTA Text: {profile.cta}

CONTENT DETAILS:
Platform: {brief.platform}
Content Category: {brief.content_category.value}
Topic / Goal: {brief.topic}

{festival_instructions}

CONTENT CATEGORY BEHAVIOR (INTERNAL LOGIC):
{category_behavior}

REQUIRED OUTPUT FORMAT (STRICT – PLAIN TEXT ONLY):

Your response MUST follow this structure exactly:

POST TEXT
Headline:
<one clear, professional headline>

Caption:
<clean, well-written caption aligned with content category>

CTA:
<include CTA only if applicable>

Hashtags:
<relevant, non-spammy hashtags>


IMAGE PROMPT
Create a professional 1080x1080 social media post design with
<clear visual description>.
The style should match the brand tone and content category.
Mention colors, layout, mood, and visual elements clearly.
The design must be clean, modern, premium, and uncluttered.

REMEMBER:
- NO JSON format
- NO placeholders or dummy data
- Brand details must be EXACT
- Output must be ready to copy-paste
- Follow content category behavior strictly
"""
    
    if instructions and instructions.extra_instructions:
        prompt += f"\n\nADDITIONAL INSTRUCTIONS:\n{instructions.extra_instructions}\n"
    
    return prompt


def get_category_behavior(category: ContentCategory, cta_enabled: bool = False) -> str:
    """
    Returns category-specific behavior instructions.
    This is internal logic that guides the AI but is not exposed in the output.
    """
    
    behaviors = {
        ContentCategory.SERVICE_PROMOTION: """
- Focus on benefits, growth, leads, ROI
- CTA should be strong and clear
- Highlight results and transformation
- Professional and persuasive tone
""",
        ContentCategory.BRAND_AWARENESS: """
- Focus on trust, positioning, credibility
- CTA is soft or optional
- Build brand reputation and authority
- Emphasize values and mission
""",
        ContentCategory.FESTIVAL_OCCASION: f"""
- Mention the specific festival explicitly
- Emotional, respectful, culturally appropriate
- NO selling language
- CTA only if CTA Enabled = Yes (currently: {"Yes" if cta_enabled else "No"})
- Warm, celebratory, and genuine tone
- Focus on wishes and celebration, not promotion
""",
        ContentCategory.TRENDING_TOPIC: """
- Opinionated, expert, insightful
- Position brand as knowledgeable
- Add value to the conversation
- Thought leadership tone
""",
        ContentCategory.EDUCATIONAL: """
- Teach ONE clear idea
- Encourage save, learn, or awareness
- Minimal CTA
- Helpful and informative tone
- Break down complex topics simply
""",
        ContentCategory.FOUNDER_TEAM: """
- Human, authentic, trust-building
- No selling tone
- Share story, journey, or behind-the-scenes
- Personal and relatable
""",
        ContentCategory.TESTIMONIAL: """
- Social proof, confidence, credibility
- Professional tone
- Real results and experiences
- Build trust through customer success
""",
        ContentCategory.ENGAGEMENT_POST: """
- Ask a clear question
- Encourage comments or interaction
- NO selling
- Conversational and inviting tone
- Make audience feel heard
"""
    }
    
    return behaviors.get(category, "")

