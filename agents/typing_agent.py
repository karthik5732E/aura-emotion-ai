import time

class TypingAgent:
    def __init__(self):
        self.reset()

    def record_keystroke(self):
        self.keystrokes.append(time.time())

    def record_backspace(self):
        self.backspace_count += 1
        self.record_keystroke()

    def analyze(self, text_length):
        if len(self.keystrokes) < 3:
            return {"score": 20}
        gaps = [
            self.keystrokes[i + 1] - self.keystrokes[i]
            for i in range(len(self.keystrokes) - 1)
        ]
        avg_gap        = sum(gaps) / len(gaps)
        backspace_ratio = self.backspace_count / max(text_length, 1)
        score = min(100, (backspace_ratio * 60) + (avg_gap * 25))
        return {
            "score":           round(score),
            "backspace_ratio": round(backspace_ratio, 2),
            "avg_pause":       round(avg_gap, 3),
        }

    def reset(self):
        self.keystrokes     = []
        self.backspace_count = 0