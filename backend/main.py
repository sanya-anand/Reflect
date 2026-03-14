from fastapi import FastAPI
from database import Base, engine
from models import journal
from routes import journal_routes
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="REFLECT API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(journal_routes.router)

@app.get("/")
def home():
    return {"message": "REFLECT API Running"}