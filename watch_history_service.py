from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI()

# Mock data
users = {101, 102, 103}
movies = {201, 202, 203}
watch_history: Dict[int, List[int]] = {}


class WatchRequest(BaseModel):
    user_id: int
    movie_id: int


@app.post("/watch")
def watch_movie(request: WatchRequest):
    if request.user_id not in users:
        raise HTTPException(status_code=400, detail="Invalid user_id")
    if request.movie_id not in movies:
        raise HTTPException(status_code=400, detail="Invalid movie_id")

    watch_history.setdefault(request.user_id, []).append(request.movie_id)

    return {
        "status": "success",
        "user_id": request.user_id,
        "movie_id": request.movie_id
    }


@app.get("/watch_history")
def get_watch_history(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=400, detail="Invalid user_id")

    return {
        "user_id": user_id,
        "movies": watch_history.get(user_id, [])
    }
 
