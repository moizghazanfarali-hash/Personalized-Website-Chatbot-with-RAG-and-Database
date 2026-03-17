import google.generativeai as genai
from app.vector_database import search_chunks
from app.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def rag_answer(question: str, user_id: str = "") -> dict:
    # Sirf is user ke chunks search karo
    chunks = search_chunks(question, user_id=user_id)
    context = "\n".join(chunks).strip()

    relevance_prompt = f"""
Neeche kuch context diya gaya hai aur ek question hai.
Sirf "YES" ya "NO" jawab do.
Kya context mein is question ka jawab maujood hai?

Context:
{context}

Question:
{question}
"""
    relevance_response = model.generate_content(relevance_prompt)
    is_relevant = "YES" in relevance_response.text.upper()

    if is_relevant:
        prompt = f"""
Context:
{context}

Question:
{question}

Answer using only the provided context. Be helpful and concise.
"""
        response = model.generate_content(prompt)
        return {"answer": response.text, "from_url": True, "note": None}

    else:
        prompt = f"Answer the following question using your own knowledge:\n\nQuestion:\n{question}"
        response = model.generate_content(prompt)
        return {
            "answer":   response.text,
            "from_url": False,
            "note":     "LLM se generate kiya gaya answer",
        }