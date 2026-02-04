from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class ContentCategory(str, Enum):
    SERVICE_PROMOTION = "Service Promotion"
    BRAND_AWARENESS = "Brand Awareness"
    FESTIVAL_OCCASION = "Festival / Occasion"
    TRENDING_TOPIC = "Trending Topic"
    EDUCATIONAL = "Educational"
    FOUNDER_TEAM = "Founder / Team"
    TESTIMONIAL = "Testimonial"
    ENGAGEMENT_POST = "Engagement Post"

class BrandProfile(BaseModel):
    name: str
    industry: str
    primary_service: str
    target_audience: str
    tone: str
    phone: str
    cta: str
    forbidden_words: List[str] = []

class ContentBrief(BaseModel):
    platform: str
    content_category: ContentCategory
    topic: str
    # Festival-specific fields (only used when content_category = Festival / Occasion)
    festival_name: Optional[str] = None
    festival_type: Optional[str] = None
    cta_enabled: Optional[bool] = False

class AgencyInstructions(BaseModel):
    extra_instructions: Optional[str] = None

class GenerationRequest(BaseModel):
    profile: BrandProfile
    brief: ContentBrief
    instructions: Optional[AgencyInstructions] = None

class GenerationResponse(BaseModel):
    headline: str
    caption: str
    cta: str
    hashtags: List[str]
    design_prompt: str
    image_url: Optional[str] = None
    cost_metadata: Optional[dict] = None
