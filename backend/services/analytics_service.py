"""Service for calculating analytics from journal entries."""

from typing import List, Dict, Any
from datetime import datetime, timedelta
from collections import defaultdict
from models.journal import JournalEntry


def get_basic_stats(entries: List[JournalEntry]) -> Dict[str, Any]:
    """Calculate total entries, average length, and most common emotion."""
    if not entries:
        return {
            "total_entries": 0,
            "average_length": 0,
            "most_common_emotion": None,
            "current_streak": 0,
            "longest_streak": 0
        }

    total = len(entries)
    total_words = sum(len(e.content.split()) for e in entries)
    avg_length = total_words // total if total > 0 else 0

    emotion_counts = defaultdict(int)
    for e in entries:
        if e.emotion:
            emotion_counts[e.emotion] += 1

    most_common_emotion = None
    if emotion_counts:
        most_common_emotion = max(emotion_counts, key=emotion_counts.get)

    streaks = calculate_streaks(entries)

    return {
        "total_entries": total,
        "average_length": avg_length,
        "most_common_emotion": most_common_emotion,
        "current_streak": streaks["current_streak"],
        "longest_streak": streaks["longest_streak"]
    }


def calculate_streaks(entries: List[JournalEntry]) -> Dict[str, int]:
    """Calculate current and longest journaling streaks."""
    if not entries:
        return {"current_streak": 0, "longest_streak": 0}

    # Extract unique dates of entries
    dates = sorted(list(set([e.created_at.date() for e in entries])), reverse=True)
    
    current_streak = 0
    longest_streak = 0
    current_temp = 0
    
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)
    
    # Check if streak is active (entry today or yesterday)
    is_active = len(dates) > 0 and (dates[0] == today or dates[0] == yesterday)
    
    if is_active:
        current_streak = 1
        for i in range(len(dates) - 1):
            if (dates[i] - dates[i+1]).days == 1:
                current_streak += 1
            else:
                break
                
    # Calculate longest streak
    if len(dates) > 0:
        current_temp = 1
        longest_streak = 1
        for i in range(len(dates) - 1):
            if (dates[i] - dates[i+1]).days == 1:
                current_temp += 1
                longest_streak = max(longest_streak, current_temp)
            else:
                current_temp = 1
                
    return {
        "current_streak": current_streak,
        "longest_streak": longest_streak
    }


def get_emotion_trends(entries: List[JournalEntry], days: int = 7) -> Dict[str, Any]:
    """Calculate emotion trends over the specified number of days."""
    if not entries:
        return {}
        
    cutoff_date = datetime.utcnow().date() - timedelta(days=days)
    recent_entries = [e for e in entries if e.created_at.date() >= cutoff_date]
    
    # Group by date
    trends = defaultdict(lambda: defaultdict(int))
    
    for entry in recent_entries:
        date_str = entry.created_at.date().isoformat()
        if entry.emotion:
            trends[date_str][entry.emotion] += 1
            
    return dict(trends)


def get_calendar_heatmap(entries: List[JournalEntry]) -> List[Dict[str, Any]]:
    """Format data for a contribution calendar heatmap."""
    
    # Group by date
    daily_stats = defaultdict(lambda: {"count": 0, "emotions": defaultdict(int)})
    
    for entry in entries:
        date_str = entry.created_at.date().isoformat()
        daily_stats[date_str]["count"] += 1
        if entry.emotion:
            daily_stats[date_str]["emotions"][entry.emotion] += 1
            
    # Find dominant emotion for each day
    heatmap = []
    for date_str, stats in daily_stats.items():
        dominant_emotion = None
        if stats["emotions"]:
            dominant_emotion = max(stats["emotions"], key=stats["emotions"].get)
            
        heatmap.append({
            "date": date_str,
            "count": stats["count"],
            "dominant_emotion": dominant_emotion
        })
        
    return heatmap
