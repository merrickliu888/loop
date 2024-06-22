from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.utils.route_types import Subscriber
from backend.utils.db import supabase_client

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
def add_subscriber(subscriber: Subscriber) -> Subscriber:
    # Make sure topic is safe

    # Insert into db
    supabase_client.table("subscribers").insert({
        "email": subscriber.email,
        "topic": subscriber.topic,
        "time": subscriber.time
    }).execute()

    # Add to scheduler

    return subscriber



