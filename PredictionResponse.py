from pydantic import BaseModel


class PredictionResponse(BaseModel):
    prediction: int
    probability: str
    conclusion: list
