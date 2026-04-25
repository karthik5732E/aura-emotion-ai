# 🧠 Aura — Emotion-Aware AI Agent

[![Hugging Face Spaces](https://img.shields.io/badge/🤗%20Hugging%20Face-Live%20Demo-blue)](https://huggingface.co/spaces/YOUR_USERNAME/aura-emotion-ai)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black)](https://github.com/YOUR_USERNAME/aura-emotion-ai)

> An emotionally intelligent AI assistant that detects your emotional state in real-time and adapts its personality, tone, and strategy to support you — built with multi-agent architecture, RAG memory, and LLM.

---

## 🎯 What It Does

Aura is not just a chatbot. It's a **multi-agent AI system** that:

- 🔍 **Detects 14+ emotions** in real-time from your text (stress, anxiety, grief, loneliness, shame, frustration, anger, fatigue, and more)
- 🎭 **Adapts its personality** — tone, language style, and response strategy change based on your emotional state
- 🧠 **Remembers past sessions** using RAG (Retrieval-Augmented Generation) with ChromaDB
- 📈 **Tracks emotional trends** across a session and detects escalation
- 💙 **Provides support resources** when distress is detected
- 💻 **Fully capable AI** — coding help, research, advice, creative writing, and more

---

## 🏗️ Architecture

```
User Input
    │
    ├── Typing Agent      → analyzes typing behavior
    ├── Text Agent        → NLP sentiment & keyword analysis (TextBlob)
    └── Voice Agent       → audio energy analysis (optional)
           │
           ▼
    Orchestrator Agent    → combines all scores
           │
           ▼
    Emotion Engine        → classifies into 14 emotion categories
           │
           ▼
    RAG Memory            → retrieves relevant past context (ChromaDB)
           │
           ▼
    Prompt Builder        → builds adaptive system prompt
           │
           ▼
    Groq LLM (Llama 3.3)  → generates emotionally adapted response
           │
           ▼
    Streamlit UI          → ChatGPT-style dark interface
```

---

## 🧠 Emotion Categories Detected

| Emotion | Trigger Example |
|---------|----------------|
| 😌 Calm | Normal questions, coding help |
| 😰 Stress | "overwhelmed", "deadline", "too much" |
| 😟 Anxiety | "nervous", "what if", "worried" |
| 😠 Anger | "furious", "so angry", "rage" |
| 😤 Frustration | "why won't this work", "so annoying" |
| 😢 Sad | "lonely", "heartbroken", "feel empty" |
| 💔 Grief | "someone died", "lost my", "passed away" |
| 😔 Shame | "ashamed", "guilty", "feel worthless" |
| 🥺 Lonely | "no one cares", "feel invisible" |
| 😴 Fatigue | "exhausted", "no energy", "burnt out" |
| 😕 Confused | "don't understand", "can you explain" |
| 💪 Confident | "I can do this", "proud", "accomplished" |
| 🌟 Hopeful | "looking forward", "getting better" |
| 😐 Mild Stress | Mid-range mixed signals |

---

## 🚀 Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | Groq API — Llama 3.3 70B |
| Memory | ChromaDB (RAG) |
| NLP | TextBlob |
| UI | Streamlit |
| Deployment | Hugging Face Spaces |
| Language | Python 3.11+ |

---

## 📁 Project Structure

```
aura-emotion-ai/
│
├── app.py                    ← Main Streamlit app
├── requirements.txt
├── .gitignore
│
├── agents/
│   ├── typing_agent.py       ← Typing behavior analysis
│   ├── text_agent.py         ← NLP sentiment analysis
│   ├── voice_agent.py        ← Audio analysis (optional)
│   ├── emotion_engine.py     ← Core emotion classifier
│   ├── orchestrator.py       ← Combines all agent scores
│   └── prompt_builder.py     ← Builds adaptive LLM prompt
│
└── memory/
    └── rag_memory.py         ← ChromaDB RAG memory
```

---

## ⚙️ Run Locally

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/aura-emotion-ai.git
cd aura-emotion-ai

# 2. Install dependencies
pip install -r requirements.txt
python -m textblob.download_corpora

# 3. Set your Groq API key
# Get free key at: console.groq.com
export GROQ_API_KEY=your_key_here   # Mac/Linux
set GROQ_API_KEY=your_key_here      # Windows

# 4. Run
streamlit run app.py
```

---

## 🌐 Live Demo

👉 **[Try Aura on Hugging Face](https://huggingface.co/spaces/YOUR_USERNAME/aura-emotion-ai)**

---

## 🔮 Future Upgrades (Roadmap)

- [ ] Voice input integration (real microphone analysis)
- [ ] Long-term persistent memory (across sessions)
- [ ] User authentication + personal emotion history
- [ ] Mobile app version
- [ ] Multilingual emotion detection

---

## 👨‍💻 Built By

Built as a multi-agent AI project combining emotion detection, RAG memory, and adaptive LLM prompting.

---

## 📄 License

MIT License — free to use and build on.