from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, HttpUrl

from app.scrapper   import scrape_website
from app.chunker  import chunk_text
from app.vector_database import store_chunks
from app.database   import websites_col
from app.security  import get_current_user

router = APIRouter(prefix="/store", tags=["Store"])


class StoreRequest(BaseModel):
    url: HttpUrl


@router.post("/")
def store_website(request: StoreRequest, current_user: str = Depends(get_current_user)):
    url_str = str(request.url)

    existing = websites_col.find_one({"url": url_str, "user_id": current_user})
    if existing:
        return {
            "message":      "this url already exist",
            "url":          url_str,
            "chunks_stored": existing.get("chunks_count", 0),
        }

    try:
        raw_text = scrape_website(url_str)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Scraping fail ho gayi: {str(e)}")

    if not raw_text or len(raw_text.strip()) < 50:
        raise HTTPException(status_code=422, detail="URL se kafi content nahi mila.")

    chunks = chunk_text(raw_text)

    try:
        store_chunks(chunks, url=url_str)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vector storage fail: {str(e)}")

    websites_col.insert_one({
        "user_id":      current_user,
        "url":          url_str,
        "chunks_count": len(chunks),
    })

    return {
        "message":      "Website successfully scrape aur store ho gayi.",
        "url":          url_str,
        "chunks_stored": len(chunks),
    }
