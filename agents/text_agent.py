from textblob import TextBlob

class TextAgent:
    def analyze(self, text):
        if not text or len(text.split()) < 2:
            return {"score": 10}
        blob = TextBlob(text)
        sentiment    = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        words   = text.split()
        avg_len = sum(len(w) for w in words) / len(words)
        score   = max(0, min(100,
            (1 - sentiment) * 35 +
            subjectivity * 30 +
            max(0, avg_len - 4) * 5
        ))
        return {
            "score":        round(score),
            "sentiment":    round(sentiment, 2),
            "subjectivity": round(subjectivity, 2),
        }