import asyncio
import sys
import io
import json
from contextlib import redirect_stdout
from typing import Optional
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from database import Database
from pipeline import Pipeline
from config import Config
import os

app = FastAPI(title="LeadForge API")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global queue for logs
log_queue = asyncio.Queue()

class OutputCapture(io.TextIOBase):
    """Captures stdout and puts it into the async queue."""
    def __init__(self, queue):
        self.queue = queue
        self.buffer = ""

    def write(self, s):
        if s:
            # Send to terminal too for debugging
            sys.__stdout__.write(s)
            # Put in queue for web UI
            asyncio.create_task(self.queue.put(s))
        return len(s)

    def flush(self):
        sys.__stdout__.flush()

@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    return FileResponse("dashboard.html")

@app.get("/stream")
async def stream_logs():
    """Stream logs to the frontend via Server-Sent Events."""
    async def event_generator():
        while True:
            log_line = await log_queue.get()
            if log_line:
                # Format for SSE
                yield f"data: {json.dumps({'message': log_line.strip()})}\n\n"
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.post("/run/maps")
async def run_maps(query: str = Form(...), location: str = Form(...), limit: int = Form(10)):
    # Create search record first
    db = Database()
    search_id = db.create_search(query, location, "google_maps")
    db.close()

    async def run_in_background():
        capture = OutputCapture(log_queue)
        with redirect_stdout(capture):
            try:
                pipeline = Pipeline()
                pipeline.run(query, location, limit, search_id=search_id)
                pipeline.close()
            except Exception as e:
                await log_queue.put(f"❌ Error: {str(e)}")
    
    asyncio.create_task(run_in_background())
    return {"status": "started", "engine": "google_maps", "search_id": search_id}

@app.post("/run/linkedin")
async def run_linkedin(role: str = Form(...), industry: str = Form(...), location: str = Form(""), limit: int = Form(10)):
    # Create search record first
    db = Database()
    search_id = db.create_search(f"{role} in {industry}", location, "linkedin")
    db.close()

    async def run_in_background():
        capture = OutputCapture(log_queue)
        with redirect_stdout(capture):
            try:
                pipeline = Pipeline()
                pipeline.run_expert_search("linkedin", role, industry, location, limit, search_id=search_id)
                pipeline.close()
            except Exception as e:
                await log_queue.put(f"❌ Error: {str(e)}")
    
    asyncio.create_task(run_in_background())
    return {"status": "started", "engine": "linkedin", "search_id": search_id}

@app.post("/run/clutch")
async def run_clutch(category: str = Form(...), location: str = Form(""), limit: int = Form(10)):
    # Create search record first
    db = Database()
    search_id = db.create_search(category, location, "clutch")
    db.close()

    async def run_in_background():
        capture = OutputCapture(log_queue)
        with redirect_stdout(capture):
            try:
                pipeline = Pipeline()
                pipeline.run_expert_search("clutch", category, location=location, limit=limit, search_id=search_id)
                pipeline.close()
            except Exception as e:
                await log_queue.put(f"❌ Error: {str(e)}")
    
    asyncio.create_task(run_in_background())
    return {"status": "started", "engine": "clutch", "search_id": search_id}

@app.get("/history")
async def get_history(limit: int = 10):
    """Get search history."""
    db = Database()
    history = db.get_recent_searches(limit)
    db.close()
    return history

@app.get("/results/{search_id}")
async def get_results(search_id: int):
    """Get leads for a specific search ID."""
    db = Database()
    leads = db.get_leads_by_search(search_id)
    db.close()
    return leads

@app.get("/results/latest")
async def get_latest_results():
    """Get leads from the most recent search."""
    db = Database()
    history = db.get_recent_searches(1)
    if not history:
        db.close()
        return []
    leads = db.get_leads_by_search(history[0]['id'])
    db.close()
    return leads

if __name__ == "__main__":
    import uvicorn
    Config.validate()
    print("🚀 ProspectVantage Server starting at http://localhost:8001")
    uvicorn.run(app, host="0.0.0.0", port=8001)
