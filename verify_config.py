from app.config import settings
import os

print("-" * 30)
print("CONFIG VERIFICATION")
print("-" * 30)

key = settings.GROQ_API_KEY
if key:
    masked = f"{key[:5]}...{key[-5:]}"
    print(f"✅ API Key Loaded: {masked}")
    print(f"✅ Length: {len(key)}")
else:
    print("❌ API Key NOT loaded!")

print("-" * 30)
