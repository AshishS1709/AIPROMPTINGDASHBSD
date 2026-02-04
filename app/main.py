from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from fastapi.responses import FileResponse
from app.schemas import GenerationRequest, GenerationResponse
from app.services.prompt_engine import assemble_prompt
from app.services.text_gen import generate_text
from app.core.validation import validate_output
from dotenv import load_dotenv
load_dotenv(override=True)

app = FastAPI(title="AI Social Media Content Engine")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for frontend
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if not os.path.exists(frontend_dir):
    os.makedirs(frontend_dir)
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
def root():
    return FileResponse(os.path.join(frontend_dir, "index.html"))

@app.post("/generate-post", response_model=GenerationResponse)
async def generate_post(request: GenerationRequest):
    # 1. Assemble Prompt
    prompt = assemble_prompt(request.profile, request.brief, request.instructions)
    print(f"Generated text prompt: {prompt}")

    # 2. Text Generation (Groq)
    text_data = generate_text(prompt)
    if not text_data:
        raise HTTPException(status_code=500, detail="Failed to generate text content.")
    
    # 3. Validation
    is_valid, error_msg = validate_output(text_data, request.profile, request.brief.content_category)
    if not is_valid:
        print(f"Validation failed: {error_msg}")
    
    # 4. Design Prompt (No Image Generation)
    design_prompt = text_data.get("design_prompt")
    
    return GenerationResponse(
        headline=text_data.get("headline", ""),
        caption=text_data.get("caption", ""),
        cta=text_data.get("cta", ""),
        hashtags=text_data.get("hashtags", []),
        design_prompt=design_prompt,
        image_url=None,
        cost_metadata={"status": "logged"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
