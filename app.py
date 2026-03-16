"""
AI SECOND BRAIN — PREMIUM UI
Streamlit + Custom CSS + Groq. Maximum visual quality.
"""

import streamlit as st
import requests
import time
import os
from pathlib import Path

API = os.getenv("API_BASE", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="🧠 AI Second Brain",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════
# PREMIUM CSS — Deep Space Neural Theme
# ══════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
  --void:    #02040a;
  --deep:    #060d1a;
  --card:    #0a1628;
  --raised:  #0f1f35;
  --rim:     #152840;
  --glow:    #1a3356;
  --cyan:    #06d6f5;
  --violet:  #8b5cf6;
  --emerald: #10d98a;
  --amber:   #fbbf24;
  --rose:    #f43f5e;
  --t1:      #edf4ff;
  --t2:      #7fa8cc;
  --t3:      #3d6080;
  --head:    'Syne', sans-serif;
  --body:    'DM Sans', sans-serif;
  --mono:    'JetBrains Mono', monospace;
}

/* ── Reset ── */
*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp {
  background: var(--void) !important;
  font-family: var(--body) !important;
  color: var(--t1) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-track { background: var(--deep); }
::-webkit-scrollbar-thumb { background: var(--glow); border-radius: 2px; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #060d1a 0%, #04090f 100%) !important;
  border-right: 1px solid var(--rim) !important;
  box-shadow: 6px 0 40px rgba(0,0,0,0.7) !important;
}
section[data-testid="stSidebar"] > div { padding: 0 !important; }

/* ── Main ── */
.main .block-container {
  padding: 2rem 2.5rem !important;
  max-width: 100% !important;
}
.main { background: var(--void) !important; }

/* ── Headings ── */
h1, h2, h3 {
  font-family: 'Syne', sans-serif !important;
  letter-spacing: -0.5px !important;
}
h1 { font-size: 2.4rem !important; font-weight: 800 !important; }
h2 { font-size: 1.5rem !important; font-weight: 700 !important; }
h3 { font-size: 1.1rem !important; font-weight: 600 !important; }

/* ── Buttons ── */
.stButton > button {
  background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 10px !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 600 !important;
  font-size: 14px !important;
  padding: 10px 22px !important;
  letter-spacing: 0.3px !important;
  transition: all 0.25s cubic-bezier(.4,0,.2,1) !important;
  box-shadow: 0 4px 24px rgba(109,40,217,0.4) !important;
}
.stButton > button:hover {
  transform: translateY(-2px) scale(1.02) !important;
  box-shadow: 0 8px 32px rgba(109,40,217,0.6) !important;
}
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, #06d6f5 0%, #0891b2 100%) !important;
  box-shadow: 0 4px 24px rgba(6,214,245,0.35) !important;
}
.stButton > button[kind="primary"]:hover {
  box-shadow: 0 8px 32px rgba(6,214,245,0.55) !important;
}
.stButton > button[kind="secondary"] {
  background: linear-gradient(135deg, #1a3356 0%, #0f1f35 100%) !important;
  box-shadow: 0 2px 12px rgba(0,0,0,0.4) !important;
  border: 1px solid var(--glow) !important;
}

/* ── Text inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
  background: var(--card) !important;
  border: 1px solid var(--rim) !important;
  border-radius: 10px !important;
  color: var(--t1) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 14px !important;
  padding: 12px 16px !important;
  transition: border-color 0.2s !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
  border-color: var(--cyan) !important;
  box-shadow: 0 0 0 3px rgba(6,214,245,0.1) !important;
}

/* ── Chat input ── */
.stChatInput > div {
  background: var(--card) !important;
  border: 1px solid var(--rim) !important;
  border-radius: 14px !important;
  box-shadow: 0 4px 30px rgba(0,0,0,0.5) !important;
}
.stChatInput > div:focus-within {
  border-color: var(--cyan) !important;
  box-shadow: 0 0 0 3px rgba(6,214,245,0.1), 0 4px 30px rgba(0,0,0,0.5) !important;
}
.stChatInput textarea {
  background: transparent !important;
  color: var(--t1) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 15px !important;
}

/* ── Chat messages ── */
.stChatMessage {
  background: transparent !important;
  border: none !important;
  padding: 4px 0 !important;
}
[data-testid="stChatMessage"] {
  background: var(--card) !important;
  border: 1px solid var(--rim) !important;
  border-radius: 16px !important;
  padding: 16px 20px !important;
  margin-bottom: 12px !important;
  box-shadow: 0 4px 20px rgba(0,0,0,0.3) !important;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
  background: var(--raised) !important;
  border-color: var(--glow) !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
  background: var(--card) !important;
  border: 1px solid var(--rim) !important;
  border-radius: 12px !important;
  padding: 16px 18px !important;
  transition: all 0.2s !important;
}
[data-testid="stMetric"]:hover {
  border-color: var(--glow) !important;
  transform: translateY(-1px) !important;
}
[data-testid="stMetricValue"] {
  color: var(--cyan) !important;
  font-family: 'Syne', sans-serif !important;
  font-weight: 700 !important;
  font-size: 1.6rem !important;
}
[data-testid="stMetricLabel"] {
  color: var(--t2) !important;
  font-size: 11px !important;
  text-transform: uppercase !important;
  letter-spacing: 1.2px !important;
  font-family: 'JetBrains Mono', monospace !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--card) !important;
  border-radius: 12px !important;
  border: 1px solid var(--rim) !important;
  padding: 5px !important;
  gap: 3px !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  color: var(--t2) !important;
  border-radius: 8px !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 500 !important;
  font-size: 14px !important;
  padding: 9px 22px !important;
  border: none !important;
  transition: all 0.2s !important;
}
.stTabs [data-baseweb="tab"]:hover {
  color: var(--t1) !important;
  background: var(--raised) !important;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, #8b5cf6, #6d28d9) !important;
  color: #fff !important;
  box-shadow: 0 3px 14px rgba(109,40,217,0.45) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding: 0 !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
  background: var(--card) !important;
  border: 1px solid var(--rim) !important;
  border-radius: 10px !important;
  color: var(--t1) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 500 !important;
  padding: 12px 16px !important;
}
.streamlit-expanderContent {
  background: var(--deep) !important;
  border: 1px solid var(--rim) !important;
  border-top: none !important;
  border-radius: 0 0 10px 10px !important;
  padding: 14px 16px !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
  background: var(--card) !important;
  border: 2px dashed var(--glow) !important;
  border-radius: 14px !important;
  transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"]:hover {
  border-color: var(--cyan) !important;
}

