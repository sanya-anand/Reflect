from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import Base, engine
from utils.logger import setup_logger
from middleware.error_handler import global_exception_handler, http_exception_handler

# Import all models so Base.metadata.create_all picks them up
from models import user, journal  # noqa: F401
from routes import auth_routes, journal_routes, analytics_routes, export_routes

# Setup logging
logger = setup_logger()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="REFLECT API",
    description="AI-powered emotion-aware journaling platform",
    version="3.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global error handlers
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

# Include routers
app.include_router(auth_routes.router)
app.include_router(journal_routes.router)
app.include_router(analytics_routes.router)
app.include_router(export_routes.router)


@app.get("/")
def home():
    """Health check endpoint."""
    return {"message": "REFLECT API v3.0 Running"}