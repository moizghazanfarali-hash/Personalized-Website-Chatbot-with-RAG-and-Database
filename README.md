# Isky — AI Knowledge Engine

A full-stack RAG (Retrieval-Augmented Generation) chatbot. Index any website URL, then ask questions — answers come from your indexed content first, with Gemini AI as fallback.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI |
| Frontend | Streamlit |
| Database | MongoDB Atlas |
| Vector DB | ChromaDB |
| AI Model | Gemini 2.5 Flash |
| Embeddings | all-MiniLM-L6-v2 |
| Auth | JWT (Bearer Token) |

---

## Project Structure

```
merged_project/
├── main.py                  # FastAPI entry point
├── streamlit_app.py         # Streamlit frontend
├── requirements.txt
├── .env                     # Environment variables (create this)
└── app/
    ├── config.py            # Settings
    ├── database.py          # MongoDB collections
    ├── security.py          # JWT auth
    ├── models.py            # Pydantic models
    ├── scrapper.py          # Web scraper
    ├── chunker.py           # Text chunker
    ├── embedding.py         # Sentence embeddings
    ├── vector_database.py   # ChromaDB
    ├── rag_pipeline.py      # RAG + Gemini
    └── routes/
        ├── auth.py          # /api/register, /api/login, /api/me
        ├── store_route.py   # /store/
        └── chat_route.py    # /chat/
```

---

## Setup

**1. Clone and install dependencies**
```bash
pip install -r requirements.txt
```

**2. Create `.env` file**
```env
MONGODB_URL=mongodb+srv://<user>:<password>@cluster.mongodb.net/
DB_NAME=isky_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
GEMINI_API_KEY=your-gemini-api-key
```

Get your free Gemini API key at [aistudio.google.com](https://aistudio.google.com)

**3. Run the backend** (Terminal 1)
```bash
python -m uvicorn app.main:app --reload
```

**4. Run the frontend** (Terminal 2)
```bash
streamlit run streamlit_app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/register` | Create account | No |
| POST | `/api/login` | Sign in | No |
| GET | `/api/me` | Get current user | Yes |
| POST | `/store/` | Index a URL | Yes |
| POST | `/chat/` | Ask a question | Yes |
| GET | `/chat/history` | Get chat history | Yes |
| GET | `/health` | Health check | No |

API docs available at [http://localhost:8000/docs](http://localhost:8000/docs)

---

## How It Works

1. **Register/Login** → get a JWT token
2. **Index a URL** → content is scraped, chunked, and stored in ChromaDB
3. **Ask a question** → system searches ChromaDB for relevant chunks, sends to Gemini
4. If relevant content found → answer comes from your indexed URLs
5. If not found → Gemini answers from its own knowledge

---

## Requirements

- Python 3.10+
- MongoDB Atlas account (free tier works)
- Gemini API key (free at Google AI Studio)
