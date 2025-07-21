# main.py (entry point of your FastAPI app)
from fastapi import FastAPI
from auth import auth_router
from crud import crud_router
from database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow requests from your frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://edtech-tracker.netlify.app"],  # ⚠️ Change "*" to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_router)
app.include_router(crud_router)

@app.get("/")
def root():
    return {"message": "Assignment Tracker API is running!"}
