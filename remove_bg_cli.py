from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from rembg import new_session, remove
from PIL import Image
import io
import uvicorn
import os
import gc
from run_server import start_keep_alive

# Initialize FastAPI without Swagger UI
app = FastAPI(docs_url=None, redoc_url=None)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Preload rembg session (lightweight u2netp model)
session = new_session("u2netp")

# Max dimension to reduce memory usage
MAX_DIMENSION = 512

@app.get("/")
@app.head("/")
def health(request: Request = None):
    return {"status": "ok"}

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    # Read uploaded file bytes and close temp file
    input_bytes = await file.read()
    await file.close()

    # Open image and convert to RGB (less memory usage than RGBA)
    image = Image.open(io.BytesIO(input_bytes)).convert("RGB")

    # Resize large images to MAX_DIMENSION
    if max(image.size) > MAX_DIMENSION:
        image.thumbnail((MAX_DIMENSION, MAX_DIMENSION))

    # Convert resized image to bytes in memory
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    buf.seek(0)
    resized_bytes = buf.read()

    # Remove background using preloaded session
    output_bytes = remove(resized_bytes, session=session)

    # Ensure valid PNG output
    result_image = Image.open(io.BytesIO(output_bytes)).convert("RGB")
    out_buf = io.BytesIO()
    result_image.save(out_buf, format="PNG")
    out_buf.seek(0)

    # Clear memory to avoid crashes on subsequent requests
    del image, buf, resized_bytes, result_image, output_bytes
    gc.collect()

    return StreamingResponse(out_buf, media_type="image/png")


if __name__ == "__main__":
    # 🔁 Start background ping thread to keep Render alive and auto-restart if needed
    start_keep_alive()
    
    # Use environment PORT if available (for Render, Railway, etc.)
    PORT = int(os.environ.get("PORT", 8000))
    
    # 🚀 Run uvicorn with single worker to prevent memory spikes
    uvicorn.run("remove_bg_cli:app", host="0.0.0.0", port=PORT, reload=False)
