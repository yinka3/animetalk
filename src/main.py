import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import users, buyers, sellers


app = FastAPI()

app.include_router(users.router)
app.include_router(buyers.router)
app.include_router(sellers.router)

if __name__ == "__main__":
    uvicorn.run("src.main:app" , host="127.0.0.1", port=8000, reload=True)