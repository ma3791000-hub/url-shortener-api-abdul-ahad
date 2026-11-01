
from fastapi import FastAPI

from app.routers import links
from app.routers import redirect
from app.routers import analytics

app = FastAPI(
    title="URL Shortener API",
    description="A local URL shortening service",
    version="1.0.0",
)
app.include_router(links.router)
app.include_router(analytics.router)


@app.get("/")
def home():
    return {
        "message": "URL Shortener API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
app.include_router(redirect.router)
