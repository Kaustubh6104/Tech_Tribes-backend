from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import models
# 👇 CHANGE 1: Import 'Base' here alongside 'engine'
from database import engine, Base 
from routers import listings, auth, ai_planner, chat

# 👇 CHANGE 2: Use 'Base' directly (remove 'models.')
# This creates the tables in guide.db
Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"] # In a real app, restrict this. For hackathon, "*" (allow all) is fine.

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(listings.router)
app.include_router(auth.router)
app.include_router(ai_planner.router)
app.include_router(chat.router)

@app.get("/")
def home():
    return {"message": "Guide-Us Backend is Live and Database is Created! 🚀"}