/* ── Alerts ── */
.stSuccess {
  background: rgba(16,217,138,0.08) !important;
  border: 1px solid rgba(16,217,138,0.3) !important;
  border-radius: 10px !important;
  color: var(--emerald) !important;
}
.stInfo {
  background: rgba(6,214,245,0.07) !important;
  border: 1px solid rgba(6,214,245,0.25) !important;
  border-radius: 10px !important;
  color: var(--t2) !important;
}
.stError {
  background: rgba(244,63,94,0.08) !important;
  border: 1px solid rgba(244,63,94,0.3) !important;
  border-radius: 10px !important;
}
.stWarning {
  background: rgba(251,191,36,0.08) !important;
  border: 1px solid rgba(251,191,36,0.3) !important;
  border-radius: 10px !important;
}

/* ── Divider ── */
hr { border-color: var(--rim) !important; margin: 1.2rem 0 !important; }

/* ── Selectbox ── */
.stSelectbox > div > div {
  background: var(--card) !important;
  border: 1px solid var(--rim) !important;
  border-radius: 10px !important;
  color: var(--t1) !important;
}

/* ── Caption / small text ── */
.stCaption {
  color: var(--t3) !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 11px !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Animations ── */
@keyframes pulse-dot { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.5;transform:scale(0.85)} }
@keyframes fade-in   { from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:translateY(0)} }
@keyframes shimmer   { 0%{background-position:-200% 0} 100%{background-position:200% 0} }

