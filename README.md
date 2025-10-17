#  Background Removal Backend (U²-Net Powered)

A fully functional **backend service** for **image background removal**, powered by the **U²-Net deep learning model**.  
The API accepts image uploads and returns the same image with the background cleanly removed — ideal for use in web apps, design tools, or e-commerce pipelines.

---

## ⚙️ Tech Stack
-  **U²-Net** – Deep learning model for salient object detection  
-  **FastAPI** – Lightweight and high-performance Python web framework  
-  **Docker** – Containerized for easy deployment  
-  **Render** – Cloud hosting for backend services  
-  **Python Libraries:** `torch`, `numpy`, `opencv-python`, `pillow`, `requests`, `uvicorn`, `fastapi`

---

##  About U²-Net
[U²-Net (U-square Net)](https://github.com/xuebinqin/U-2-Net) is a deep neural network for **salient object detection (SOD)**.  
It’s designed to efficiently capture both fine details and global context, making it one of the most accurate models for background removal and segmentation tasks.

---

##  Features
- Removes image background in seconds  
- Works with PNG, JPG, and JPEG images  
- Returns **transparent PNG** output  
- Lightweight and production-ready  
- Dockerized for seamless deployment on Render or any other cloud platform  

---

##  API Endpoints

### `POST /remove-bg`
Removes the background from an uploaded image.

#### **Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body:
  - `file`: Image file to process

Example using `curl`:
```bash
curl -X POST "https://<your-render-app>.onrender.com/remove-bg" \
     -F "file=@example.jpg" \
     -o output.png
