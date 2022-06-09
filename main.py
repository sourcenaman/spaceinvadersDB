from fastapi import Depends, FastAPI
from pydantic import BaseModel, constr
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from models import Score

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

class ScoreData(BaseModel):
    name: constr(max_length=4)
    score: int

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/")
def read_scores(db: Session = Depends(get_db)):
    scores = db.query(Score).order_by(Score.score.desc())[:5]
    # scores = db.query(Score).all()
    print(scores)
    return scores
    return {"Hello": "World"}

@app.post("/score/")
def write_score(score_data: ScoreData, db: Session = Depends(get_db)):
    score = Score()
    score.name = score_data.name
    score.score = score_data.score
    db.add(score)
    db.commit()
    return True