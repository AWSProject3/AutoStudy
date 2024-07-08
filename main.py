from fastapi import Depends, FastAPI

from api import quiz, auth


app = FastAPI()
app.include_router(quiz.router)
app.include_router(auth.router)

@app.get("/")
def health_check():
    return {"message": "ok"}



