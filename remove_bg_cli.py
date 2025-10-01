from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from rembg import new_session, remove
from PIL import Image
import io

app = FastAPI(docs_url=None, redoc_url=None)

# Create session once at startup
session = new_session("u2netp")

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    input_bytes = await file.read()
    output_bytes = remove(input_bytes, session=session)
    image = Image.open(io.BytesIO(output_bytes)).convert("RGBA")
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")