.fade-in { animation: fade-in 0.4s ease forwards; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
# API HELPERS
# ══════════════════════════════════════════════════════════════════════════

def api_get(path, timeout=20):
    try:
        r = requests.get(API + path, timeout=timeout)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None

def api_post(path, payload=None, files=None, timeout=90):
    try:
        r = requests.post(API + path, files=files, timeout=timeout) if files \
            else requests.post(API + path, json=payload, timeout=timeout)
        return r.json() if r.status_code in [200, 201] else None
    except Exception:
        return None

def api_delete(path, timeout=15):
    try:
        r = requests.delete(API + path, timeout=timeout)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None

# ══════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════

for k, v in {"messages": [], "last_sources": []}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════

with st.sidebar:

    # ── Branding ───────────────────────────────────────────────────────
    st.markdown("""
    <div style="padding:32px 20px 8px;text-align:center;">
      <div style="font-size:64px;line-height:1;margin-bottom:12px;
                  filter:drop-shadow(0 0 20px rgba(6,214,245,0.6));">🧠</div>
      <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:18px;
                  background:linear-gradient(135deg,#06d6f5,#8b5cf6);
                  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                  letter-spacing:-0.3px;">AI SECOND BRAIN</div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:9px;
                  color:#3d6080;letter-spacing:2.5px;text-transform:uppercase;
                  margin-top:5px;">Knowledge Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── Status ─────────────────────────────────────────────────────────
    health = api_get("/health")
    if health:
        docs_n = health.get("documents", 0)
        chat_n = health.get("conversations", 0)
        st.markdown("""
        <div style="margin:0 4px 16px;padding:12px 14px;
                    background:#0a1628;border:1px solid #152840;
                    border-radius:12px;display:flex;align-items:center;gap:10px;">
          <div style="width:9px;height:9px;border-radius:50%;background:#10d98a;
                      box-shadow:0 0 10px #10d98a;
                      animation:pulse-dot 2s infinite;flex-shrink:0;"></div>
          <span style="font-family:'JetBrains Mono',monospace;font-size:11px;
                       color:#10d98a;font-weight:600;letter-spacing:0.5px;">ONLINE</span>
          <span style="font-family:'JetBrains Mono',monospace;font-size:10px;
                       color:#3d6080;margin-left:auto;">llama-3.3-70b</span>
        </div>
        """, unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        col1.metric("📁 Docs",   docs_n)
        col2.metric("💬 Chats",  chat_n)
    else:
        st.markdown("""
        <div style="margin:0 4px 16px;padding:12px 14px;
                    background:#0a1628;border:1px solid #152840;
                    border-radius:12px;display:flex;align-items:center;gap:10px;">
          <div style="width:9px;height:9px;border-radius:50%;background:#f43f5e;
                      box-shadow:0 0 10px #f43f5e;flex-shrink:0;"></div>
          <span style="font-family:'JetBrains Mono',monospace;font-size:11px;
                       color:#f43f5e;font-weight:600;">OFFLINE</span>
        </div>
        """, unsafe_allow_html=True)
        st.error("Run: `python main.py`")

    st.divider()

    # ── Upload ─────────────────────────────────────────────────────────
    st.markdown("""
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;padding:0 2px;">
      <span style="font-size:18px;">📤</span>
      <span style="font-family:'Syne',sans-serif;font-weight:700;
                   font-size:14px;color:#edf4ff;">Upload Knowledge</span>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Files",
        type=["pdf","docx","txt","md","csv"],
        label_visibility="collapsed",
    )

    if uploaded:
        ext   = Path(uploaded.name).suffix.lower()
        icons = {".pdf":"📕",".docx":"📘",".txt":"📄",".md":"📝",".csv":"📊"}
        ficon = icons.get(ext, "📄")
        fname = uploaded.name[:28] + "…" if len(uploaded.name) > 30 else uploaded.name
        st.markdown(
            "<div style='background:#0a1628;border:1px solid #152840;border-radius:8px;"
            "padding:8px 12px;margin:8px 0;display:flex;align-items:center;gap:8px;'>"
            "<span style='font-size:16px;'>" + ficon + "</span>"
            "<span style='font-size:12px;color:#7fa8cc;font-family:DM Sans,sans-serif;'>"
            + fname + "</span></div>",
            unsafe_allow_html=True,
        )
        if st.button("⚡  Upload & Index", use_container_width=True, type="primary"):
            with st.spinner("📖 Reading document…"):
                files  = {"file": (uploaded.name, uploaded.getvalue(),
                                   uploaded.type or "application/octet-stream")}
                result = api_post("/upload", files=files)
            if result:
                st.success("✅  Indexed " + str(result.get("word_count",0)) + " words!")
                summary = result.get("summary","")
                if summary:
                    st.info("📋  " + summary[:140] + "…")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌  Upload failed.")

    st.divider()

    # ── Library ────────────────────────────────────────────────────────
    st.markdown("""
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;padding:0 2px;">
      <span style="font-size:18px;">📚</span>
      <span style="font-family:'Syne',sans-serif;font-weight:700;
                   font-size:14px;color:#edf4ff;">Knowledge Library</span>
    </div>
    """, unsafe_allow_html=True)

    docs = api_get("/documents") or []

    if not docs:
        st.markdown("""
        <div style="background:#0a1628;border:1px dashed #152840;border-radius:12px;
                    padding:24px 16px;text-align:center;">
          <div style="font-size:32px;margin-bottom:8px;opacity:0.5;">📭</div>
          <p style="color:#3d6080;font-size:12px;margin:0;
                    font-family:DM Sans,sans-serif;">No documents yet</p>
          <p style="color:#1a3356;font-size:11px;margin:4px 0 0;">
            Upload to start learning
          </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        ext_icons = {".pdf":"📕",".docx":"📘",".txt":"📄",".md":"📝",".csv":"📊"}
        for doc in docs:
            ext  = Path(doc["filename"]).suffix.lower()
            icon = ext_icons.get(ext, "📄")
            name = doc["filename"]
            wc   = str(doc.get("word_count", 0))
            sz   = str(round(doc.get("size",0)/1024,1))

            st.markdown(
                "<div style='background:#0a1628;border:1px solid #152840;"
                "border-radius:10px;padding:10px 12px;margin-bottom:8px;'>"
                "<div style='display:flex;align-items:center;gap:8px;'>"
                "<span style='font-size:20px;'>" + icon + "</span>"
                "<div style='flex:1;min-width:0;'>"
                "<p style='font-size:12px;font-weight:600;color:#edf4ff;margin:0;"
                "overflow:hidden;text-overflow:ellipsis;white-space:nowrap;"
                "font-family:DM Sans,sans-serif;'>" + name + "</p>"
                "<p style='font-size:10px;color:#3d6080;margin:2px 0 0;"
                "font-family:JetBrains Mono,monospace;'>"
                + wc + " words · " + sz + " KB</p>"
                "</div></div></div>",
                unsafe_allow_html=True,
            )
            with st.expander("Details", expanded=False):
                summary = doc.get("summary","")
                if summary:
                    st.caption(summary[:200])
                if st.button("🗑️ Delete", key="del_"+doc["id"], use_container_width=True):
                    if api_delete("/documents/"+doc["id"]):
                        st.rerun()

    st.divider()

    # ── API Key ────────────────────────────────────────────────────────
    st.markdown("""
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;padding:0 2px;">
      <span style="font-size:18px;">🔑</span>
      <span style="font-family:'Syne',sans-serif;font-weight:700;
                   font-size:14px;color:#edf4ff;">Groq API Key</span>
    </div>
    """, unsafe_allow_html=True)

    key_val = st.text_input("key", type="password",
                             placeholder="gsk_…", label_visibility="collapsed")
    if key_val:
        os.environ["GROQ_API_KEY"] = key_val
        st.success("✅  Key saved")
    st.markdown(
        "<p style='font-size:10px;color:#3d6080;font-family:JetBrains Mono,monospace;"
        "margin:4px 0 0;'>console.groq.com — free tier</p>",
        unsafe_allow_html=True,
    )
    st.divider()

    if st.button("🗑️  Clear All Data", use_container_width=True, type="secondary"):
        if api_delete("/clear"):
            st.session_state.messages = []
            st.session_state.last_sources = []
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════════════════════════════════════════

# ── Hero header ────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding:8px 0 28px;">
  <div style="display:flex;align-items:flex-start;justify-content:space-between;
              flex-wrap:wrap;gap:16px;">
    <div>
      <h1 style="font-family:'Syne',sans-serif;font-weight:800;font-size:2.6rem;
                 background:linear-gradient(135deg,#fff 0%,#06d6f5 45%,#8b5cf6 100%);
                 -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                 letter-spacing:-1.5px;margin:0;line-height:1.1;">
        AI Second Brain
      </h1>
      <p style="color:#3d6080;font-size:14px;margin:8px 0 0;
                font-family:'DM Sans',sans-serif;letter-spacing:0.2px;">
        Upload anything you learn — I remember, connect, and explain knowledge across all documents
      </p>
    </div>
    <div style="display:flex;gap:10px;flex-wrap:wrap;">
      <div style="background:#0a1628;border:1px solid #152840;border-radius:12px;
                  padding:10px 16px;text-align:center;min-width:72px;">
        <div style="font-size:22px;">🔮</div>
        <div style="font-size:9px;color:#3d6080;font-family:'JetBrains Mono',monospace;
                    text-transform:uppercase;letter-spacing:1px;margin-top:3px;">Groq AI</div>
      </div>
      <div style="background:#0a1628;border:1px solid #152840;border-radius:12px;
                  padding:10px 16px;text-align:center;min-width:72px;">
        <div style="font-size:22px;">📚</div>
        <div style="font-size:9px;color:#3d6080;font-family:'JetBrains Mono',monospace;
                    text-transform:uppercase;letter-spacing:1px;margin-top:3px;">128K ctx</div>
      </div>
      <div style="background:#0a1628;border:1px solid #152840;border-radius:12px;
                  padding:10px 16px;text-align:center;min-width:72px;">
        <div style="font-size:22px;">⚡</div>
        <div style="font-size:9px;color:#3d6080;font-family:'JetBrains Mono',monospace;
                    text-transform:uppercase;letter-spacing:1px;margin-top:3px;">Instant</div>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Metrics ────────────────────────────────────────────────────────────────
if health:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🧠  Model",      "Llama 3.3 · 70B")
    c2.metric("📁  Documents",  health.get("documents", 0))
    c3.metric("💬  Questions",  health.get("conversations", 0))
    c4.metric("🌐  Context",    "128 K tokens")

st.divider()

# ── Tabs ────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "💬   Chat with Brain",
    "📋   My Documents",
    "🕵️   History & Guide",
])

# ══════════════════════════════════════════════════════════════════════════
# TAB 1 — CHAT
# ══════════════════════════════════════════════════════════════════════════

with tab1:
    st.markdown("<br>", unsafe_allow_html=True)

    # Empty state suggestion cards
    if not st.session_state.messages:
        st.markdown("""
        <div style="margin-bottom:28px;">
          <p style="font-family:'Syne',sans-serif;font-weight:700;font-size:17px;
                    color:#edf4ff;margin:0 0 16px;">
            💡 Try asking your Second Brain…
          </p>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
        """, unsafe_allow_html=True)

        suggestions = [
            ("🔬", "How are statistics used in machine learning?",   "Cross-topic synthesis"),
            ("🗄️", "Explain SQL and Data Science connections",       "Concept linking"),
            ("🐍", "How does Python help in data pipelines?",        "Technical bridge"),
            ("🧩", "What themes connect all my documents?",          "Knowledge map"),
            ("📊", "Summarize everything I've uploaded",             "Full overview"),
            ("🔗", "What are the key concepts across my notes?",     "Pattern finder"),
        ]

        col1, col2 = st.columns(2)
        for i, (icon, q, tag) in enumerate(suggestions):
            card = (
                "<div style='background:#0a1628;border:1px solid #152840;"
                "border-radius:12px;padding:14px 16px;margin-bottom:2px;'>"
                "<div style='display:flex;align-items:flex-start;gap:10px;'>"
                "<span style='font-size:20px;flex-shrink:0;'>" + icon + "</span>"
                "<div>"
                "<p style='font-size:13px;font-weight:600;color:#edf4ff;margin:0 0 3px;"
                "font-family:DM Sans,sans-serif;line-height:1.4;'>" + q + "</p>"
                "<span style='font-size:10px;color:#3d6080;"
                "font-family:JetBrains Mono,monospace;'>" + tag + "</span>"
                "</div></div></div>"
            )
            if i % 2 == 0:
                col1.markdown(card, unsafe_allow_html=True)
            else:
                col2.markdown(card, unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

        if not docs:
            st.markdown("""
            <div style="background:rgba(6,214,245,0.05);border:1px solid rgba(6,214,245,0.2);
                        border-radius:12px;padding:16px 20px;margin-bottom:20px;">
              <p style="font-family:'DM Sans',sans-serif;font-size:14px;
                        color:#06d6f5;margin:0;">
                👋  <strong>Get started:</strong> Upload your PDFs, notes, or
                research papers from the sidebar, then ask questions here!
              </p>
            </div>
            """, unsafe_allow_html=True)

    # Chat messages
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(
                    "<span style='font-family:DM Sans,sans-serif;font-size:15px;"
                    "color:#edf4ff;'>" + msg["content"] + "</span>",
                    unsafe_allow_html=True,
                )
        else:
            with st.chat_message("assistant", avatar="🧠"):
                st.write(msg["content"])
                if msg.get("sources"):
                    src_list = "  ·  ".join("📄 " + s for s in msg["sources"])
                    st.markdown(
                        "<div style='margin-top:12px;padding:8px 14px;"
                        "background:#060d1a;border:1px solid #152840;"
                        "border-radius:8px;display:inline-block;'>"
                        "<span style='font-size:10px;color:#3d6080;"
                        "font-family:JetBrains Mono,monospace;letter-spacing:0.5px;"
                        "text-transform:uppercase;'>📎 Sources  </span>"
                        "<span style='font-size:11px;color:#7fa8cc;"
                        "font-family:DM Sans,sans-serif;'>" + src_list + "</span>"
                        "</div>",
                        unsafe_allow_html=True,
                    )

    # Chat input
    st.markdown("<br>", unsafe_allow_html=True)
    question = st.chat_input("Ask your Second Brain anything… (synthesizes ALL documents)")

    if question:
        with st.chat_message("user", avatar="👤"):
            st.markdown(
                "<span style='font-family:DM Sans,sans-serif;font-size:15px;"
                "color:#edf4ff;'>" + question + "</span>",
                unsafe_allow_html=True,
            )
        st.session_state.messages.append({"role": "user", "content": question})

        history = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages[:-1]
            if m["role"] in ["user", "assistant"]
        ]

        with st.chat_message("assistant", avatar="🧠"):
            with st.spinner("🧠  Synthesizing across all documents…"):
                result = api_post("/ask", {"question": question, "history": history[-6:]})

            if result:
                answer  = result.get("answer", "")
                sources = result.get("sources", [])
                st.write(answer)
                if sources:
                    src_list = "  ·  ".join("📄 " + s for s in sources)
                    st.markdown(
                        "<div style='margin-top:12px;padding:8px 14px;"
                        "background:#060d1a;border:1px solid #152840;"
                        "border-radius:8px;display:inline-block;'>"
                        "<span style='font-size:10px;color:#3d6080;"
                        "font-family:JetBrains Mono,monospace;letter-spacing:0.5px;"
                        "text-transform:uppercase;'>📎 Sources  </span>"
                        "<span style='font-size:11px;color:#7fa8cc;"
                        "font-family:DM Sans,sans-serif;'>" + src_list + "</span>"
                        "</div>",
                        unsafe_allow_html=True,
                    )
                st.session_state.messages.append({
                    "role": "assistant", "content": answer, "sources": sources
                })
            else:
                err = "❌ Error. Check backend is running and GROQ_API_KEY is set."
                st.error(err)
                st.session_state.messages.append({"role":"assistant","content":err,"sources":[]})

    if st.session_state.messages:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️  Clear Chat", type="secondary"):
            st.session_state.messages = []
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════
# TAB 2 — DOCUMENTS
# ══════════════════════════════════════════════════════════════════════════

with tab2:
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-bottom:20px;">
      <h2 style="font-family:'Syne',sans-serif;font-weight:700;font-size:20px;
                 color:#edf4ff;margin:0 0 4px;">📋  Knowledge Library</h2>
      <p style="color:#3d6080;font-size:13px;margin:0;
                font-family:'DM Sans',sans-serif;">
        All documents stored in your Second Brain
      </p>
    </div>
    """, unsafe_allow_html=True)

    docs = api_get("/documents") or []

    if not docs:
        st.markdown("""
        <div style="text-align:center;padding:60px 20px;background:#0a1628;
                    border:1px dashed #152840;border-radius:16px;">
          <div style="font-size:56px;margin-bottom:12px;opacity:0.4;">📭</div>
          <h3 style="font-family:'Syne',sans-serif;color:#edf4ff;
                     font-size:18px;margin:0 0 8px;">Empty Library</h3>
          <p style="color:#3d6080;font-size:13px;margin:0;">
            Upload PDFs, notes, research papers from the sidebar
          </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        tw = sum(d.get("word_count",0) for d in docs)
        ts = sum(d.get("size",0) for d in docs)
        c1,c2,c3 = st.columns(3)
        c1.metric("📁  Total Docs",  len(docs))
        c2.metric("📝  Total Words", f"{tw:,}")
        c3.metric("💾  Total Size",  str(round(ts/1024,1)) + " KB")
        st.markdown("<br>", unsafe_allow_html=True)

        ext_icons = {".pdf":"📕",".docx":"📘",".txt":"📄",".md":"📝",".csv":"📊"}
        for doc in docs:
            ext  = Path(doc["filename"]).suffix.lower()
            icon = ext_icons.get(ext, "📄")
            wc   = str(doc.get("word_count",0))
            sz   = str(round(doc.get("size",0)/1024,1))
            dt   = doc.get("uploaded_at","")[:10]
            name = doc["filename"]

            col_main, col_del = st.columns([6, 1])
            with col_main:
                with st.expander(icon + "  " + name + "  ·  " + wc + " words"):
                    st.markdown(
                        "<div style='display:flex;gap:12px;flex-wrap:wrap;margin-bottom:10px;'>"
                        "<span style='font-size:11px;color:#3d6080;"
                        "font-family:JetBrains Mono,monospace;background:#060d1a;"
                        "border:1px solid #152840;border-radius:6px;padding:3px 8px;'>"
                        "📅 " + dt + "</span>"
                        "<span style='font-size:11px;color:#3d6080;"
                        "font-family:JetBrains Mono,monospace;background:#060d1a;"
                        "border:1px solid #152840;border-radius:6px;padding:3px 8px;'>"
                        "💾 " + sz + " KB</span>"
                        "</div>",
                        unsafe_allow_html=True,
                    )
                    summary = doc.get("summary","")
                    if summary:
                        st.info("📋  " + summary[:250])

                    qkey = "qd_" + doc["id"]
                    quick = st.text_input(
                        "Ask",
                        placeholder="Ask something specific about this document…",
                        key=qkey, label_visibility="collapsed",
                    )
                    if quick:
                        with st.spinner("🧠  Thinking…"):
                            res = api_post("/ask", {"question": quick, "history": []})
                        if res:
                            st.success("🧠  " + res.get("answer","")[:500])

            with col_del:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🗑️", key="d2_"+doc["id"], help="Delete"):
                    if api_delete("/documents/"+doc["id"]):
                        st.rerun()

# ══════════════════════════════════════════════════════════════════════════
# TAB 3 — HISTORY & GUIDE
# ══════════════════════════════════════════════════════════════════════════

with tab3:
    st.markdown("<br>", unsafe_allow_html=True)

    col_hist, col_guide = st.columns([3, 2])

    with col_hist:
        st.markdown("""
        <h2 style="font-family:'Syne',sans-serif;font-weight:700;font-size:20px;
                   color:#edf4ff;margin:0 0 16px;">🕵️  Recent Conversations</h2>
        """, unsafe_allow_html=True)

        convs = api_get("/conversations") or []
        if not convs:
            st.info("💬  No conversations yet. Start chatting!")
        else:
            for conv in reversed(convs):
                ts  = conv.get("ts","")[:16].replace("T"," ")
                q   = conv.get("question","")
                a   = conv.get("answer","")
                src = conv.get("sources",[])
                with st.expander("❓  " + q[:70] + "  🕐 " + ts):
                    st.markdown(
                        "<p style='font-weight:600;color:#edf4ff;"
                        "font-family:DM Sans,sans-serif;margin:0 0 8px;'>"
                        + q + "</p>",
                        unsafe_allow_html=True,
                    )
                    st.divider()
                    st.write(a[:400] + ("…" if len(a) > 400 else ""))
                    if src:
                        st.caption("📎  " + " · ".join(src))

    with col_guide:
        st.markdown("""
        <h2 style="font-family:'Syne',sans-serif;font-weight:700;font-size:20px;
                   color:#edf4ff;margin:0 0 16px;">🔬  How It Works</h2>
        """, unsafe_allow_html=True)

        steps = [
            ("📤", "Upload",  "Add PDFs, notes, research papers, articles from the sidebar."),
            ("🧠", "AI Reads","Groq's 128K context window holds ALL your documents at once."),
            ("🔗", "Connect", "Ask any question — AI synthesizes knowledge across everything."),
        ]
        for icon, title, desc in steps:
            st.markdown(
                "<div style='background:#0a1628;border:1px solid #152840;"
                "border-radius:12px;padding:14px 16px;margin-bottom:10px;"
                "display:flex;gap:12px;align-items:flex-start;'>"
                "<div style='width:36px;height:36px;background:#060d1a;"
                "border:1px solid #1a3356;border-radius:8px;"
                "display:flex;align-items:center;justify-content:center;"
                "font-size:18px;flex-shrink:0;'>" + icon + "</div>"
                "<div>"
                "<p style='font-weight:700;font-family:Syne,sans-serif;"
                "color:#edf4ff;font-size:14px;margin:0 0 3px;'>" + title + "</p>"
                "<p style='color:#3d6080;font-size:12px;margin:0;"
                "font-family:DM Sans,sans-serif;line-height:1.5;'>" + desc + "</p>"
                "</div></div>",
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <h3 style="font-family:'Syne',sans-serif;font-weight:700;font-size:15px;
                   color:#edf4ff;margin:0 0 12px;">💡  Example Questions</h3>
        """, unsafe_allow_html=True)

        examples = [
            "How are statistics used in ML?",
            "Explain SQL and Data Science connections",
            "What concepts appear in all my documents?",
            "Summarize my entire knowledge base",
        ]
        for ex in examples:
            st.markdown(
                "<div style='background:#060d1a;border:1px solid #152840;"
                "border-radius:8px;padding:9px 14px;margin-bottom:6px;'>"
                "<span style='color:#06d6f5;font-size:11px;"
                "font-family:JetBrains Mono,monospace;'>→  </span>"
                "<span style='color:#7fa8cc;font-size:13px;"
                "font-family:DM Sans,sans-serif;'>" + ex + "</span>"
                "</div>",
                unsafe_allow_html=True,
            )

    st.divider()
    st.markdown("""
    <div style="text-align:center;padding:8px 0;">
      <span style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#1a3356;
                   letter-spacing:1px;">
        🧠 AI SECOND BRAIN  ·  ⚡ GROQ LLAMA-3.3-70B  ·  🚀 FASTAPI + STREAMLIT
      </span>
    </div>
    """, unsafe_allow_html=True)
