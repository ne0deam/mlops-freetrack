from fastapi import FastAPI, HTTPException, Query
from recommender import load_model, recommend_songs
from schemas import RecommendationResponse
from typing import List

app = FastAPI(
        title="Spotify Recomender API",
        description="Получи рекомендации похожих песен по названию трека на основе косинусного сходства.",
        version="1.0.0",
        contact={
            "name": "Your Name",
            "email": "your_example@example.com"
        }
)

model = load_model()

@app.get("/", tags=["Health Check"])
def read_root():
    return {"message": "🎶 Spotify Recommender is running!"}

@app.get(
    "/api/recommend/",
    response_model=RecommendationResponse,
    summary="Получить рекомендации по песне",
    description="Возвращает список песен, похожих на указанную, используя косинусное сходство по признакам.",
    tags=["Recommendation"]
)
def get_recommendations(
    track_title: str = Query(..., description="Название песни для поиска"),
    N: int = Query(5, alias="n", ge=1, le=20, description="Количество рекомендаций (от 1 до 20)")
):
    recommendations = recommend_songs(model, track_title, N)

    if not recommendations:
        raise HTTPException(
            status_code=404,
            detail=f"Трек '{track_title}' не найден в базе данных."
        )

    return {"requested_track": track_title, "recommendations": recommendations}
