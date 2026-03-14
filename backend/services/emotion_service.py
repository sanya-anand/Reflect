from transformers import pipeline

emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base"
)

def detect_emotion(text: str):

    result = emotion_classifier(text)[0]

    emotion = result["label"]
    confidence = result["score"]

    return emotion, confidence