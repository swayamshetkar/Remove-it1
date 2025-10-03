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
    allow_origins=[""],  # In production, replace "" with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use smallest model for low memory (u2netp-lite < u2netp < u2net)
session = new_session("u2netp-lite")

# Max dimension to avoid OOM (keep small on 512MB Railway)
MAX_DIMENSION = 512


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    # Read file
    input_bytes = await file.read()

    # Open and ensure RGBA
    image = Image.open(io.BytesIO(input_bytes)).convert("RGBA")

    # Resize aggressively to save RAM
    if max(image.size) > MAX_DIMENSION:
        image.thumbnail((MAX_DIMENSION, MAX_DIMENSION), Image.LANCZOS)

    # Run background removal directly on PIL (no extra buffer copies)
    output_bytes = remove(image, session=session)

    # Ensure valid PNG output
    result_image = Image.open(io.BytesIO(output_bytes)).convert("RGBA")
    out_buf = io.BytesIO()
    result_image.save(out_buf, format="PNG", optimize=True)  # optimize PNG size
    out_buf.seek(0)

    return StreamingResponse(out_buf, media_type="image/png")


if _name_ == "_main_":
    PORT = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=PORT)
