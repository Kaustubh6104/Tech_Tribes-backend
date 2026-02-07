from pydantic import BaseModel
from typing import Optional, List

# ==========================
# 🏠 LISTING SCHEMAS
# ==========================

# Common properties for Listings (Hotels/Cafes)
class ListingBase(BaseModel):
    title: str
    category: str  # e.g., 'hotel', 'cafe'
    city: str
    description: Optional[str] = None
    price_range: Optional[str] = None
    image_url: Optional[str] = None

# What we need to CREATE a listing
class ListingCreate(ListingBase):
    pass

# What we return to the frontend (includes ID and Owner ID)
class Listing(ListingBase):
    id: int
    owner_id: int
    is_premium: bool

    class Config:
        from_attributes = True  # Allows Pydantic to read SQLAlchemy models

# ==========================
# 👤 USER SCHEMAS
# ==========================

# What we need to REGISTER a user
class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str
    role: str = "traveler"  # Default to 'traveler'

# What we return to the frontend (NEVER return the password!)
class User(BaseModel):
    id: int
    full_name: str
    email: str
    role: str
    listings: List[Listing] = []  # Show their listings if they are an owner

    class Config:
        from_attributes = True

# ==========================
# 🔐 TOKEN SCHEMAS
# ==========================

# What the Login Endpoint returns
class Token(BaseModel):
    access_token: str
    token_type: str

# Data inside the token
class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None