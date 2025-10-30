
import os, jwt
from fastapi import Header, HTTPException
from .models import SessionLocal

SECRET = os.environ.get("PULSE_SECRET", "dev-secret")

def create_demo_admin_token():
    return jwt.encode({"role": "admin"}, SECRET, algorithm="HS256")

def get_current_admin(authorization: str = Header(None)):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(401, "Missing token")
    token = authorization.split()[1]
    try:
        data = jwt.decode(token, SECRET, algorithms=["HS256"])
    except Exception:
        raise HTTPException(401, "Invalid token")
    if data.get("role") != "admin":
        raise HTTPException(403, "Admin role required")
    return True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
