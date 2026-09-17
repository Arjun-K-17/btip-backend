from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# =====================================================
# Database
# =====================================================

from database.connection import engine, Base
from database import models


# =====================================================
# API Routers
# =====================================================

from api.auth import router as auth_router
from api.datasets import router as datasets_router
from api.analytics import router as analytics_router
from api.crisis import router as crisis_router
from api.forecast import router as forecast_router
from api.simulation import router as simulation_router
from api.recommendations import router as recommendations_router
from api.alerts import router as alerts_router
from api.reports import router as reports_router
from api.dashboard import router as dashboard_router
from api.chatbot import router as chatbot_router


# =====================================================
# FastAPI Application
# =====================================================

app = FastAPI(
    title="BTIP - Business Turnaround Intelligence Platform",

    description=(
        "Backend API for financial and "
        "business turnaround analysis."
    ),

    version="1.0.0"
)


# =====================================================
# CORS Configuration
# =====================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",

        # AI chatbot development frontend
        "http://localhost:5174",
        "http://127.0.0.1:5174"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =====================================================
# Database Table Creation
# =====================================================

Base.metadata.create_all(
    bind=engine
)


# =====================================================
# API Router Registration
# =====================================================

app.include_router(
    auth_router
)

app.include_router(
    datasets_router
)

app.include_router(
    analytics_router
)

app.include_router(
    crisis_router
)

app.include_router(
    forecast_router
)

app.include_router(
    simulation_router
)

app.include_router(
    recommendations_router
)

app.include_router(
    alerts_router
)

app.include_router(
    reports_router
)

app.include_router(
    dashboard_router
)

app.include_router(
    chatbot_router
)


# =====================================================
# Root Endpoint
# =====================================================

@app.get("/")
def root():
    return {
        "message": (
            "BTIP Backend is running"
        ),
        "status": "success"
    }


# =====================================================
# Health Check
# =====================================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }