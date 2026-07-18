"""
Emotion analysis service using DistilRoBERTa.
Model: j-hartmann/emotion-english-distilroberta-base
Emotions: anger, disgust, fear, joy, neutral, sadness, surprise
"""

from transformers import pipeline

# Load the model once at startup
emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None,  # Return all 7 emotion scores
)

# Actionable recommendations for each detected emotion
EMOTION_RECOMMENDATIONS = {
    "joy": "Keep nurturing what brings you happiness! Consider sharing your good energy with someone today.",
    "sadness": "It's okay to feel sad. Try a short walk, listen to comforting music, or reach out to a friend.",
    "anger": "Take a few deep breaths. Physical activity or journaling more can help process these feelings.",
    "fear": "Acknowledge your fear — it's a natural response. Grounding exercises or talking to someone can help.",
    "surprise": "Unexpected moments can be powerful. Reflect on what surprised you and why.",
    "disgust": "Strong reactions reveal our values. Consider what boundaries might need attention.",
    "neutral": "A balanced state of mind. This is a great time for planning or creative thinking.",
}


def detect_emotion(text: str):
    """Original function — returns (emotion, confidence) tuple.
    Preserved for backward compatibility."""
    result = emotion_classifier(text)[0]
    sorted_results = sorted(result, key=lambda x: x["score"], reverse=True)
    emotion = sorted_results[0]["label"]
    confidence = sorted_results[0]["score"]
    return emotion, confidence


def analyze_emotion(text: str) -> dict:
    """Enhanced analysis returning full emotion breakdown.

    Returns:
        dict with primary_emotion, confidence, secondary_emotion,
        secondary_confidence, all_emotions, and recommendation.
    """
    result = emotion_classifier(text)[0]
    sorted_results = sorted(result, key=lambda x: x["score"], reverse=True)

    primary = sorted_results[0]
    secondary = sorted_results[1]

    return {
        "primary_emotion": primary["label"],
        "confidence": round(primary["score"], 4),
        "secondary_emotion": secondary["label"],
        "secondary_confidence": round(secondary["score"], 4),
        "all_emotions": {r["label"]: round(r["score"], 4) for r in sorted_results},
        "recommendation": EMOTION_RECOMMENDATIONS.get(primary["label"], ""),
    }