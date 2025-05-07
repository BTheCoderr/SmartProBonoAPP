from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, EmailStr
from typing import Optional
import logging
from datetime import datetime
import secrets
from sqlalchemy.orm import Session
from services.email_service import send_confirmation_email
from services.analytics_service import track_event
from database import get_db
from models.beta_signup import BetaSignup

router = APIRouter(prefix="/api/beta", tags=["beta"])

class BetaSignupRequest(BaseModel):
    email: EmailStr
    source: Optional[str] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None

@router.post("/signup")
async def beta_signup(
    signup: BetaSignupRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """Handle beta signup requests with email confirmation."""
    try:
        # Generate confirmation token
        confirmation_token = secrets.token_urlsafe(32)
        
        # Create new signup record
        db_signup = BetaSignup(
            email=signup.email,
            source=signup.source,
            utm_source=signup.utm_source,
            utm_medium=signup.utm_medium,
            utm_campaign=signup.utm_campaign,
            confirmation_token=confirmation_token
        )
        
        db.add(db_signup)
        db.commit()
        db.refresh(db_signup)
        
        # Send confirmation email
        await send_confirmation_email(
            to_email=signup.email,
            confirmation_token=confirmation_token
        )
        
        # Track signup event
        await track_event(
            event_name="beta_signup",
            properties={
                "email": signup.email,
                "source": signup.source,
                "utm_source": signup.utm_source,
                "utm_medium": signup.utm_medium,
                "utm_campaign": signup.utm_campaign,
                "ip_address": request.client.host
            }
        )
        
        return {
            "status": "success",
            "message": "Please check your email to confirm your signup."
        }
        
    except Exception as e:
        logging.error(f"Beta signup error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to process beta signup")

@router.get("/confirm/{token}")
async def confirm_signup(token: str, db: Session = Depends(get_db)):
    """Confirm beta signup email."""
    try:
        signup = db.query(BetaSignup).filter(
            BetaSignup.confirmation_token == token,
            BetaSignup.is_confirmed == False
        ).first()
        
        if not signup:
            raise HTTPException(status_code=404, detail="Invalid or expired confirmation token")
        
        # Update signup record
        signup.is_confirmed = True
        signup.confirmed_at = datetime.now()
        signup.confirmation_token = None  # Invalidate token
        
        db.commit()
        
        # Track confirmation event
        await track_event(
            event_name="beta_signup_confirmed",
            properties={"email": signup.email}
        )
        
        return {
            "status": "success",
            "message": "Thank you for confirming your email! We'll notify you when the beta is ready."
        }
        
    except Exception as e:
        logging.error(f"Beta confirmation error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to confirm signup") 