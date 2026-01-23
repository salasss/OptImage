import time
import asyncio
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from app.services.image_processor import process_image
from fastapi.responses import StreamingResponse
from prometheus_fastapi_instrumentator import Instrumentator
#INIT
app = FastAPI(
    title="Image Optimizer API",
    description="Microservice d'optimisation d'images",
    version="0.0.1"
)
Instrumentator().instrument(app).expose(app)
#base route
@app.get("/")
async def root():
    return{
        "message":"Image Optimizer API is running",
        "docs": "/docs"
    }

#archive(simulation)
def archive_task_image(filename:str,original_size:int):
    time.sleep(2)
    print(f"[[BG]]image{filename} archived. original size {original_size}")

@app.post("/optimize")
async def optimize_image_endpoint(bg_tasks: BackgroundTasks,file : UploadFile = File(...),width: int = None,height: int = None,format:str = "WEBP",quality:int = 80):
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="the file should be an image")
        
    content = await file.read()
    
    bg_tasks.add_task(archive_task_image,file.filename,len(content))
    #traitement cpu bound
    try:
        opti_buffer = await asyncio.to_thread(
            process_image,
            content,
            width=width,
            height=height,
            format=format,
            quality=quality
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e))
    media_type = f"image/{format.lower()}"
    if format.lower() == "jpg": media_type = "image/jpeg"

    return StreamingResponse(
        opti_buffer, 
        media_type=media_type
    )
    
    

    
@app.get("/health")
async def health_check():
    return{
        "status":"healthy"
    }