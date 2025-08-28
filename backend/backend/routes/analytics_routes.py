from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from datetime import datetime
from services.analytics_service import analytics_service
from models.analytics import (
    FormView,
    FormStart,
    FormCompletion,
    FormAbandonment,
    FieldInteraction,
    FieldTiming,
    FormError,
    FormAnalytics,
    AbandonmentAnalysis,
    FormSuccessRate
)
from services.auth import get_current_user
from models.user import User

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.post("/form-view")
async def track_form_view(
    form_view: FormView,
    current_user: User = Depends(get_current_user)
):
    """Track a form view event."""
    try:
        await analytics_service.track_form_view(form_view)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/form-start")
async def track_form_start(
    form_start: FormStart,
    current_user: User = Depends(get_current_user)
):
    """Track a form start event."""
    try:
        await analytics_service.track_form_start(form_start)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/form-completion")
async def track_form_completion(
    form_completion: FormCompletion,
    current_user: User = Depends(get_current_user)
):
    """Track a form completion event."""
    try:
        await analytics_service.track_form_completion(form_completion)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/form-abandonment")
async def track_form_abandonment(
    abandonment: FormAbandonment,
    current_user: User = Depends(get_current_user)
):
    """Track a form abandonment event."""
    try:
        await analytics_service.track_form_abandonment(abandonment)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/field-interaction")
async def track_field_interaction(
    interaction: FieldInteraction,
    current_user: User = Depends(get_current_user)
):
    """Track a field interaction event."""
    try:
        await analytics_service.track_field_interaction(interaction)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/field-timing")
async def track_field_timing(
    timing: FieldTiming,
    current_user: User = Depends(get_current_user)
):
    """Track field timing data."""
    try:
        await analytics_service.track_field_timing(timing)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/form-error")
async def track_form_error(
    error: FormError,
    current_user: User = Depends(get_current_user)
):
    """Track a form error event."""
    try:
        await analytics_service.track_form_error(error)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/forms/{form_type}")
async def get_form_analytics(
    form_type: str,
    date_range: str = Query("7d", regex="^[0-9]+[d]$"),
    current_user: User = Depends(get_current_user)
) -> FormAnalytics:
    """Get comprehensive analytics for a specific form type."""
    try:
        return await analytics_service.get_form_analytics(form_type, date_range)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/forms/{form_type}/fields/{field_name}")
async def get_field_analytics(
    form_type: str,
    field_name: str,
    current_user: User = Depends(get_current_user)
):
    """Get analytics for a specific form field."""
    try:
        return await analytics_service.get_field_analytics(form_type, field_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/forms/{form_type}/abandonment")
async def get_abandonment_analysis(
    form_type: str,
    current_user: User = Depends(get_current_user)
) -> AbandonmentAnalysis:
    """Get detailed analysis of form abandonments."""
    try:
        return await analytics_service.get_abandonment_analysis(form_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/forms/{form_type}/success-rate")
async def get_form_success_rate(
    form_type: str,
    date_range: str = Query("30d", regex="^[0-9]+[d]$"),
    current_user: User = Depends(get_current_user)
) -> FormSuccessRate:
    """Get form success rate metrics."""
    try:
        return await analytics_service.get_form_success_rate(form_type, date_range)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dashboard/stats")
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user)
):
    """Get overall dashboard statistics."""
    try:
        return await analytics_service.get_dashboard_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user-metrics")
async def get_user_metrics(
    days: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_user)
):
    """Get user-related metrics."""
    try:
        return await analytics_service.get_user_metrics(days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/error-analytics")
async def get_error_analytics(
    current_user: User = Depends(get_current_user)
):
    """Get error analytics data."""
    try:
        return await analytics_service.get_error_analytics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/performance-metrics")
async def get_performance_metrics(
    current_user: User = Depends(get_current_user)
):
    """Get performance metrics data."""
    try:
        return await analytics_service.get_performance_metrics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 