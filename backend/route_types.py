from pydantic import BaseModel

class Subscriber(BaseModel):
    email: str
    time: str
    topic: str