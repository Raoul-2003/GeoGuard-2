from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="GeoGuard V2 API",
    description="API Professionnelle pour la plateforme d'intelligence territoriale GeoGuard",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "GeoGuard V2 API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
