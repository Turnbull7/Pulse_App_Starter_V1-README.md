
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from .models import Base, engine, User, Event, Sponsor, TrendSignal, Consent
from .schemas import UserCreate, EventIn, SponsorCreate, TrendQuery
from .security import get_current_admin, get_db, create_demo_admin_token
from sqlalchemy.orm import Session
from datetime import datetime, timezone

app = FastAPI(title="Pulse API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.now(timezone.utc).isoformat()}

@app.post("/auth/demo-admin-token")
def demo_admin_token():
    return {"token": create_demo_admin_token()}

@app.post("/users", response_model=dict)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    user = User(email=payload.email, age=payload.age, gender=payload.gender, region=payload.region)
    db.add(user); db.commit(); db.refresh(user)
    consent = Consent(user_id=user.id, marketing=False, analytics=False)
    db.add(consent); db.commit()
    return {"id": user.id, "email": user.email}

@app.post("/consent/{user_id}")
def set_consent(user_id: int, consent: dict, db: Session = Depends(get_db)):
    c = db.query(Consent).filter(Consent.user_id == user_id).first()
    if not c:
        raise HTTPException(404, "Consent record not found")
    c.marketing = bool(consent.get("marketing", False))
    c.analytics = bool(consent.get("analytics", False))
    db.commit()
    return {"ok": True, "user_id": user_id, "consent": {"marketing": c.marketing, "analytics": c.analytics}}

@app.post("/events")
def ingest_event(evt: EventIn, request: Request, db: Session = Depends(get_db)):
    consent = db.query(Consent).filter(Consent.user_id == evt.user_id).first()
    if not consent or not consent.analytics:
        raise HTTPException(403, "Analytics consent required")
    e = Event(user_id=evt.user_id, type=evt.type, properties=evt.properties, created_at=datetime.now(timezone.utc))
    db.add(e); db.commit()
    return {"ok": True}

@app.delete("/privacy/delete/{user_id}")
def privacy_delete(user_id: int, db: Session = Depends(get_db)):
    db.query(Event).filter(Event.user_id == user_id).delete()
    db.query(Consent).filter(Consent.user_id == user_id).delete()
    db.query(User).filter(User.id == user_id).delete()
    db.commit()
    return {"ok": True}

@app.post("/sponsors", dependencies=[Depends(get_current_admin)])
def create_sponsor(payload: SponsorCreate, db: Session = Depends(get_db)):
    s = Sponsor(name=payload.name, industry=payload.industry)
    db.add(s); db.commit(); db.refresh(s)
    return {"id": s.id, "name": s.name}

@app.post("/sponsor/insights")
def sponsor_insights(q: TrendQuery, db: Session = Depends(get_db)):
    signals = db.query(TrendSignal).filter(
        TrendSignal.segment == q.segment, TrendSignal.metric == q.metric
    ).order_by(TrendSignal.generated_at.desc()).limit(24).all()

    series = []
    for s in signals:
        if s.sample_size >= 50:
            series.append({"t": s.generated_at.isoformat(), "value": s.value, "n": s.sample_size})

    return {"segment": q.segment, "metric": q.metric, "series": series}

@app.get("/.well-known/pulse-sdk")
def sdk_descriptor():
    return {
        "name": "PulseSDK",
        "version": "0.1.0",
        "events": ["app_open", "session_start", "quiz_answer", "share", "purchase", "sponsor_cta_click"],
        "endpoint": "/events",
        "privacy": {"consent_required": True, "delete_endpoint": "/privacy/delete/{user_id}"}
    }
