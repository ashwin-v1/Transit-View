from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
from app.routes import stops, kpis, vehicles

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(stops.router)
app.include_router(kpis.router)
app.include_router(vehicles.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Toronto Insights API"}

