class OrchestratorAgent:
    def combine(self, typing_result, text_result, voice_result):
        t  = typing_result.get("score", 0)
        tx = text_result.get("score", 0)
        v  = voice_result.get("score", 0)
        final = round(t * 0.35 + tx * 0.40 + v * 0.25)
        if final < 30:   level = "Low"
        elif final < 60: level = "Moderate"
        else:            level = "High"
        return {
            "final_score": final,
            "level": level,
            "breakdown": {"typing": t, "text": tx, "voice": v},
        }