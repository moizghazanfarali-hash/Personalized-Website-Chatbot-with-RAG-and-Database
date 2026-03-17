import google.generativeai as genai
from app.vector_database import search_chunks
from app.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def rag_answer(question: str, user_id: str = "") -> dict:
    
    chunks = search_chunks(question, user_id=user_id)
    context = "\n".join(chunks).strip()

    relevance_prompt = f"""
You are a helpful, concise AI assistant.

Rules you MUST follow:
- Answer in the same language the user asked in (Urdu, English, Roman Urdu, etc.)
- Keep answers SHORT and TO THE POINT — no unnecessary explanation
- Do NOT use markdown formatting (no **, no ##, no bullet points with *)
- Do NOT ask clarifying questions — give your best direct answer
- If the question is ambiguous, pick the most common interpretation and answer it
- Use simple, plain text only
- Maximum 5-6 lines for general questions
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
