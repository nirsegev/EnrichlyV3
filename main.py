from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import asyncio
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open(os.path.join("static", "index.html")) as f: 
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/api/task/{box_number}")
async def run_background_task(box_number: int):
    # Simulate a 10-second task
    await asyncio.sleep(10)
    return JSONResponse(content={
        "message": f"Operation completed for Hello World #{box_number}!"
    })

@app.get("/health")
async def health_check():
    try:
        # Log the health check
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Health check successful at {current_time}")
        
        return JSONResponse(content={
            "status": "healthy",
            "timestamp": current_time
        })
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "unhealthy",
                "error": str(e)
            }
        )