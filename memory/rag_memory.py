import chromadb
from datetime import datetime

class RAGMemory:
    def __init__(self):
        self.client = chromadb.EphemeralClient()
        self.col    = self.client.get_or_create_collection("aura_sessions")

    def save(self, emotion_result, user_text):
        sid = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        doc = (
            f"Emotion: {emotion_result['emotion']}, "
            f"intensity {emotion_result['intensity']}, "
            f"trend {emotion_result['trend']}. "
            f"User said: {user_text}"
        )
        self.col.add(
            documents=[doc],
            ids=[sid],
            metadatas=[{"intensity": emotion_result["intensity"]}],
        )

    def get_context(self, query, n=3):
        if self.col.count() == 0:
            return "No previous sessions yet."
        r = self.col.query(
            query_texts=[query],
            n_results=min(n, self.col.count()),
        )
        return "\n".join(r["documents"][0])