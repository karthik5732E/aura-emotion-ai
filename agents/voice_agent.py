import numpy as np

class VoiceAgent:
    def analyze_dummy(self):
        return {"score": 25}

    def analyze(self, audio, sr):
        try:
            import librosa
            rms = float(np.mean(librosa.feature.rms(y=audio)))
            zcr = float(np.mean(librosa.feature.zero_crossing_rate(audio)))
            score = min(100, rms * 400 + zcr * 80)
            return {"score": round(score)}
        except Exception:
            return {"score": 25}