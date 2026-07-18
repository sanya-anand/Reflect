"""Service for generating AI-like programmatic insights from journal data."""

from typing import List, Dict, Any
from datetime import datetime, timedelta
from collections import defaultdict
from models.journal import JournalEntry


def generate_insights(entries: List[JournalEntry]) -> List[Dict[str, str]]:
    """Generate meaningful insights based on user's journal entries."""
    if not entries:
        return [{"type": "info", "message": "Write more journals to unlock insights!"}]

    insights = []
    
    # Analyze entry length vs emotion
    insights.extend(_analyze_length_vs_emotion(entries))
    
    # Analyze mood comparison (this week vs last week)
    insights.extend(_analyze_weekly_mood_shift(entries))
    
    # Analyze weekday vs weekend
    insights.extend(_analyze_weekday_vs_weekend(entries))
    
    # Analyze writing time (if time of day was tracked, but we can do it by created_at)
    insights.extend(_analyze_writing_time(entries))

    # If not enough data, provide a generic one
    if not insights:
        insights.append({
            "type": "info",
            "message": "Keep journaling! The more you write, the better insights we can provide."
        })

    return insights


def _analyze_length_vs_emotion(entries: List[JournalEntry]) -> List[Dict[str, str]]:
    insights = []
    emotion_lengths = defaultdict(list)
    
    for entry in entries:
        if entry.emotion:
            words = len(entry.content.split())
            emotion_lengths[entry.emotion].append(words)
            
    avg_lengths = {emo: sum(lengths)/len(lengths) for emo, lengths in emotion_lengths.items() if len(lengths) > 1}
    
    if avg_lengths:
        longest_emo = max(avg_lengths, key=avg_lengths.get)
        if avg_lengths[longest_emo] > 50: # Threshold for a meaningful insight
            insights.append({
                "type": "pattern",
                "message": f"You tend to write longer entries when you are feeling {longest_emo}."
            })
            
    return insights


def _analyze_weekly_mood_shift(entries: List[JournalEntry]) -> List[Dict[str, str]]:
    insights = []
    now = datetime.utcnow()
    this_week = [e for e in entries if (now - e.created_at).days <= 7]
    last_week = [e for e in entries if 7 < (now - e.created_at).days <= 14]
    
    if not this_week or not last_week:
        return insights
        
    this_week_emotions = [e.emotion for e in this_week if e.emotion]
    last_week_emotions = [e.emotion for e in last_week if e.emotion]
    
    positive_emotions = {"joy", "surprise"}
    negative_emotions = {"sadness", "anger", "fear", "disgust"}
    
    def get_positivity(emotions):
        if not emotions:
            return 0
        pos = sum(1 for e in emotions if e in positive_emotions)
        neg = sum(1 for e in emotions if e in negative_emotions)
        return pos - neg

    this_pos = get_positivity(this_week_emotions)
    last_pos = get_positivity(last_week_emotions)
    
    if this_pos > last_pos + 1:
        insights.append({
            "type": "positive",
            "message": "Your overall mood seems more positive this week compared to last week!"
        })
    elif this_pos < last_pos - 1:
        insights.append({
            "type": "support",
            "message": "It looks like this week has been a bit tougher than the last. Take care of yourself."
        })
        
    return insights


def _analyze_weekday_vs_weekend(entries: List[JournalEntry]) -> List[Dict[str, str]]:
    insights = []
    weekend_emotions = defaultdict(int)
    weekday_emotions = defaultdict(int)
    
    for entry in entries:
        if not entry.emotion:
            continue
        # 5 and 6 are Saturday and Sunday
        if entry.created_at.weekday() >= 5:
            weekend_emotions[entry.emotion] += 1
        else:
            weekday_emotions[entry.emotion] += 1
            
    if sum(weekend_emotions.values()) > 2 and sum(weekday_emotions.values()) > 2:
        top_weekend = max(weekend_emotions, key=weekend_emotions.get)
        top_weekday = max(weekday_emotions, key=weekday_emotions.get)
        
        if top_weekend != top_weekday:
            if top_weekday in ["anger", "sadness", "fear", "disgust"]:
                 insights.append({
                    "type": "observation",
                    "message": f"Stress appears higher on weekdays (dominant: {top_weekday}), but weekends bring more {top_weekend}."
                })
            elif top_weekend == "joy":
                insights.append({
                    "type": "observation",
                    "message": "You experience significantly more joy during the weekends!"
                })
                
    return insights


def _analyze_writing_time(entries: List[JournalEntry]) -> List[Dict[str, str]]:
    insights = []
    if len(entries) < 5:
        return insights
        
    morning = sum(1 for e in entries if 5 <= e.created_at.hour < 12)
    afternoon = sum(1 for e in entries if 12 <= e.created_at.hour < 17)
    evening = sum(1 for e in entries if 17 <= e.created_at.hour < 22)
    night = sum(1 for e in entries if e.created_at.hour >= 22 or e.created_at.hour < 5)
    
    times = {"morning": morning, "afternoon": afternoon, "evening": evening, "late night": night}
    favorite_time = max(times, key=times.get)
    
    # Only report if it's a strong preference (e.g., > 50% of entries)
    if times[favorite_time] > len(entries) * 0.5:
        insights.append({
            "type": "habit",
            "message": f"You are a {favorite_time} writer! You write most of your entries during this time."
        })
        
    return insights
