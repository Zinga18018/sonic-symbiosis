from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import json
import asyncio
import numpy as np
import librosa
from datetime import datetime, timedelta
import uuid
from typing import List, Dict, Optional
import random
import math

app = FastAPI(title="Sonic Symbiosis", description="AI-powered therapeutic soundscapes from plant bioacoustic data")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Data models
class BioacousticData(BaseModel):
    plant_id: str
    timestamp: datetime
    soil_moisture: float
    temperature: float
    humidity: float
    growth_rate: float
    stress_level: float

class TherapySession(BaseModel):
    user_mood: str
    therapy_goal: str
    duration_minutes: int
    selected_plants: List[str]

# Global storage for demo purposes
active_sessions: Dict[str, dict] = {}
connected_plants: List[dict] = [
    {
        "id": "plant_001",
        "name": "Monstera Deliciosa",
        "type": "Tropical",
        "health": 85,
        "last_reading": datetime.now().isoformat()
    },
    {
        "id": "plant_002",
        "name": "Snake Plant",
        "type": "Succulent",
        "health": 92,
        "last_reading": datetime.now().isoformat()
    },
    {
        "id": "plant_003",
        "name": "Peace Lily",
        "type": "Flowering",
        "health": 78,
        "last_reading": datetime.now().isoformat()
    }
]

class SonicSymbiosis:
    def __init__(self):
        self.sample_rate = 44100
        self.base_frequencies = {
            "Tropical": [220, 330, 440],  # A3, E4, A4
            "Succulent": [174, 285, 396],  # Lower, grounding frequencies
            "Flowering": [528, 639, 741]  # Higher, uplifting frequencies
        }
    
    def simulate_plant_data(self, plant_id: str) -> BioacousticData:
        """Simulate real-time plant sensor data"""
        base_time = datetime.now()
        
        # Simulate realistic plant data with some randomness
        return BioacousticData(
            plant_id=plant_id,
            timestamp=base_time,
            soil_moisture=random.uniform(0.3, 0.8),
            temperature=random.uniform(18, 26),
            humidity=random.uniform(40, 70),
            growth_rate=random.uniform(0.1, 0.5),
            stress_level=random.uniform(0.1, 0.4)
        )
    
    def generate_therapeutic_tone(self, plant_data: BioacousticData, plant_type: str, user_mood: str) -> np.ndarray:
        """Generate therapeutic audio based on plant data and user preferences"""
        duration = 2.0  # 2 seconds of audio
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        # Get base frequencies for plant type
        base_freqs = self.base_frequencies.get(plant_type, [440, 550, 660])
        
        # Modify frequencies based on plant health metrics
        freq_modifier = 1.0 + (plant_data.soil_moisture - 0.5) * 0.2
        frequencies = [f * freq_modifier for f in base_freqs]
        
        # Adjust amplitude based on stress level (lower stress = higher amplitude)
        amplitude = 0.3 * (1.0 - plant_data.stress_level)
        
        # Generate harmonic series
        audio = np.zeros_like(t)
        for i, freq in enumerate(frequencies):
            # Add harmonics with decreasing amplitude
            harmonic_weight = 1.0 / (i + 1)
            audio += harmonic_weight * amplitude * np.sin(2 * np.pi * freq * t)
        
        # Apply mood-based filtering
        if user_mood == "stressed":
            # Lower frequencies, slower modulation
            modulation = 0.1 * np.sin(2 * np.pi * 0.5 * t)
            audio *= (1.0 + modulation)
        elif user_mood == "energetic":
            # Higher frequencies, faster modulation
            modulation = 0.2 * np.sin(2 * np.pi * 2.0 * t)
            audio *= (1.0 + modulation)
        
        # Apply gentle fade in/out
        fade_samples = int(0.1 * self.sample_rate)
        audio[:fade_samples] *= np.linspace(0, 1, fade_samples)
        audio[-fade_samples:] *= np.linspace(1, 0, fade_samples)
        
        return audio
    
    def create_soundscape_data(self, session_id: str, plant_ids: List[str], user_mood: str) -> dict:
        """Create soundscape data for visualization"""
        soundscape_data = {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "plants": [],
            "combined_audio_features": {}
        }
        
        combined_audio = np.array([])
        
        for plant_id in plant_ids:
            # Find plant info
            plant_info = next((p for p in connected_plants if p["id"] == plant_id), None)
            if not plant_info:
                continue
            
            # Generate plant data and audio
            plant_data = self.simulate_plant_data(plant_id)
            audio = self.generate_therapeutic_tone(plant_data, plant_info["type"], user_mood)
            
            # Extract audio features for visualization
            spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=self.sample_rate)[0]
            mfccs = librosa.feature.mfcc(y=audio, sr=self.sample_rate, n_mfcc=13)
            
            plant_features = {
                "plant_id": plant_id,
                "name": plant_info["name"],
                "type": plant_info["type"],
                "health": plant_info["health"],
                "bioacoustic_data": plant_data.dict(),
                "audio_features": {
                    "spectral_centroid_mean": float(np.mean(spectral_centroid)),
                    "mfcc_mean": [float(x) for x in np.mean(mfccs, axis=1)],
                    "amplitude": float(np.max(np.abs(audio))),
                    "frequency_range": [float(np.min(spectral_centroid)), float(np.max(spectral_centroid))]
                }
            }
            
            soundscape_data["plants"].append(plant_features)
            
            # Combine audio for overall features
            if len(combined_audio) == 0:
                combined_audio = audio
            else:
                # Mix audio tracks
                min_len = min(len(combined_audio), len(audio))
                combined_audio = combined_audio[:min_len] + audio[:min_len]
        
        # Calculate combined features
        if len(combined_audio) > 0:
            combined_spectral_centroid = librosa.feature.spectral_centroid(y=combined_audio, sr=self.sample_rate)[0]
            combined_mfccs = librosa.feature.mfcc(y=combined_audio, sr=self.sample_rate, n_mfcc=13)
            
            soundscape_data["combined_audio_features"] = {
                "overall_harmony": float(np.std(combined_spectral_centroid)),
                "complexity": float(np.mean(np.std(combined_mfccs, axis=1))),
                "energy": float(np.mean(combined_audio ** 2)),
                "therapeutic_score": random.uniform(0.7, 0.95)  # Simulated therapeutic effectiveness
            }
        
        return soundscape_data

