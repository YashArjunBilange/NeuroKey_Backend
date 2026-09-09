from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import health, scraping, analysis, nlp_api, prediction, conversation
from app.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix=settings.API_V1_STR, tags=["Health"])
app.include_router(scraping.router, prefix=settings.API_V1_STR, tags=["Scraping"])
app.include_router(analysis.router, prefix=settings.API_V1_STR, tags=["Analysis"])
app.include_router(nlp_api.router, prefix=settings.API_V1_STR, tags=["NLP"])
app.include_router(prediction.router, prefix=f"{settings.API_V1_STR}/predict", tags=["Prediction"])
app.include_router(conversation.router, prefix=f"{settings.API_V1_STR}/conversation", tags=["Conversation"])

@app.get("/")
async def root():
    return {"message": "Welcome to NLP Smart Keyboard API"}
