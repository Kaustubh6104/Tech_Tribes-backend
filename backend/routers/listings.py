from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
import shutil  
import uuid     
import os

# 👇 THIS LINE IS MISSING OR NAMED WRONG
router = APIRouter(tags=["Listings"])

# 1. GET LISTINGS (Filtered by City)
@router.get("/listings/{city}", response_model=list[schemas.Listing])
def get_listings(city: str, db: Session = Depends(get_db)):
    listings = db.query(models.Listing).filter(models.Listing.city == city).all()
    # Sort premium first
    listings.sort(key=lambda x: x.is_premium, reverse=True)
    return listings

# 2. CREATE LISTING
@router.post("/listings/", response_model=schemas.Listing)
def create_listing(listing: schemas.ListingCreate, owner_id: int, db: Session = Depends(get_db)):
    db_listing = models.Listing(**listing.dict(), owner_id=owner_id)
    db.add(db_listing)
    db.commit()
    db.refresh(db_listing)
    return db_listing

#3. UPLOAD IMAGE ENDPOINT
@router.post("/upload-image")
def upload_image(file: UploadFile = File(...)):
    # A. Generate a unique name so files don't overwrite each other
    # e.g., "hotel.jpg" -> "a1b2c3d4-hotel.jpg"
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = f"static/{unique_filename}"
    
    # B. Save the file to your 'static' folder
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # C. Return the URL that the frontend should save in the database
    # Example: http://localhost:8000/static/a1b2c3d4.jpg
    return {"url": f"http://127.0.0.1:8000/static/{unique_filename}"}