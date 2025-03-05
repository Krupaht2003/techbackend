from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import metrics, optimization, health, auth, users, dashboard
from starlette.middleware.sessions import SessionMiddleware
app = FastAPI(title="Resource Monitoring & Optimization Tool")

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include routes
app.include_router(metrics.router, prefix="/api/metrics", tags=["Metrics"])
app.include_router(optimization.router, prefix="/api/services/optimization", tags=["Optimization"])
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["User Management"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])


# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the Resource Monitoring & Optimization Tool"}

@app.get("/")
async def root():
    return {"message": "Welcome to Resource Monitoring & Optimization Tool"}

# Start collecting metrics when the application starts
@app.on_event("startup")
async def startup_event():
    # The metrics collection thread is already started when metrics_service is imported
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)