from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from app.rag_pipeline import rag_answer
from app.database     import save_chat, chat_col
from app.security     import get_current_user

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    message: str


@router.post("/")
def chat(request: ChatRequest, current_user: str = Depends(get_current_user)):
    """User ka question lo, RAG se answer generate karo, aur history save karo."""
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message khali nahi hona chahiye.")

    try:
        result = rag_answer(request.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG pipeline error: {str(e)}")

    save_chat(user_id=current_user, message=request.message, response=result["answer"])

    response_data = {
        "user_id":  current_user,
        "question": request.message,
        "answer":   result["answer"],
        "from_url": result["from_url"],
    }
    if result["note"]:
        response_data["note"] = result["note"]

    return response_data


@router.get("/history")
def get_history(current_user: str = Depends(get_current_user)):
    chats = list(chat_col.find({"user_id": current_user}, {"_id": 0}))

    if not chats:
        return {"user_id": current_user, "history": [], "message": "Koi history nahi mili."}

    return {
        "user_id":       current_user,
        "total_messages": len(chats),
        "history":       chats,
    }
