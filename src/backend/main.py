"""Entrypoint to consume data and produce the results"""
from fastapi import FastAPI, UploadFile, File,Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
from core import Connector
import os
import io
import zipfile
import json
import os
from pydantic import BaseModel

class PathRequest(BaseModel):
    path: str
    
    
app = FastAPI()
# Allow CORS for all origins, methods, and headers (not recommended for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get("/healthz")
async def ok():
    return {"status": "OK"}


@app.get("/api/files")
async def get_files():
    current_directory = os.getcwd()
    absolute_path = os.path.join(current_directory, "data/data-hackaton")
    
    file_list = []
    for root, dirs, files in os.walk(absolute_path):
        for file in files:
            file_list.append(os.path.relpath(os.path.join(root, file), start=absolute_path))

    try:
       
        return JSONResponse(content={"files": file_list})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/api/analyze")
async def upload_file(path_request: PathRequest):
    contractions, mean, is_FCFB_determined, img_mean, variability, amount_accelerations, amount_decelerations = Connector.analyize(path_request.path)
    
    # You can process the file_content here, for example, save it to disk or perform further operations.
    # For demonstration purposes, this example returns a message with the file details.
    return {
        "contractions": contractions,
        "mean": mean,
        "is_FCFB_determined": bool(is_FCFB_determined),
        "variability": variability,
        "amount_accelerations": amount_accelerations,
        "amount_decelerations": amount_decelerations,
        "img_url": img_mean
    }


"""@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # ... (your file handling logic)
    if not file:
        return JSONResponse(status_code=400, content={"message": "No file provided"})

   
    # Prepare the response ZIP file with some files inside
    file_content_1 = b"Content of file 1"
    file_content_2 = b"Content of file 2"
    
    zip_data = io.BytesIO()
    with zipfile.ZipFile(zip_data, mode="w") as zipf:
        zipf.writestr("file1.txt", file_content_1)
        zipf.writestr("file2.txt", file_content_2)


    # Return the response with the ZIP file and custom metadata in headers
    response = Response(content=zip_data.getvalue(), media_type="application/zip")
    response.headers["Content-Disposition"] = "attachment; filename=files.zip"
    return response
"""

if __name__ == "__main__":
    import uvicorn

    load_dotenv(dotenv_path=".env.local")
    PORT = int(os.getenv("PORT", 8181))
    # DEBUG = os.getenv("DEBUG")

    uvicorn.run(app, host="0.0.0.0", port=PORT)
