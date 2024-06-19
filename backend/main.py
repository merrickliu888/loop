from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from route_types import Subscriber
from db import supabase_client


app = FastAPI()
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["POST"],
)



@app.post("/")
def add_subscriber(subscriber: Subscriber) -> Subscriber:
    # Insert into db
    supabase_client.table("subscribers").insert({
        "email": subscriber.email,
        "topic": subscriber.topic,
        "time": subscriber.time
    }).execute()

    # Add to scheduler

    return subscriber



