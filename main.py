from fastapi import FastAPI

from api import quiz


app = FastAPI()
app.include_router(quiz.router)

@app.get("/")
def health_check():
    return {"message": "ok"}



