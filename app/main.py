from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.store_route import router as store_router
from app.routes.chat_route  import router as chat_router
from app.routes.auth import router as auth_router

app = FastAPI(
    title="Isky RAG Chatbot API",
    description="Auth + RAG Chatbot — Register, Login, Store URLs, Chat",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)   
app.include_router(store_router)   
app.include_router(chat_router)    

@app.get("/health", tags=["System"])
def health():
    return {"status": "ok", "message": "Isky RAG ApI chal rahi hai "}
