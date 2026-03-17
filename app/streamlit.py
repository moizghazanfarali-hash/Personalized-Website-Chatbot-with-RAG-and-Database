import streamlit as st
import requests
import time
import base64
from datetime import datetime

st.set_page_config(
    page_title="Isky — AI Knowledge Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_BASE = "http://127.0.0.1:8000"

# ── Robot image (base64 embedded) ─────────────────────────────────────────────
ROBOT_B64 = "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"

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #EEF2F7 !important;
    color: #1a1a2e !important;
}

[data-testid="stHeader"], [data-testid="stDecoration"],
footer, #MainMenu { display: none !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #E2E8F0 !important;
    box-shadow: 2px 0 8px rgba(0,0,0,0.04) !important;
}
[data-testid="stSidebarContent"] { padding: 0 !important; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: #CBD5E0; border-radius: 4px; }

/* ── ALL INPUTS ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #FFFFFF !important;
    border: 1.5px solid #E2E8F0 !important;
    border-radius: 8px !important;
    color: #1a1a2e !important;
    font-size: 14px !important;
    padding: 10px 14px !important;
    box-shadow: none !important;
    transition: border-color 0.2s !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #6C63FF !important;
    box-shadow: 0 0 0 3px rgba(108,99,255,0.12) !important;
}
.stTextInput > div > div > input::placeholder { color: #A0AEC0 !important; }
.stTextInput label, .stTextArea label {
    color: #4A5568 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #6C63FF 0%, #4F46E5 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    padding: 10px 22px !important;
    transition: all 0.2s !important;
    box-shadow: 0 2px 8px rgba(108,99,255,0.3) !important;
    letter-spacing: 0.01em !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(108,99,255,0.4) !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 2px solid #E2E8F0 !important;
    gap: 0 !important; padding: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    border-bottom: 3px solid transparent !important;
    color: #A0AEC0 !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    padding: 12px 22px !important;
    margin-bottom: -2px !important;
    border-radius: 0 !important;
    transition: all 0.15s !important;
}
.stTabs [aria-selected="true"] {
    color: #6C63FF !important;
    border-bottom-color: #6C63FF !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-panel"] { padding: 24px 0 !important; }

/* ── ALERTS ── */
.stSuccess { background: #F0FFF4 !important; border: 1px solid #9AE6B4 !important; border-radius: 8px !important; color: #276749 !important; }
.stError   { background: #FFF5F5 !important; border: 1px solid #FEB2B2 !important; border-radius: 8px !important; color: #C53030 !important; }
.stWarning { background: #FFFBEB !important; border: 1px solid #F6E05E !important; border-radius: 8px !important; color: #744210 !important; }

/* ── METRICS ── */
[data-testid="metric-container"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    padding: 20px 24px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
}
[data-testid="metric-container"] label {
    color: #718096 !important; font-size: 12px !important;
    text-transform: uppercase !important; letter-spacing: 0.08em !important; font-weight: 600 !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #1a1a2e !important; font-size: 28px !important; font-weight: 700 !important;
}

/* ── EXPANDER ── */
.streamlit-expanderHeader {
    background: #FFFFFF !important; border: 1px solid #E2E8F0 !important;
    border-radius: 8px !important; color: #4A5568 !important;
    font-size: 13px !important; font-weight: 600 !important;
}
.streamlit-expanderContent {
    background: #F7FAFC !important; border: 1px solid #E2E8F0 !important;
    border-top: none !important; border-radius: 0 0 8px 8px !important;
}
[data-testid="column"] { padding: 0 6px !important; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ────────────────────────────────────────────────────────────────────

def api_post(endpoint, data, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        r = requests.post(f"{API_BASE}{endpoint}", json=data, headers=headers, timeout=30)
        return {"ok": r.status_code < 300, "data": r.json()}
    except requests.exceptions.ConnectionError:
        return {"ok": False, "data": {"detail": "Cannot connect to backend. Make sure the server is running on port 8000."}}
    except Exception as e:
        return {"ok": False, "data": {"detail": str(e)}}


def api_get(endpoint, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        r = requests.get(f"{API_BASE}{endpoint}", headers=headers, timeout=30)
        return {"ok": r.status_code < 300, "data": r.json()}
    except requests.exceptions.ConnectionError:
        return {"ok": False, "data": {"detail": "Cannot connect to backend."}}
    except Exception as e:
        return {"ok": False, "data": {"detail": str(e)}}


def init_session():
    for k, v in {
        "token": None, "user_name": None, "user_email": None,
        "messages": [], "stored_urls": [], "page": "chat",
    }.items():
        if k not in st.session_state:
            st.session_state[k] = v


def logged_in():
    return bool(st.session_state.get("token"))


def do_logout():
    for k in ["token", "user_name", "user_email"]:
        st.session_state[k] = None
    st.session_state.messages = []
    st.session_state.stored_urls = []
    st.rerun()


def greeting():
    h = datetime.now().hour
    if h < 12: return "Good morning"
    if h < 17: return "Good afternoon"
    if h < 21: return "Good evening"
    return "Good night"


# ── SIDEBAR ───────────────────────────────────────────────────────────────────

def sidebar():
    with st.sidebar:
        # Logo
        st.markdown("""
        <div style="padding:22px 20px 18px; border-bottom:1px solid #E2E8F0;">
            <div style="display:flex; align-items:center; gap:10px;">
                <div style="width:36px; height:36px; border-radius:10px;
                            background:linear-gradient(135deg,#6C63FF,#4F46E5);
                            color:#fff; display:flex; align-items:center;
                            justify-content:center; font-size:18px; font-weight:700;
                            box-shadow:0 2px 8px rgba(108,99,255,0.35);">⚡</div>
                <div>
                    <div style="font-size:16px; font-weight:700; color:#1a1a2e;">NexusAI</div>
                    <div style="font-size:10.5px; color:#A0AEC0;">AI Knowledge Engine</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if logged_in():
            name    = st.session_state.user_name or "User"
            email   = st.session_state.user_email or ""
            initial = name[0].upper()

            st.markdown(f"""
            <div style="margin:14px 12px 6px; padding:10px 12px; background:#F7FAFC;
                        border:1px solid #E2E8F0; border-radius:10px;
                        display:flex; align-items:center; gap:10px;">
                <div style="width:32px; height:32px; border-radius:50%;
                            background:linear-gradient(135deg,#6C63FF,#4F46E5);
                            color:#fff; display:flex; align-items:center;
                            justify-content:center; font-size:13px; font-weight:700;
                            flex-shrink:0;">{initial}</div>
                <div style="overflow:hidden; min-width:0;">
                    <div style="font-size:13px; font-weight:600; color:#1a1a2e;
                                white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">User: {name}</div>
                    <div style="font-size:11px; color:#A0AEC0;
                                white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{email}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
            st.markdown('<div style="padding:4px 8px; font-size:11px; color:#A0AEC0; font-weight:600; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:4px;">Navigation</div>', unsafe_allow_html=True)

            pages = [("💬  Chat", "chat"), ("🧠  Knowledge Base", "knowledge"),
                     ("📋  History", "history"), ("⚙️  Settings", "settings")]
            for label, key in pages:
                if st.button(label, key=f"nav_{key}", use_container_width=True):
                    st.session_state.page = key
                    st.rerun()

            st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
            st.markdown('<hr style="border:none; border-top:1px solid #E2E8F0; margin:0 8px;">', unsafe_allow_html=True)
            st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

            if st.button("🚪  Logout", key="signout_btn", use_container_width=True):
                do_logout()
        else:
            st.markdown("""
            <div style="padding:20px 18px; font-size:13px; color:#718096; line-height:1.7;">
                Sign in or create an account to get started.
            </div>
            """, unsafe_allow_html=True)


# ── AUTH PAGE ─────────────────────────────────────────────────────────────────

def page_auth():
    _, col, _ = st.columns([1, 1.4, 1])
    with col:

        # Hero with robot image
        st.markdown(f"""
        <div style="text-align:center; padding:40px 0 28px;">
            <img src="data:image/jpeg;base64,{ROBOT_B64}"
                 style="width:100px; height:100px; object-fit:contain;
                        filter:drop-shadow(0 8px 20px rgba(108,99,255,0.3));
                        margin-bottom:16px;" />
            <div style="font-size:28px; font-weight:700; color:#1a1a2e;
                        letter-spacing:-0.02em;">Welcome to NexusAI</div>
            <div style="color:#718096; font-size:13.5px; margin-top:6px; line-height:1.6;">
                Your personal AI knowledge engine
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Card
        st.markdown("""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0;
                    border-radius:16px; padding:28px 28px 22px;
                    box-shadow:0 4px 20px rgba(0,0,0,0.07);">
        """, unsafe_allow_html=True)

        t1, t2 = st.tabs(["Sign in", "Create account"])

        with t1:
            st.markdown('<div style="height:6px;"></div>', unsafe_allow_html=True)
            email = st.text_input("Email address", placeholder="you@example.com", key="li_email")
            pwd   = st.text_input("Password", type="password", placeholder="Your password", key="li_pwd")
            st.markdown('<div style="height:4px;"></div>', unsafe_allow_html=True)
            if st.button("Sign in →", key="login_btn", use_container_width=True):
                if not email or not pwd:
                    st.error("Please enter your email and password.")
                else:
                    with st.spinner("Signing in..."):
                        time.sleep(0.3)
                        res = api_post("/api/login", {"email": email, "password": pwd})
                    if res["ok"]:
                        d = res["data"]
                        st.session_state.token      = d["token"]
                        st.session_state.user_name  = d["name"]
                        st.session_state.user_email = d["email"]
                        st.session_state.page       = "chat"
                        st.success("✓ Signed in successfully!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error(res["data"].get("detail", "Sign in failed."))

        with t2:
            st.markdown('<div style="height:6px;"></div>', unsafe_allow_html=True)
            name   = st.text_input("Full name", placeholder="Your name", key="reg_name")
            email2 = st.text_input("Email address", placeholder="you@example.com", key="reg_email")
            pwd2   = st.text_input("Password", type="password", placeholder="Min. 6 characters", key="reg_pwd")
            st.markdown('<div style="height:4px;"></div>', unsafe_allow_html=True)
            if st.button("Create account →", key="reg_btn", use_container_width=True):
                if not name or not email2 or not pwd2:
                    st.error("All fields are required.")
                elif len(pwd2) < 6:
                    st.warning("Password must be at least 6 characters.")
                else:
                    with st.spinner("Creating account..."):
                        time.sleep(0.3)
                        res = api_post("/api/register", {"name": name, "email": email2, "password": pwd2})
                    if res["ok"]:
                        d = res["data"]
                        st.session_state.token      = d["token"]
                        st.session_state.user_name  = d["name"]
                        st.session_state.user_email = d["email"]
                        st.session_state.page       = "chat"
                        st.success("✓ Account created! Welcome aboard.")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error(res["data"].get("detail", "Registration failed."))

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div style="text-align:center; margin-top:16px; font-size:11px; color:#A0AEC0;
                    display:flex; align-items:center; justify-content:center; gap:10px;">
            <span>Gemini 2.5</span><span>·</span>
            <span>ChromaDB</span><span>·</span>
            <span>MongoDB</span>
        </div>
        """, unsafe_allow_html=True)


# ── CHAT PAGE ─────────────────────────────────────────────────────────────────

def page_chat():
    token = st.session_state.token
    name  = st.session_state.user_name or "there"
    msgs  = st.session_state.messages

    # Header
    st.markdown(f"""
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px;
                padding:20px 24px; margin-bottom:20px;
                box-shadow:0 1px 4px rgba(0,0,0,0.06);">
        <div style="display:flex; align-items:center; justify-content:space-between;">
            <div>
                <div style="font-size:22px; font-weight:700; color:#1a1a2e;">AI Assistant Dashboard</div>
                <div style="font-size:13px; color:#718096; margin-top:3px;">
                    {greeting()}, {name}! Ask anything from your knowledge base.
                </div>
            </div>
            <img src="data:image/jpeg;base64,{ROBOT_B64}"
                 style="width:64px; height:64px; object-fit:contain;
                        filter:drop-shadow(0 4px 12px rgba(108,99,255,0.25));" />
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats row
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Messages", len([m for m in msgs if m["role"] == "user"]))
    with c2: st.metric("Mode", "Knowledge Base" if any(m.get("from_url") for m in msgs if m["role"]=="assistant") else "General AI")
    with c3:
        sources = list(set([m.get("note","").split("//")[1].split("/")[0] if m.get("note") and "//" in m.get("note","") else "" for m in msgs if m.get("note")]))
        st.metric("Source", sources[0] if sources and sources[0] else "None")

    st.markdown('<div style="height:6px;"></div>', unsafe_allow_html=True)

    # Message area
    st.markdown("""
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px;
                padding:20px; margin-bottom:12px; box-shadow:0 1px 4px rgba(0,0,0,0.05);
                min-height:200px;">
    """, unsafe_allow_html=True)

    if not msgs:
        st.markdown(f"""
        <div style="text-align:center; padding:30px 20px; color:#A0AEC0;">
            <img src="data:image/jpeg;base64,{ROBOT_B64}"
                 style="width:80px; height:80px; object-fit:contain; opacity:0.6; margin-bottom:12px;" />
            <div style="font-size:15px; font-weight:600; color:#4A5568; margin-bottom:6px;">
                Ready to help!
            </div>
            <div style="font-size:13px; line-height:1.6;">
                Start a conversation. Answers pull from your indexed URLs first,<br>then fall back to AI.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in msgs:
            if msg["role"] == "user":
                st.markdown(f"""
                <div style="display:flex; justify-content:flex-end; margin-bottom:12px;">
                    <div style="max-width:70%; background:linear-gradient(135deg,#6C63FF,#4F46E5);
                                color:#fff; padding:11px 16px; border-radius:16px 16px 4px 16px;
                                font-size:14px; line-height:1.65; word-break:break-word;
                                box-shadow:0 2px 8px rgba(108,99,255,0.3);">
                        {msg['content'].replace(chr(10), '<br>')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                if msg.get("from_url"):
                    badge = '<span style="display:inline-flex; align-items:center; gap:4px; background:#F0FFF4; color:#276749; font-size:10px; font-weight:600; padding:2px 10px; border-radius:99px; border:1px solid #9AE6B4; margin-bottom:7px;">📚 From knowledge base</span>'
                else:
                    badge = '<span style="display:inline-flex; align-items:center; gap:4px; background:#EBF4FF; color:#2B6CB0; font-size:10px; font-weight:600; padding:2px 10px; border-radius:99px; border:1px solid #90CDF4; margin-bottom:7px;">🤖 AI generated</span>'

                note = ""
                if msg.get("note"):
                    note = f'<div style="margin-top:8px; padding:8px 12px; background:#EBF4FF; border:1px solid #90CDF4; border-radius:8px; font-size:12px; color:#2B6CB0; line-height:1.5;">🔗 {msg["note"]}</div>'

                st.markdown(f"""
                <div style="display:flex; gap:10px; margin-bottom:16px; align-items:flex-start;">
                    <img src="data:image/jpeg;base64,{ROBOT_B64}"
                         style="width:32px; height:32px; object-fit:contain;
                                border-radius:8px; flex-shrink:0; margin-top:2px;
                                border:1px solid #E2E8F0;" />
                    <div style="flex:1; min-width:0;">
                        {badge}
                        <div style="background:#F7FAFC; border:1px solid #E2E8F0;
                                    border-radius:4px 14px 14px 14px; padding:12px 15px;
                                    font-size:14px; line-height:1.75; color:#1a1a2e;
                                    word-break:break-word;">
                            {msg['content'].replace(chr(10), '<br>')}
                        </div>
                        {note}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Input + buttons row
    st.markdown("""
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px;
                padding:16px 18px; box-shadow:0 1px 4px rgba(0,0,0,0.05);">
        <div style="font-size:12px; color:#A0AEC0; font-weight:600;
                    text-transform:uppercase; letter-spacing:0.06em; margin-bottom:8px;">Message</div>
    """, unsafe_allow_html=True)

    c_in, c_btn = st.columns([8, 1])
    with c_in:
        user_input = st.text_input(
            "msg", placeholder="Type your message here...",
            key="chat_input", label_visibility="collapsed"
        )
    with c_btn:
        send = st.button("Send", key="send_btn", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Buttons row
    st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
    b1, b2, _ = st.columns([1, 1, 4])
    with b1:
        if st.button("🗑  Clear Chat", key="clear_chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with b2:
        if st.button("🚪  Logout", key="logout_chat", use_container_width=True):
            do_logout()

    if send and user_input.strip():
        _send_message(user_input, token)

    # Suggestions if no msgs
    if not msgs:
        st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:11px; color:#A0AEC0; font-weight:600; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:8px;">Quick suggestions</div>', unsafe_allow_html=True)
        suggestions = [
            "Summarize the content from my indexed URLs",
            "What are the key points from stored content?",
            "What is the latest information available?",
            "Give me an overview of everything you know",
        ]
        c1, c2 = st.columns(2)
        for i, s in enumerate(suggestions):
            with (c1 if i % 2 == 0 else c2):
                if st.button(s, key=f"sug_{i}", use_container_width=True):
                    _send_message(s, token)


def _send_message(text, token):
    st.session_state.messages.append({"role": "user", "content": text})
    with st.spinner("Thinking..."):
        res = api_post("/chat/", {"message": text}, token=token)
    if res["ok"]:
        d = res["data"]
        st.session_state.messages.append({
            "role": "assistant",
            "content": d["answer"],
            "from_url": d.get("from_url", False),
            "note": d.get("note"),
        })
    else:
        st.session_state.messages.append({
            "role": "assistant",
            "content": res["data"].get("detail", "Something went wrong. Please try again."),
            "from_url": False, "note": None,
        })
    st.rerun()


# ── KNOWLEDGE BASE ────────────────────────────────────────────────────────────

def page_knowledge():
    token = st.session_state.token

    st.markdown("""
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px;
                padding:20px 24px; margin-bottom:20px; box-shadow:0 1px 4px rgba(0,0,0,0.06);">
        <div style="font-size:22px; font-weight:700; color:#1a1a2e;">🧠 Knowledge Base</div>
        <div style="font-size:13px; color:#718096; margin-top:4px;">
            Add URLs — AI will scrape, chunk, and index the content automatically.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Indexed URLs", len(st.session_state.stored_urls))
    with c2: st.metric("Total Chunks", sum(u.get("chunks", 0) for u in st.session_state.stored_urls))
    with c3: st.metric("Status", "Active ✅")

    st.markdown('<div style="height:18px;"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px;
                padding:22px 24px; margin-bottom:18px; box-shadow:0 1px 4px rgba(0,0,0,0.05);">
        <div style="font-size:14px; font-weight:600; color:#1a1a2e; margin-bottom:14px;">
            🔗 Add a Website URL
        </div>
    """, unsafe_allow_html=True)

    url = st.text_input("Website URL", placeholder="https://example.com/article", key="url_in")
    if st.button("Index Website", key="index_btn", use_container_width=False):
        if not url.strip():
            st.error("Please enter a URL.")
        elif not url.startswith(("http://", "https://")):
            st.error("URL must start with http:// or https://")
        else:
            with st.spinner("Scraping and indexing..."):
                res = api_post("/store/", {"url": url}, token=token)
            if res["ok"]:
                d = res["data"]
                st.success(f"✓ {d['message']} — {d['chunks_stored']} chunks indexed.")
                st.session_state.stored_urls.append({
                    "url": url, "chunks": d["chunks_stored"],
                    "time": datetime.now().strftime("%H:%M"),
                })
                st.rerun()
            else:
                st.error(res["data"].get("detail", "Could not index URL."))

    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.stored_urls:
        st.markdown('<div style="font-size:12px; color:#A0AEC0; font-weight:600; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:10px;">Indexed Sources</div>', unsafe_allow_html=True)
        for item in st.session_state.stored_urls:
            domain = item["url"].split("/")[2] if len(item["url"].split("/")) > 2 else item["url"]
            st.markdown(f"""
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px;
                        padding:14px 18px; margin-bottom:8px;
                        display:flex; align-items:center; justify-content:space-between;
                        box-shadow:0 1px 3px rgba(0,0,0,0.05);">
                <div style="display:flex; align-items:center; gap:12px; overflow:hidden;">
                    <div style="width:36px; height:36px; border-radius:9px;
                                background:linear-gradient(135deg,#6C63FF,#4F46E5);
                                color:#fff; display:flex; align-items:center;
                                justify-content:center; font-size:14px; flex-shrink:0;">🌐</div>
                    <div style="overflow:hidden;">
                        <div style="font-size:13px; font-weight:600; color:#1a1a2e;
                                    white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{domain}</div>
                        <div style="font-size:11px; color:#A0AEC0; margin-top:1px;
                                    white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{item['url']}</div>
                    </div>
                </div>
                <div style="display:flex; align-items:center; gap:10px; flex-shrink:0;">
                    <div style="font-size:12px; color:#718096;">{item['chunks']} chunks</div>
                    <div style="background:#F0FFF4; color:#276749; font-size:11px;
                                font-weight:600; padding:3px 10px; border-radius:99px;
                                border:1px solid #9AE6B4;">✓ Indexed</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center; padding:44px; background:#FFFFFF;
                    border:2px dashed #E2E8F0; border-radius:14px;">
            <div style="font-size:24px; margin-bottom:10px;">🧠</div>
            <div style="font-size:13px; color:#A0AEC0;">No URLs indexed yet.<br>Add one above to get started.</div>
        </div>
        """, unsafe_allow_html=True)


# ── HISTORY ───────────────────────────────────────────────────────────────────

def page_history():
    token = st.session_state.token

    st.markdown("""
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px;
                padding:20px 24px; margin-bottom:20px; box-shadow:0 1px 4px rgba(0,0,0,0.06);">
        <div style="font-size:22px; font-weight:700; color:#1a1a2e;">📋 History</div>
        <div style="font-size:13px; color:#718096; margin-top:4px;">Your past conversations</div>
    </div>
    """, unsafe_allow_html=True)

    _, cr = st.columns([5, 1])
    with cr:
        refresh = st.button("↻ Refresh", key="ref_h", use_container_width=True)

    if refresh or "hist" not in st.session_state:
        with st.spinner("Loading history..."):
            res = api_get("/chat/history", token=token)
        st.session_state.hist = res["data"] if res["ok"] else None

    data = st.session_state.get("hist")

    if data is None:
        st.error("Could not load history.")
    elif not data.get("history"):
        st.markdown("""
        <div style="text-align:center; padding:44px; background:#FFFFFF;
                    border:2px dashed #E2E8F0; border-radius:14px;">
            <div style="font-size:22px; margin-bottom:10px;">📋</div>
            <div style="font-size:13px; color:#A0AEC0;">No conversations yet.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        chats = data["history"]
        st.markdown(f'<div style="font-size:12px; color:#A0AEC0; margin-bottom:12px;">{len(chats)} conversation{"s" if len(chats)!=1 else ""}</div>', unsafe_allow_html=True)
        for i, chat in enumerate(reversed(chats)):
            q     = chat.get("message", "")
            label = (q[:74] + "…") if len(q) > 74 else q
            with st.expander(label, expanded=(i == 0)):
                st.markdown(f"""
                <div style="padding:4px 0;">
                    <div style="margin-bottom:12px;">
                        <div style="font-size:10px; font-weight:700; color:#718096;
                                    text-transform:uppercase; letter-spacing:0.07em; margin-bottom:6px;">You asked</div>
                        <div style="background:linear-gradient(135deg,#6C63FF,#4F46E5); color:#fff;
                                    border-radius:10px; padding:10px 14px;
                                    font-size:13px; line-height:1.65;">{chat.get('message','')}</div>
                    </div>
                    <div>
                        <div style="font-size:10px; font-weight:700; color:#276749;
                                    text-transform:uppercase; letter-spacing:0.07em; margin-bottom:6px;">🤖 AI replied</div>
                        <div style="background:#F7FAFC; border:1px solid #E2E8F0;
                                    border-radius:10px; padding:10px 14px;
                                    font-size:13px; color:#1a1a2e; line-height:1.75;">
                            {chat.get('response','').replace(chr(10), '<br>')}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)


# ── SETTINGS ──────────────────────────────────────────────────────────────────

def page_settings():
    name  = st.session_state.user_name or "User"
    email = st.session_state.user_email or ""

    st.markdown("""
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px;
                padding:20px 24px; margin-bottom:20px; box-shadow:0 1px 4px rgba(0,0,0,0.06);">
        <div style="font-size:22px; font-weight:700; color:#1a1a2e;">⚙️ Settings</div>
        <div style="font-size:13px; color:#718096; margin-top:4px;">Account and application settings</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px;
                    padding:22px 24px; margin-bottom:12px; box-shadow:0 1px 4px rgba(0,0,0,0.05);">
            <div style="font-size:11px; font-weight:700; color:#718096; text-transform:uppercase;
                        letter-spacing:0.08em; margin-bottom:16px;">Profile</div>
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
                <div style="width:44px; height:44px; border-radius:50%;
                            background:linear-gradient(135deg,#6C63FF,#4F46E5); color:#fff;
                            display:flex; align-items:center; justify-content:center;
                            font-size:18px; font-weight:700;">{name[0].upper()}</div>
                <div>
                    <div style="font-size:14px; font-weight:600; color:#1a1a2e;">{name}</div>
                    <div style="font-size:12px; color:#A0AEC0;">{email}</div>
                </div>
            </div>
            <div style="background:#F7FAFC; border:1px solid #E2E8F0;
                        border-radius:8px; padding:10px 12px;">
                <div style="font-size:10px; color:#A0AEC0; text-transform:uppercase;
                            letter-spacing:0.08em; margin-bottom:3px;">Session token</div>
                <div style="font-family:monospace; font-size:11px; color:#718096;
                            word-break:break-all; line-height:1.5;">
                    {st.session_state.token[:44]}…
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#FFF5F5; border:1px solid #FEB2B2; border-radius:14px;
                    padding:22px 24px; box-shadow:0 1px 4px rgba(0,0,0,0.05);">
            <div style="font-size:11px; font-weight:700; color:#C53030; text-transform:uppercase;
                        letter-spacing:0.08em; margin-bottom:8px;">Danger Zone</div>
            <div style="font-size:13px; color:#718096; margin-bottom:14px; line-height:1.6;">
                Signing out clears your current session.
            </div>
        """, unsafe_allow_html=True)
        if st.button("Sign out", key="s_logout"):
            do_logout()
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px;
                    padding:22px 24px; margin-bottom:12px; box-shadow:0 1px 4px rgba(0,0,0,0.05);">
            <div style="font-size:11px; font-weight:700; color:#718096; text-transform:uppercase;
                        letter-spacing:0.08em; margin-bottom:14px;">API Connection</div>
        """, unsafe_allow_html=True)
        if st.button("Check connection", key="chk_api"):
            with st.spinner("Checking..."):
                res = api_get("/health")
            if res["ok"]:
                st.success("✓ " + res["data"].get("message", "Connected"))
            else:
                st.error("✗ " + res["data"].get("detail", "Connection failed"))

        for method, ep, label in [
            ("POST","/api/register","Register"), ("POST","/api/login","Login"),
            ("GET", "/api/me",      "Profile"),  ("POST","/store/","Store URL"),
            ("POST","/chat/",       "Chat"),     ("GET", "/chat/history","History"),
        ]:
            c  = "#276749" if method=="GET" else "#744210"
            bg = "#F0FFF4" if method=="GET" else "#FFFBEB"
            bd = "#9AE6B4" if method=="GET" else "#F6E05E"
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:9px; padding:7px 0;
                        border-bottom:1px solid #EDF2F7; font-size:12px;">
                <span style="background:{bg}; color:{c}; font-size:9px; font-weight:700;
                             padding:2px 7px; border-radius:4px; font-family:monospace;
                             border:1px solid {bd}; flex-shrink:0;">{method}</span>
                <span style="font-family:monospace; color:#718096; flex:1; font-size:11.5px;">{ep}</span>
                <span style="color:#A0AEC0;">{label}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px;
                    padding:22px 24px; box-shadow:0 1px 4px rgba(0,0,0,0.05);">
            <div style="font-size:11px; font-weight:700; color:#718096; text-transform:uppercase;
                        letter-spacing:0.08em; margin-bottom:14px;">Stack</div>
        """, unsafe_allow_html=True)
        for lbl, val in [("Version","2.0.0"),("Backend","FastAPI"),("AI Model","Gemini 2.5 Flash"),
                         ("Embeddings","all-MiniLM-L6-v2"),("Vector DB","ChromaDB"),("Database","MongoDB")]:
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center;
                        padding:8px 0; border-bottom:1px solid #EDF2F7; font-size:13px;">
                <span style="color:#718096;">{lbl}</span>
                <span style="color:#1a1a2e; font-weight:600; font-size:12.5px;">{val}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    init_session()
    sidebar()

    if not logged_in():
        page_auth()
        return

    _, mc, _ = st.columns([0.04, 9.92, 0.04])
    with mc:
        p = st.session_state.page
        if   p == "chat":      page_chat()
        elif p == "knowledge": page_knowledge()
        elif p == "history":   page_history()
        elif p == "settings":  page_settings()
        else:                  page_chat()


if __name__ == "__main__":
    main()