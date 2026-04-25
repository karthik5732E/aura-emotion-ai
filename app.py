import streamlit as st
from groq import Groq
import os
from agents.typing_agent import TypingAgent
from agents.text_agent import TextAgent
from agents.voice_agent import VoiceAgent
from agents.emotion_engine import EmotionEngine
from agents.orchestrator import OrchestratorAgent
from agents.prompt_builder import PromptBuilder
from memory.rag_memory import RAGMemory

# ── API Key ───────────────────────────────────────────────────
API_KEY = os.environ.get("GROQ_API_KEY", "")
client  = Groq(api_key=API_KEY)

st.set_page_config(
    page_title="Aura — Emotion-Aware AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: #0d0d0d !important; }
[data-testid="stAppViewContainer"],[data-testid="stMain"],
[data-testid="stMainBlockContainer"],section.main {
    background-color: #0d0d0d !important;
    color: #e8e8e8 !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stSidebar"],[data-testid="stSidebarContent"] {
    background-color: #111111 !important;
    border-right: 1px solid #1e1e1e !important;
}
header[data-testid="stHeader"] { background: transparent !important; display: none; }
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
[data-testid="stChatMessage"] {
    background: transparent !important; border: none !important;
    box-shadow: none !important; padding: 6px 0 !important;
    max-width: 900px !important; margin: 0 auto !important;
}
[data-testid="stChatMessageAvatarUser"],
[data-testid="stChatMessageAvatarAssistant"] { display: none !important; }
.user-bubble { display:flex; justify-content:flex-end; padding:4px 20px; margin:2px 0; }
.user-bubble .bubble {
    background:#2f2f2f; color:#ffffff;
    border-radius:20px 20px 5px 20px;
    padding:12px 18px; max-width:70%;
    font-size:15px; line-height:1.6;
    font-family:'Inter',sans-serif;
    white-space:pre-wrap; word-wrap:break-word;
}
.bot-bubble { display:flex; justify-content:flex-start; padding:4px 20px; margin:2px 0; gap:10px; align-items:flex-start; }
.bot-avatar {
    width:34px; height:34px; background:#1a1a3e;
    border:1.5px solid #7c6af7; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-size:16px; flex-shrink:0; margin-top:2px;
}
.bot-bubble .bubble {
    background:#16162a; color:#e2e2f5;
    border:1px solid #252545;
    border-radius:5px 20px 20px 20px;
    padding:12px 18px; max-width:75%;
    font-size:15px; line-height:1.65;
    font-family:'Inter',sans-serif;
    white-space:pre-wrap; word-wrap:break-word;
}
.helpline-card {
    background:#1a0a0a; border:1px solid #ef444433;
    border-radius:12px; padding:14px 18px; margin:8px 20px;
    font-family:'Inter',sans-serif;
}
.helpline-card .htitle { color:#ef4444; font-size:13px; font-weight:600; margin-bottom:6px; }
.helpline-card .hline  { color:#aaa; font-size:13px; line-height:1.8; }
[data-testid="stChatInput"] {
    background:#0d0d0d !important;
    border-top:1px solid #1e1e1e !important;
    padding:14px 24px !important;
}
[data-testid="stChatInput"] textarea {
    background:#1a1a1a !important; border:1px solid #2a2a2a !important;
    border-radius:14px !important; color:#e8e8e8 !important;
    font-size:15px !important; padding:12px 18px !important;
    font-family:'Inter',sans-serif !important; caret-color:#7c6af7 !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color:#7c6af7 !important;
    box-shadow:0 0 0 3px rgba(124,106,247,0.12) !important;
}
[data-testid="stChatInput"] textarea::placeholder { color:#3a3a3a !important; }
[data-testid="stMetric"] {
    background:#161616 !important; border-radius:10px !important;
    padding:10px 14px !important; border:1px solid #1e1e1e !important;
}
[data-testid="stMetricValue"] { color:#a78bfa !important; font-size:18px !important; font-weight:600 !important; }
[data-testid="stMetricLabel"] { color:#555 !important; font-size:10px !important; text-transform:uppercase !important; letter-spacing:0.8px !important; }
[data-testid="stButton"] button {
    background:#161616 !important; color:#888 !important;
    border:1px solid #252525 !important; border-radius:8px !important;
    font-family:'Inter',sans-serif !important; font-size:13px !important;
}
[data-testid="stButton"] button:hover {
    border-color:#7c6af7 !important; color:#a78bfa !important; background:#1a1a2e !important;
}
hr { border:none !important; border-top:1px solid #1e1e1e !important; margin:14px 0 !important; }
::-webkit-scrollbar { width:4px; }
::-webkit-scrollbar-track { background:transparent; }
::-webkit-scrollbar-thumb { background:#222; border-radius:4px; }
[data-testid="stMainBlockContainer"] { padding-top:0 !important; max-width:100% !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────
def init_state():
    defaults = {
        "messages": [],
        "intensity_history": [],
        "current_emotion": {
            "emotion": "calm", "intensity": 0,
            "escalating": False, "trend": "stable",
            "intervention_needed": False,
        },
        "typing_agent": TypingAgent(),
        "rag": RAGMemory(),
        "msg_count": 0,
        "mode": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

text_agent     = TextAgent()
voice_agent    = VoiceAgent()
emotion_engine = EmotionEngine()
orchestrator   = OrchestratorAgent()
prompt_builder = PromptBuilder()

# ── All emotion display data ──────────────────────────────────
EMOTION_EMOJI = {
    "calm":        "😌",
    "stress":      "😰",
    "anxiety":     "😟",
    "anger":       "😠",
    "frustration": "😤",
    "sad":         "😢",
    "grief":       "💔",
    "shame":       "😔",
    "lonely":      "🥺",
    "fatigue":     "😴",
    "confused":    "😕",
    "confident":   "💪",
    "hopeful":     "🌟",
    "mild_stress": "😐",
}
EMOTION_COLOR = {
    "calm":        "#22c55e",
    "stress":      "#ef4444",
    "anxiety":     "#f97316",
    "anger":       "#dc2626",
    "frustration": "#eab308",
    "sad":         "#60a5fa",
    "grief":       "#818cf8",
    "shame":       "#a855f7",
    "lonely":      "#38bdf8",
    "fatigue":     "#6b7280",
    "confused":    "#fb923c",
    "confident":   "#4ade80",
    "hopeful":     "#facc15",
    "mild_stress": "#a78bfa",
}

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:4px 0 16px'>
        <div style='font-size:20px;font-weight:600;color:#e8e8e8;letter-spacing:-0.3px'>🧠 Aura</div>
        <div style='color:#333;font-size:11px;margin-top:2px;letter-spacing:0.5px'>EMOTION-AWARE AI AGENT</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    em    = st.session_state.current_emotion
    emoji = EMOTION_EMOJI.get(em["emotion"], "🤔")
    color = EMOTION_COLOR.get(em["emotion"], "#a78bfa")
    label = em["emotion"].replace("_", " ").title()

    st.markdown(f"""
    <div style='text-align:center;padding:20px 12px;background:#141414;
                border-radius:14px;border:1px solid {color}35;margin-bottom:14px'>
        <div style='font-size:42px;margin-bottom:8px'>{emoji}</div>
        <div style='color:{color};font-size:18px;font-weight:600'>{label}</div>
        <div style='color:#333;font-size:10px;margin-top:3px;text-transform:uppercase;letter-spacing:0.8px'>
            Current Emotional State
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    c1.metric("Intensity", f"{em['intensity']}/100")
    c2.metric("Trend", em["trend"].title())

    st.markdown(f"""
    <div style='background:#141414;border-radius:8px;border:1px solid #1e1e1e;
                padding:9px 14px;margin-top:8px;display:flex;
                justify-content:space-between;align-items:center'>
        <span style='color:#444;font-size:10px;text-transform:uppercase;letter-spacing:0.6px'>Messages</span>
        <span style='color:#a78bfa;font-size:16px;font-weight:600'>{st.session_state.msg_count}</span>
    </div>
    """, unsafe_allow_html=True)

    if em["escalating"]:
        st.error("⚠️ Distress rising — Aura is adapting")

    if len(st.session_state.intensity_history) >= 2:
        st.markdown("""
        <p style='color:#333;font-size:10px;text-transform:uppercase;
                  letter-spacing:0.6px;margin:14px 0 6px'>Intensity Trend</p>
        """, unsafe_allow_html=True)
        st.line_chart(st.session_state.intensity_history, color="#7c6af7", height=100)

    st.divider()
    st.markdown("<p style='color:#444;font-size:10px;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:6px'>Quick Mode</p>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3)
    if col_a.button("💻 Code",     use_container_width=True): st.session_state.mode = "code";     st.rerun()
    if col_b.button("🔍 Research", use_container_width=True): st.session_state.mode = "research"; st.rerun()
    if col_c.button("💬 Chat",     use_container_width=True): st.session_state.mode = None;       st.rerun()

    current_mode = st.session_state.get("mode")
    if current_mode:
        mode_label = "💻 Code Helper" if current_mode == "code" else "🔍 Research Helper"
        st.markdown(f"<p style='color:#7c6af7;font-size:11px;text-align:center;margin-top:4px'>Active: {mode_label}</p>", unsafe_allow_html=True)

    st.divider()
    if st.button("🗑️  New Conversation", use_container_width=True):
        st.session_state.messages         = []
        st.session_state.intensity_history = []
        st.session_state.msg_count        = 0
        st.session_state.mode             = None
        st.session_state.typing_agent.reset()
        st.session_state.current_emotion  = {
            "emotion": "calm", "intensity": 0,
            "escalating": False, "trend": "stable", "intervention_needed": False,
        }
        st.rerun()

    st.markdown("""
    <p style='color:#1e1e1e;font-size:10px;text-align:center;margin-top:20px'>
        Groq · Llama 3.3 · ChromaDB RAG
    </p>""", unsafe_allow_html=True)

# ── Main chat area ────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div style='display:flex;flex-direction:column;align-items:center;
                justify-content:center;min-height:60vh;text-align:center;padding:40px 20px'>
        <div style='font-size:52px;margin-bottom:16px'>🧠</div>
        <h1 style='color:#e8e8e8;font-size:30px;font-weight:600;
                   letter-spacing:-0.8px;margin-bottom:10px;font-family:Inter,sans-serif'>
            Hi, I'm Aura
        </h1>
        <p style='color:#444;font-size:15px;line-height:1.7;max-width:460px;font-family:Inter,sans-serif'>
            I sense how you're feeling and adapt to support you fully.<br>
            Code, research, relationships, or just a conversation — I'm here.
        </p>
        <div style='display:flex;gap:10px;margin-top:28px;flex-wrap:wrap;justify-content:center'>
            <div style='background:#141414;border:1px solid #1e1e1e;border-radius:12px;padding:12px 18px;font-size:13px;color:#666;font-family:Inter,sans-serif'>💻 Help me debug code</div>
            <div style='background:#141414;border:1px solid #1e1e1e;border-radius:12px;padding:12px 18px;font-size:13px;color:#666;font-family:Inter,sans-serif'>🔍 Research any topic</div>
            <div style='background:#141414;border:1px solid #1e1e1e;border-radius:12px;padding:12px 18px;font-size:13px;color:#666;font-family:Inter,sans-serif'>😔 I need to vent</div>
            <div style='background:#141414;border:1px solid #1e1e1e;border-radius:12px;padding:12px 18px;font-size:13px;color:#666;font-family:Inter,sans-serif'>💬 Just talk to me</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Render chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble"><div class="bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-bubble"><div class="bot-avatar">🧠</div><div class="bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)

# ── Input handling ────────────────────────────────────────────
if user_input := st.chat_input("Message Aura..."):

    input_len = len(user_input)

    typing_result = st.session_state.typing_agent.analyze(input_len)
    text_result   = text_agent.analyze(user_input)
    voice_result  = voice_agent.analyze_dummy()
    orchestrator.combine(typing_result, text_result, voice_result)

    trend = emotion_engine.get_trend(st.session_state.intensity_history)
    emotion_result = emotion_engine.classify(
        typing_score=typing_result["score"],
        text_score=text_result["score"],
        voice_score=voice_result["score"],
        trend=trend,
        text_length=input_len,
        raw_text=user_input,
    )

    st.session_state.current_emotion = emotion_result
    st.session_state.intensity_history.append(emotion_result["intensity"])
    st.session_state.msg_count += 1

    st.session_state.rag.save(emotion_result, user_input)
    memory_ctx    = st.session_state.rag.get_context(user_input)
    system_prompt = prompt_builder.build(emotion_result, memory_ctx, mode=st.session_state.get("mode"))

    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="user-bubble"><div class="bubble">{user_input}</div></div>', unsafe_allow_html=True)

    # Show helpline if distressed
    helplines = prompt_builder.get_helplines(emotion_result["emotion"])
    if helplines and emotion_result["intervention_needed"]:
        lines_html = "".join([f"📞 <b>{name}</b>: {num}<br>" for name, num in helplines])
        st.markdown(f"""
        <div class="helpline-card">
            <div class="htitle">💙 Support is available</div>
            <div class="hline">{lines_html}</div>
        </div>
        """, unsafe_allow_html=True)

    # Call Groq
    with st.spinner(""):
        try:
            groq_messages = [{"role": "system", "content": system_prompt}]
            for m in st.session_state.messages:
                groq_messages.append({"role": m["role"], "content": m["content"]})

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=groq_messages,
                max_tokens=600,
                temperature=0.72,
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = f"⚠️ Error: {str(e)}"

    st.markdown(f'<div class="bot-bubble"><div class="bot-avatar">🧠</div><div class="bubble">{reply}</div></div>', unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.typing_agent.reset()
    st.rerun()