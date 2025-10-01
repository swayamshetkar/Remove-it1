# main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from rembg import new_session, remove
from PIL import Image
import io
import uvicorn
import os

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

# Max dimension to reduce memory usage
MAX_DIMENSION = 1024  # pixels

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    # Read uploaded file bytes
    input_bytes = await file.read()

    # Open image and resize if too large
    image = Image.open(io.BytesIO(input_bytes))
    if max(image.size) > MAX_DIMENSION:
        image.thumbnail((MAX_DIMENSION, MAX_DIMENSION))
    
    # Convert resized image back to bytes
    buf = io.BytesIO()
    image.save(buf, format=image.format or "PNG")
    resized_bytes = buf.getvalue()

    # Remove background using rembg session
    output_bytes = remove(resized_bytes, session=session)

    # Return bytes directly as PNG
    return StreamingResponse(io.BytesIO(output_bytes), media_type="image/png")

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=PORT)
