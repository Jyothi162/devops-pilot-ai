from fastapi import FastAPI

app = FastAPI(
    title="DevOps Pilot AI",
    description="Multi-Agent DevOps Automation Platform",
    version="0.1.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to DevOps Pilot AI",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }