class EmotionEngine:
    """
    Comprehensive emotion detection based on:
    - Hoffman Institute Feelings List
    - Brené Brown's 87 Human Emotions (Atlas of the Heart)
    - ESL Forums List of Emotions
    All mapped into actionable emotion categories.
    """

    # ── KEYWORD GROUPS (phrases + words, all lowercase) ───────

    # CALM / ACCEPTING / OPEN
    CALM_KEYWORDS = [
        "calm", "peaceful", "serene", "content", "relaxed", "centered",
        "present", "patient", "trusting", "fulfilled", "at peace", "okay now",
        "feeling good", "all good", "doing well", "fine", "great", "wonderful",
        "happy", "joyful", "excited", "enthusiastic", "energized", "refreshed",
        "grateful", "thankful", "blessed", "inspired", "thrilled", "delighted",
        "satisfied", "renewed", "vibrant", "lively", "playful", "free",
        "awe", "amazed", "enchanted", "blissful"
    ]

    # STRESS / OVERWHELM / TENSE
    STRESS_KEYWORDS = [
        "stressed", "stress", "overwhelmed", "overwhelm", "burned out", "burnout",
        "burnt out", "exhausted from", "frazzled", "depleted", "worn out",
        "too much to handle", "can't keep up", "falling apart", "breaking point",
        "deadline", "under pressure", "too much pressure", "so much going on",
        "rattled", "shaken", "on edge", "can't breathe", "freaking out",
        "everything at once", "losing my mind", "going crazy with work",
        "tense", "tight", "restless from stress"
    ]

    # ANXIETY / FEAR / WORRY
    ANXIETY_KEYWORDS = [
        "anxious", "anxiety", "nervous", "scared", "worried", "worrying",
        "terrified", "afraid", "fear", "fearful", "panic", "panicking",
        "apprehensive", "dread", "dreading", "hesitant", "paralyzed",
        "what if", "overthinking", "can't stop thinking", "spiraling",
        "uneasy", "unsettled", "frightened", "on edge about",
        "impending doom", "something bad", "scared of", "nervous about",
        "avoidance", "avoiding because", "vulnerability", "fragile right now"
    ]

    # ANGER / ANNOYED / HOSTILE
    ANGER_KEYWORDS = [
        "so angry", "i'm furious", "furious", "rage", "outraged",
        "i hate this so much", "makes me so mad", "pissed off", "pissed",
        "i'm done with this", "fed up", "irate", "hostile",
        "contempt", "cynical about", "bitter about", "resentful",
        "vindictive", "agitated", "aggravated", "so annoyed",
        "i want to hurt", "i want to kill", "beat him up", "beat her up",
        "attack him", "attack her", "fight him", "fight her",
        "i could scream", "makes my blood boil"
    ]

    # FRUSTRATION / IRRITATION
    FRUSTRATION_KEYWORDS = [
        "frustrated", "frustrating", "so annoyed", "irritated", "irritating",
        "why won't this work", "doesn't work", "nothing is working",
        "can't believe this", "this is ridiculous", "so stupid",
        "keeps failing", "not working", "broken", "annoying",
        "exasperated", "grouchy", "moody", "on edge",
        "being bullied", "being harassed", "harassment", "bully",
        "disgruntled", "disturbed by", "edgy", "impatient"
    ]

    # SADNESS / GRIEF / DESPAIR
    SAD_KEYWORDS = [
        "sad", "sadness", "depressed", "depression", "lonely", "loneliness",
        "heartbroken", "heartbreak", "grief", "grieving", "lost someone",
        "miss him", "miss her", "miss them", "miss you", "missing",
        "hopeless", "hopelessness", "despair", "anguish", "sorrow",
        "melancholy", "gloomy", "forlorn", "despondent", "discouraged",
        "weary", "tearful", "crying", "want to cry", "feel like crying",
        "unhappy", "disappointed in life", "feel empty", "feel hollow",
        "feel alone", "no one cares", "nobody understands", "worthless",
        "feel worthless", "what's the point", "disconnected", "numb",
        "isolated", "withdrawn", "shut down", "feel invisible"
    ]

    # SHAME / EMBARRASSMENT / GUILT
    SHAME_KEYWORDS = [
        "ashamed", "shame", "embarrassed", "embarrassing", "humiliated",
        "humiliation", "mortified", "self-conscious", "i feel useless",
        "feel weak", "feel worthless", "guilty", "guilt", "regret",
        "remorse", "remorseful", "i'm sorry i", "i feel bad about",
        "i messed up badly", "i ruined", "i failed everyone",
        "so embarrassing", "can't face", "can't show my face"
    ]

    # LONELINESS / DISCONNECTION / SEARCHING FOR CONNECTION
    LONELY_KEYWORDS = [
        "lonely", "loneliness", "feel alone", "no friends", "no one to talk to",
        "nobody listens", "feel invisible", "left out", "don't belong",
        "not fitting in", "excluded", "disconnected from people",
        "no one understands me", "feel isolated", "nobody cares about me",
        "want someone to talk to", "miss having friends", "lost connection",
        "insecure around people", "can't connect with people"
    ]

    # SHYNESS / SOCIAL ANXIETY / INTROVERSION
    SHY_KEYWORDS = [
        "introvert", "introverted", "shy", "shyness", "socially awkward",
        "social anxiety", "awkward", "don't know how to talk",
        "scared to talk to", "nervous around people", "nervous around her",
        "nervous around him", "nervous around girls", "nervous around guys",
        "how to approach", "how to talk to a girl", "how to talk to a guy",
        "how to make friends", "how do i talk to", "hard to socialize",
        "can't start conversations", "don't know what to say",
        "fear of rejection", "scared of rejection", "talking to strangers",
        "meeting new people", "i freeze when", "go blank when talking"
    ]

    # FATIGUE / BURNOUT / EXHAUSTION
    FATIGUE_KEYWORDS = [
        "so tired", "exhausted", "no energy", "drained", "running on empty",
        "haven't slept", "can't sleep", "burnt out", "burned out",
        "can't focus", "brain fog", "lethargic", "listless", "sluggish",
        "fatigued", "weary", "sleepy", "drowsy", "too tired to",
        "too exhausted to", "barely functioning", "low energy",
        "depleted", "need rest", "need to rest", "need a break"
    ]

    # HOPEFUL / OPTIMISTIC
    HOPEFUL_KEYWORDS = [
        "hopeful", "optimistic", "encouraged", "expectant", "looking forward",
        "excited about the future", "things will get better", "i believe",
        "i think i can", "getting better", "improving", "progress",
        "motivated", "determined", "ready to try", "going to try"
    ]

    # CURIOUS / ENGAGED / EXPLORING
    CURIOUS_KEYWORDS = [
        "curious", "interested in", "want to learn", "want to know",
        "how does", "how do", "what is", "explain", "tell me about",
        "fascinated by", "intrigued", "wondering about", "want to understand",
        "help me with", "can you help", "how to", "what are"
    ]

    # CONFIDENT / POWERFUL / COURAGEOUS
    CONFIDENT_KEYWORDS = [
        "confident", "confidence", "brave", "courageous", "determined",
        "strong", "capable", "proud", "i can do this", "i will do this",
        "ready for", "prepared", "assured", "successful", "winning",
        "achieved", "accomplished", "crushed it", "nailed it"
    ]

    # CONFUSION / OVERWHELM (cognitive)
    CONFUSED_KEYWORDS = [
        "confused", "confusion", "don't understand", "don't get it",
        "lost", "what does this mean", "makes no sense", "unclear",
        "perplexed", "puzzled", "can you explain", "help me understand",
        "not sure", "unsure", "uncertain", "don't know what to do",
        "what should i do", "need help deciding", "can't decide"
    ]

    # LOVE / CONNECTION / RELATIONSHIP
    LOVE_KEYWORDS = [
        "in love", "i love", "love her", "love him", "love them",
        "relationship", "my partner", "my girlfriend", "my boyfriend",
        "my crush", "like her", "like him", "feelings for",
        "romantic", "romance", "date", "dating", "how to impress",
        "how to ask out", "want to be with", "caring about someone",
        "compassion for", "empathy", "affectionate"
    ]

    # GRIEF / LOSS (specific)
    GRIEF_KEYWORDS = [
        "someone died", "passed away", "lost my", "death of",
        "funeral", "grieving", "mourning", "can't get over losing",
        "still miss", "never coming back", "gone forever",
        "my mom died", "my dad died", "my friend died", "my pet died"
    ]

    # ── EMOTION → CATEGORY MAPPING ────────────────────────────
    # Maps detected raw emotion to final output emotion label

    EMOTION_MAP = {
        "calm":       "calm",
        "stress":     "stress",
        "anxiety":    "anxiety",
        "anger":      "anger",
        "frustration":"frustration",
        "sad":        "sad",
        "shame":      "shame",
        "lonely":     "lonely",
        "shy":        "anxiety",       # shy → handled as social anxiety
        "fatigue":    "fatigue",
        "hopeful":    "hopeful",
        "curious":    "calm",          # curious → calm but engaged
        "confident":  "confident",
        "confused":   "confused",
        "love":       "calm",          # love/relationship → warm calm
        "grief":      "grief",
    }

    def _score_all(self, text: str) -> dict:
        t = text.lower()

        def match_score(keywords, weight=10):
            return sum(weight for w in keywords if w in t)

        return {
            "calm":        match_score(self.CALM_KEYWORDS,       weight=8),
            "stress":      match_score(self.STRESS_KEYWORDS,     weight=12),
            "anxiety":     match_score(self.ANXIETY_KEYWORDS,    weight=12),
            "anger":       match_score(self.ANGER_KEYWORDS,      weight=15),
            "frustration": match_score(self.FRUSTRATION_KEYWORDS,weight=11),
            "sad":         match_score(self.SAD_KEYWORDS,        weight=12),
            "shame":       match_score(self.SHAME_KEYWORDS,      weight=12),
            "lonely":      match_score(self.LONELY_KEYWORDS,     weight=12),
            "shy":         match_score(self.SHY_KEYWORDS,        weight=12),
            "fatigue":     match_score(self.FATIGUE_KEYWORDS,    weight=10),
            "hopeful":     match_score(self.HOPEFUL_KEYWORDS,    weight=8),
            "curious":     match_score(self.CURIOUS_KEYWORDS,    weight=6),
            "confident":   match_score(self.CONFIDENT_KEYWORDS,  weight=8),
            "confused":    match_score(self.CONFUSED_KEYWORDS,   weight=9),
            "love":        match_score(self.LOVE_KEYWORDS,       weight=8),
            "grief":       match_score(self.GRIEF_KEYWORDS,      weight=14),
        }

    def classify(self, typing_score, text_score, voice_score,
                 trend="stable", text_length=0, raw_text=""):

        # Very short input = calm
        if text_length < 4:
            return {
                "emotion": "calm", "intensity": 5,
                "escalating": False, "trend": trend,
                "intervention_needed": False,
            }

        # Reduced agent scores weight — keywords drive detection
        base_avg = typing_score * 0.20 + text_score * 0.25 + voice_score * 0.10

        scores = self._score_all(raw_text)

        # Merge shy into anxiety
        scores["anxiety"] += scores.pop("shy", 0)
        # Merge love into calm
        scores["calm"] += scores.pop("love", 0) * 0.5
        # Merge curious into calm
        scores["calm"] += scores.pop("curious", 0) * 0.5
        # Merge hopeful into calm
        scores["calm"] += scores.pop("hopeful", 0) * 0.5
        # Merge confident into calm
        scores["calm"] += scores.pop("confident", 0) * 0.5

        # Add base_avg to distress emotions only
        for em in ["stress", "anxiety", "anger", "frustration", "sad", "fatigue"]:
            scores[em] += base_avg * 0.3

        # Pick highest scoring emotion
        best_emotion = max(scores, key=scores.get)
        best_score   = scores[best_emotion]

        # If best score is too low → calm or mild_stress
        if best_score < 8:
            emotion = "calm"
            final_intensity = max(5, round(base_avg))
        elif best_score < 14 and best_emotion == "calm":
            emotion = "calm"
            final_intensity = round(best_score)
        elif best_emotion == "calm" and base_avg > 15:
            emotion = "mild_stress"
            final_intensity = round(base_avg)
        else:
            emotion = self.EMOTION_MAP.get(best_emotion, best_emotion)
            final_intensity = min(100, round(best_score + base_avg * 0.2))

        escalating = trend == "rising" and final_intensity > 55

        return {
            "emotion": emotion,
            "intensity": final_intensity,
            "escalating": escalating,
            "trend": trend,
            "intervention_needed": escalating or final_intensity > 78,
        }

    def get_trend(self, history):
        if len(history) < 3:
            return "stable"
        recent = history[-3:]
        if recent[-1] > recent[0] + 8:
            return "rising"
        elif recent[-1] < recent[0] - 8:
            return "falling"
        return "stable"