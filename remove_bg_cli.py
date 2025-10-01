# main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from rembg import new_session, remove
from PIL import Image
import io

# Initialize FastAPI without Swagger UI
app = FastAPI(docs_url=None, redoc_url=None)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create rembg session once at startup
session = new_session("u2netp")

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    # Read uploaded file bytes
    input_bytes = await file.read()

    # Remove background using rembg session
    output_bytes = remove(input_bytes, session=session)

    # Convert to PIL.Image and save as PNG
    image = Image.open(io.BytesIO(output_bytes)).convert("RGBA")
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    buf.seek(0)

    # Return StreamingResponse so browser/download can handle PNG
    return StreamingResponse(buf, media_type="image/png")
