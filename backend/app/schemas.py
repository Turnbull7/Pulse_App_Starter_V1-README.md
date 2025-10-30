
from pydantic import BaseModel, Field
from typing import Optional, Dict

class UserCreate(BaseModel):
    email: str
    age: Optional[int] = None
    gender: Optional[str] = None
    region: Optional[str] = None

class EventIn(BaseModel):
    user_id: int
    type: str = Field(examples=["app_open", "session_start", "quiz_answer", "share", "purchase", "sponsor_cta_click"])
    properties: Dict = {}

class SponsorCreate(BaseModel):
    name: str
    industry: str | None = None

class TrendQuery(BaseModel):
    segment: str
    metric: str
