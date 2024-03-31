from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import api_router

app = FastAPI(title="Organization-Tool")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],  # Adicione o header a ser exposto aqui
)
app.include_router(api_router)