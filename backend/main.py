from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from backend.utils.route_types import Subscriber
from backend.utils.db import create_supabase_client
from supabase import Client

# TODO
# Add mailer/scheduler
# Fix favicon.ico
# Check out https://taddy.org/developers/podcast-api for podcasts

app = FastAPI()
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["POST"],
)

@app.post("/")
def add_subscriber(subscriber: Subscriber, supabase_client: Client = Depends(create_supabase_client)) -> Subscriber:
    supabase_client.table("subscribers").insert({
        "email": subscriber.email,
        "topic": subscriber.topic,
        "time": subscriber.time
    }).execute()

    # Add to scheduler

    return subscriber



