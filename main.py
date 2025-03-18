from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import asyncio
from datetime import datetime
import logging
from fastapi.background import BackgroundTasks
import hashlib
import hmac
import json
from config import get_settings, Settings
from routers import links  # Add this import

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

# Get your bot token from environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN', '')

def validate_telegram_webapp_data(init_data: str) -> bool:
    try:
        # Parse the init_data string
        data_dict = dict(param.split('=') for param in init_data.split('&'))
        
        if 'hash' not in data_dict:
            return False

        # Get the hash from the data
        received_hash = data_dict.pop('hash')
        
        # Sort the data alphabetically
        data_check_string = '\n'.join(f'{k}={v}' for k, v in sorted(data_dict.items()))
        
        # Create a secret key by using HMAC-SHA256 with bot token
        secret_key = hmac.new(
            key=b'WebAppData',
            msg=BOT_TOKEN.encode(),
            digestmod=hashlib.sha256
        ).digest()
        
        # Calculate the hash
        calculated_hash = hmac.new(
            key=secret_key,
            msg=data_check_string.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()
        
        return calculated_hash == received_hash
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        return False

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
async def read_index(request: Request):
    # Get the Telegram Web App init data from query parameters
    init_data = request.query_params.get('tgWebAppData')
    
    if init_data and not validate_telegram_webapp_data(init_data):
        raise HTTPException(status_code=403, detail="Invalid Telegram Web App data")
    
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

@app.get("/info")
async def info(settings: Settings = Depends(get_settings)):
    return {
        "env": settings.ENV,
        "debug": settings.DEBUG,
        "links_history_path": str(settings.LINKS_HISTORY_PATH)
    }

# Add the links router
app.include_router(links.router, prefix="/api")