# Initialize the sonic symbiosis engine
sonic_engine = SonicSymbiosis()

@app.get("/", response_class=HTMLResponse)
async def homepage():
    """Serve the main application page"""
    with open("templates/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.get("/api/plants")
async def get_connected_plants():
    """Get list of connected plants with their current status"""
    return {"plants": connected_plants, "total_count": len(connected_plants)}

@app.post("/api/therapy/start")
async def start_therapy_session(session_data: TherapySession):
    """Start a new therapy session"""
    session_id = str(uuid.uuid4())
    
    # Validate selected plants
    valid_plant_ids = [p["id"] for p in connected_plants]
    invalid_plants = [pid for pid in session_data.selected_plants if pid not in valid_plant_ids]
    
    if invalid_plants:
        raise HTTPException(status_code=400, detail=f"Invalid plant IDs: {invalid_plants}")
    
    # Create session
    session_info = {
        "id": session_id,
        "start_time": datetime.now(),
        "end_time": datetime.now() + timedelta(minutes=session_data.duration_minutes),
        "user_mood": session_data.user_mood,
        "therapy_goal": session_data.therapy_goal,
        "duration_minutes": session_data.duration_minutes,
        "selected_plants": session_data.selected_plants,
        "status": "active"
    }
    
    active_sessions[session_id] = session_info
    
    return {
        "session_id": session_id,
        "message": "Therapy session started successfully",
        "session_info": session_info
    }

@app.delete("/api/therapy/{session_id}")
async def end_therapy_session(session_id: str):
    """End an active therapy session"""
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = active_sessions[session_id]
    session["status"] = "completed"
    session["actual_end_time"] = datetime.now()
    
    return {
        "message": "Therapy session ended successfully",
        "session_summary": session
    }

@app.get("/api/soundscape/{session_id}")
async def get_soundscape_data(session_id: str):
    """Get current soundscape data for a session"""
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = active_sessions[session_id]
    
    if session["status"] != "active":
        raise HTTPException(status_code=400, detail="Session is not active")
    
    # Generate soundscape data
    soundscape_data = sonic_engine.create_soundscape_data(
        session_id=session_id,
        plant_ids=session["selected_plants"],
        user_mood=session["user_mood"]
    )
    
    return soundscape_data

@app.websocket("/ws/live-soundscape/{session_id}")
async def websocket_live_soundscape(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for live soundscape streaming"""
    await websocket.accept()
    
    if session_id not in active_sessions:
        await websocket.close(code=4004, reason="Session not found")
        return
    
    session = active_sessions[session_id]
    
    try:
        while session["status"] == "active" and datetime.now() < session["end_time"]:
            # Generate new soundscape data
            soundscape_data = sonic_engine.create_soundscape_data(
                session_id=session_id,
                plant_ids=session["selected_plants"],
                user_mood=session["user_mood"]
            )
            
            # Send data to client
            await websocket.send_text(json.dumps(soundscape_data))
            
            # Wait before next update (2 seconds)
            await asyncio.sleep(2)
        
        # Session ended
        await websocket.send_text(json.dumps({"status": "session_ended"}))
        
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for session {session_id}")
    except Exception as e:
        print(f"WebSocket error for session {session_id}: {e}")
        await websocket.close(code=4000, reason="Internal error")

@app.get("/api/analytics/{session_id}")
async def get_session_analytics(session_id: str):
    """Get analytics data for a completed or active session"""
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = active_sessions[session_id]
    
    # Calculate session duration
    if session["status"] == "completed":
        duration = (session["actual_end_time"] - session["start_time"]).total_seconds() / 60
    else:
        duration = (datetime.now() - session["start_time"]).total_seconds() / 60
    
    # Generate analytics (simulated for demo)
    analytics = {
        "session_id": session_id,
        "duration_minutes": round(duration, 2),
        "plants_used": len(session["selected_plants"]),
        "therapy_effectiveness": {
            "stress_reduction": random.uniform(0.6, 0.9),
            "focus_improvement": random.uniform(0.5, 0.8),
            "mood_enhancement": random.uniform(0.7, 0.95),
            "overall_satisfaction": random.uniform(0.75, 0.95)
        },
        "plant_synchronization": {
            plant_id: {
                "harmony_score": random.uniform(0.6, 0.9),
                "contribution_level": random.uniform(0.4, 0.8)
            } for plant_id in session["selected_plants"]
        },
        "bioacoustic_insights": {
            "dominant_frequencies": [220, 330, 440],
            "harmonic_complexity": random.uniform(0.3, 0.7),
            "therapeutic_resonance": random.uniform(0.6, 0.9)
        }
    }
    
    return analytics

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)