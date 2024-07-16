from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import quiz, auth, profile, qna

app = FastAPI()
app.include_router(quiz.router)
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(qna.router)

# CORS 
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"message":"ok"}



