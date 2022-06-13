from fastapi import Depends, FastAPI
from pydantic import BaseModel, constr
from sqlalchemy import false, true
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from models import Score
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    return scores

@app.get("/all/")
async def read_scores(db: Session = Depends(get_db)):
    query = db.query(Score).order_by(Score.score.desc())
    scores = db.execute(query).fetchall()
    return scores

@app.post("/score/")
def write_score(score_data: ScoreData, db: Session = Depends(get_db)):
    score = Score()
    score.name = score_data.name
    score.score = score_data.score
    db.add(score)
    db.commit()
    return True

@app.get("/reset/")
def write_score(db: Session = Depends(get_db)):
    db.execute('''DELETE FROM scores''')
    db.commit()
    return True

@app.get("/eligible/")
def write_score(db: Session = Depends(get_db), points: int = 200):
    scores = db.query(Score).filter(Score.score > points).count()
    if scores < 5:
        return true
    else:
        return false