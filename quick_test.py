import os
from dotenv import load_dotenv

# Key from quick_test.py that WORKED
working_key = "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"  # Replace with your actual working key

# Key from .env
load_dotenv()
env_key = os.getenv("GROQ_API_KEY")

print("="*60)
print("COMPARING KEYS")
print("="*60)
print()

print("Working key (from quick_test.py):")
print(f"  Length: {len(working_key)}")
print(f"  Preview: {working_key[:15]}...{working_key[-15:]}")
print(f"  Full: {working_key}")
print()

print("Key from .env file:")
if env_key:
    print(f"  Length: {len(env_key)}")
    print(f"  Preview: {env_key[:15]}...{env_key[-15:]}")
    print(f"  Full: {env_key}")
    print()
    
    # Character by character comparison
    if working_key == env_key:
        print("✅ Keys are IDENTICAL!")
    else:
        print("❌ Keys are DIFFERENT!")
        print()
        print("Finding differences...")
        
        # Check length difference
        if len(working_key) != len(env_key):
            print(f"  Length mismatch: {len(working_key)} vs {len(env_key)}")
        
        # Check for extra spaces
        if env_key != env_key.strip():
            print(f"  .env key has extra whitespace!")
            print(f"  Raw: {repr(env_key)}")
        
        # Character comparison
        max_len = max(len(working_key), len(env_key))
        for i in range(max_len):
            if i >= len(working_key):
                print(f"  Position {i}: .env has extra char '{env_key[i]}' (ord={ord(env_key[i])})")
            elif i >= len(env_key):
                print(f"  Position {i}: .env is missing char '{working_key[i]}'")
            elif working_key[i] != env_key[i]:
                print(f"  Position {i}: '{working_key[i]}' vs '{env_key[i]}' (ord={ord(working_key[i])} vs {ord(env_key[i])})")
else:
    print("  ❌ NOT LOADED from .env!")
    print()
    print("Possible issues:")
    print("  1. .env file not found")
    print("  2. Variable name mismatch")
    print("  3. python-dotenv not installed")

print()
print("="*60)

# Test both keys
from groq import Groq

print()
print("Testing working key...")
try:
    client = Groq(api_key=working_key)
    client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "test"}],
        max_tokens=5
    )
    print("✅ Working key: SUCCESS")
except Exception as e:
    print(f"❌ Working key: FAILED - {e}")

if env_key:
    print()
    print("Testing .env key...")
    try:
        client = Groq(api_key=env_key)
        client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        print("✅ .env key: SUCCESS")
    except Exception as e:
        print(f"❌ .env key: FAILED - {e}")