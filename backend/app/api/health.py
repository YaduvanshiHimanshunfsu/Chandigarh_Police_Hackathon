"""
Health check endpoint — for Docker healthcheck and judges' quick verification.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """Basic health check — returns platform info."""
    return {
        "status": "healthy",
        "platform": "PratiBimb Praman",
        "version": "1.0.0",
        "description": "AI Media Forensic Provenance & Origin Intelligence Platform",
        "hackathon": "Chandigarh Police National Hackathon 2026",
    }
