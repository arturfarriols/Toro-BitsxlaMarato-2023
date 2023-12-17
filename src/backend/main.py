"""Entrypoint to consume data and produce the results"""
from fastapi import FastAPI, UploadFile, File,Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
from core import connector
import os
import io
import zipfile
import json
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


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file:
        return JSONResponse(status_code=400, content={"message": "No file provided"})

    file_content = await file.read()

    if not file_content:
        return JSONResponse(
            status_code=400, content={"message": "File provided is empty"}
        )

    # You can process the file_content here, for example, save it to disk or perform further operations.
    # For demonstration purposes, this example returns a message with the file details.
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "file_size": len(file_content),
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
