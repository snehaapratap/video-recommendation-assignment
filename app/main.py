from fastapi import FastAPI, Query, HTTPException
import requests
import os
from dotenv import load_dotenv
from app.recommendation import train_model


load_dotenv()

app = FastAPI()

API_BASE_URL = os.getenv("API_BASE_URL")
FLIC_TOKEN = os.getenv("FLIC_TOKEN")

HEADERS = {"Flic-Token": FLIC_TOKEN}

@app.get("/feed")
def get_personalized_feed(username: str, category_id: int = None):
    url = f"{API_BASE_URL}/posts/view?page=1&page_size=1000"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch data")
    
    posts = response.json()
    
    if category_id:
        posts = [post for post in posts if post["category_id"] == category_id]
    
    return {"username": username, "recommended_videos": posts[:10]}


@app.get("/train")
def train():
    data = {"features": np.random.rand(100, 5), "labels": np.random.randint(0, 10, size=(100,))}
    model = train_model(data)
    return {"message": "Model trained successfully"}

