from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import asyncio
from datetime import datetime
import logging
from fastapi.background import BackgroundTasks

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Global variable to store the background task
health_check_task = None

async def periodic_health_check():
    while True:
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Periodic health check successful at {current_time}")
            
            # Wait for 60 seconds before next check
            await asyncio.sleep(60)
            
        except Exception as e:
            logger.error(f"Periodic health check failed: {str(e)}")
            await asyncio.sleep(60)  # Still wait before retrying

@app.on_event("startup")
async def startup_event():
    # Start the periodic health check when the application starts
    global health_check_task
    health_check_task = asyncio.create_task(periodic_health_check())

@app.on_event("shutdown")
async def shutdown_event():
    # Cancel the periodic health check when the application shuts down
    if health_check_task:
        health_check_task.cancel()
        try:
            await health_check_task
        except asyncio.CancelledError:
            logger.info("Periodic health check task cancelled")

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
        logger.info(f"Health check endpoint called at {current_time}")
        
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