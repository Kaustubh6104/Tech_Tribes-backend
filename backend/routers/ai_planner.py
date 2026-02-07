from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import google.generativeai as genai
import json

router = APIRouter(tags=["AI Planner"])

# 🔑 PASTE YOUR KEY HERE
GENAI_API_KEY = "AIzaSyAp46bFdyqMBcXA25ORBKs6Vz1fHFtdSpc"
genai.configure(api_key=GENAI_API_KEY)

class TripRequest(BaseModel):
    destination: str
    duration_days: int
    traveler_type: str # 'Solo', 'Group', 'Couple'
    season: str        # 'Summer', 'Winter', 'Monsoon'

class TripResponse(BaseModel):
    essentials: List[str]
    medical_kit: List[str]
    itinerary: List[dict]

@router.post("/generate-trip", response_model=TripResponse)
def generate_trip_plan(request: TripRequest):
    try:
        # 1. The Prompt
        prompt = f"""
        Act as a professional travel agent. Plan a trip to {request.destination} for {request.duration_days} days.
        Traveler Type: {request.traveler_type}. Season: {request.season}.
        
        Return ONLY valid JSON with this exact structure:
        {{
            "essentials": ["item1", "item2", "item3"],
            "medical_kit": ["med1", "med2"],
            "itinerary": [
                {{"day": 1, "activity": "...", "recommendation": "..."}},
                {{"day": 2, "activity": "...", "recommendation": "..."}}
            ]
        }}
        Do not add any markdown formatting like ```json. Just raw JSON.
        """

        # 2. Call Gemini
        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content(prompt)
        
        # 3. Clean and Parse the JSON
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_text)

        return data

    except Exception as e:
        print(f"AI Error: {e}")
        # Fallback if AI fails (keeps your demo safe!)
        return {
            "essentials": ["Standard Clothes", "Wallet", "Phone"],
            "medical_kit": ["Paracetamol"],
            "itinerary": [{"day": 1, "activity": "Enjoy the city!", "recommendation": "Local food"}]
        }