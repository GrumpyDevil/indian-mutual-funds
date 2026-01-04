from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import portfolio, benchmark, cas
import uvicorn

app = FastAPI(title="Indian Mutual Funds Portfolio API")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(portfolio.router)
app.include_router(benchmark.router)
app.include_router(cas.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Indian Mutual Funds Portfolio API"}

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
