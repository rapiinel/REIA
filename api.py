from fastapi import FastAPI
from reia.crew import Reia

app = FastAPI()

@app.post("/search")
def search_property(payload: dict):
    result = Reia().crew().kickoff(inputs=payload)
    return result.pydantic