from pydantic import BaseModel, Field
from typing import List

class Song(BaseModel):
    track_name: str = Field(..., example="Time")
    artists: str = Field(..., example="Pink Floyd")
    album_name: str = Field(..., example="The Dark Side of the Moon")

class RecommendationResponse(BaseModel):
    requested_track: str = Field(..., example="Time")
    recommendations: List[Song]
