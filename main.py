from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import asyncio

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