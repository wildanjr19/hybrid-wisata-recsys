"""
Main FastAPI application for Tourism Recommendation System
Entry point untuk backend API
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
from app.routes import recommendation

# Inisialisasi FastAPI app
app = FastAPI(
    title="Tourism Recommendation API",
    description="API untuk sistem rekomendasi wisata menggunakan LightFM",
    version="1.0.0"
)

# CORS middleware untuk allow frontend akses API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Dalam production, ganti dengan domain spesifik
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files dari frontend
frontend_dir = Path(__file__).parent.parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=str(frontend_dir / "static")), name="static")

# Include router dari routes
app.include_router(recommendation.router, prefix="/api", tags=["Recommendation"])

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve frontend HTML page"""
    html_file = frontend_dir / "templates" / "index.html"
    with open(html_file, "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    # Jalankan server di localhost:8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
