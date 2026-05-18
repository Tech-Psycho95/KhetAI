import base64
import json
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import ollama
from pydantic import BaseModel, Field
from typing import List, Optional

# --- Configuration ---
OLLAMA_MODEL = "gemma4:e4b"

# --- Pydantic Models ---
class AnalysisResponse(BaseModel):
    diagnosis: str
    confidence: str
    treatment: List[str]
    prevention: List[str]
    local_remedies: List[str] = Field(..., alias="local_remedies")
    escalate: bool
    escalate_reason: Optional[str] = None
    summary: str

class HealthCheck(BaseModel):
    model_name: str

# --- FastAPI App Initialization ---
app = FastAPI(
    title="AgriAdvisor API",
    description="AI-powered crop disease diagnostic tool for farmers.",
    version="1.0.0"
)

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- System Prompt for AI Model ---
SYSTEM_PROMPT = """
You are an expert agricultural diagnostic AI, AgriAdvisor. Your purpose is to help Indian farmers by analyzing images of their crops and answering their questions.

You MUST follow these rules:
1.  Analyze the user's image (provided as base64) and their question.
2.  Your entire response MUST be a single, valid JSON object. Do NOT include any text, explanation, or markdown formatting before or after the JSON object.
3.  The JSON object must strictly adhere to the following structure:
    {
      "diagnosis": "...",
      "confidence": "High" | "Medium" | "Low",
      "treatment": ["...", "..."],
      "prevention": ["...", "..."],
      "local_remedies": ["...", "..."],
      "escalate": true | false,
      "escalate_reason": "..." | null,
      "summary": "..."
    }
4.  Provide practical, actionable advice suitable for a farmer.
5.  If the disease is serious, confidence is low, or you cannot make a clear diagnosis, set "escalate" to true and provide a clear "escalate_reason".
6.  The 'summary' should be a concise, one-sentence overview of the situation.
7.  The user will specify a language. All text in the JSON values (diagnosis, treatment, etc.) should be in that language.
"""

# --- API Endpoints ---
@app.get("/health", response_model=HealthCheck, tags=["Status"])
async def health_check():
    """
    Performs a health check and returns the configured AI model name.
    """
    return {"model_name": OLLAMA_MODEL}

@app.post("/analyze", response_model=AnalysisResponse, tags=["Analysis"])
async def analyze_crop(
    image: UploadFile = File(...),
    question: str = Form(...),
    language: str = Form("English")
):
    """
    Analyzes a crop image to diagnose diseases or pests.
    """
    try:
        image_bytes = await image.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        full_prompt = f"Language for response: {language}. Question: {question}"

        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": full_prompt,
                    "images": [image_base64],
                },
            ],
        )

        # Clean the response to ensure it's valid JSON
        raw_response_content = response['message']['content']
        # Find the start and end of the JSON object
        json_start = raw_response_content.find('{')
        json_end = raw_response_content.rfind('}') + 1
        
        if json_start == -1 or json_end == 0:
            raise HTTPException(status_code=500, detail="AI model returned invalid format.")

        json_string = raw_response_content[json_start:json_end]
        
        # Parse the JSON string into the Pydantic model
        parsed_json = json.loads(json_string)
        return AnalysisResponse(**parsed_json)

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to decode AI response as JSON.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# --- Uvicorn Runner ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
