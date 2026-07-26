import os
import sys
import json
import re
from datetime import datetime, timezone
import requests
from bs4 import BeautifulSoup

def fetch_contributions(username="ffzlucky7-coder", output_path="data/contributions.json"):
    url = f"https://github.com/users/{username}/contributions"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print(f"Fetching contribution data for {username}...")
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print(f"Error fetching contributions HTML: HTTP {res.status_code}")
        sys.exit(1)
        
    soup = BeautifulSoup(res.text, "html.parser")
    
    # Tooltips map element ID -> text
    tooltips = {t.get("for"): t.text.strip() for t in soup.find_all("tool-tip") if t.get("for")}
    
    # Days elements
    day_elems = soup.find_all(["td", "rect"], class_=lambda c: c and "ContributionCalendar-day" in c)
    
    days_data = []
    total_contributions = 0
    
    for day in day_elems:
        date_str = day.get("data-date")
        level_str = day.get("data-level", "0")
        day_id = day.get("id")
        
        if not date_str:
            continue
            
        level = int(level_str) if level_str.isdigit() else 0
        tooltip_text = tooltips.get(day_id, "")
        
        # Parse count from tooltip text e.g. "4 contributions on January 10th." or "No contributions on..."
        count = 0
        match = re.search(r"(\d+)\s+contribution", tooltip_text, re.IGNORECASE)
        if match:
            count = int(match.group(1))
        elif level > 0:
            count = level  # fallback approximation
            
        total_contributions += count
        days_data.append({
            "date": date_str,
            "level": level,
            "count": count,
            "tooltip": tooltip_text
        })
        
    # Sort days by date
    days_data.sort(key=lambda x: x["date"])
    
    # Calculate Streaks
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    best_day = {"date": None, "count": 0}
    
    for day in days_data:
        cnt = day["count"]
        if cnt > best_day["count"]:
            best_day = {"date": day["date"], "count": cnt}
            
        if cnt > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0
            
    # Calculate current streak backwards from today/latest
    for day in reversed(days_data):
        if day["count"] > 0:
            current_streak += 1
        else:
            if current_streak == 0:
                continue
            else:
                break
                
    result = {
        "username": username,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "total_contributions": total_contributions,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day,
        "days": days_data
    }
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
        
    print(f"Contribution data successfully saved to {output_path}")
    print(f"Total Contributions: {total_contributions}, Current Streak: {current_streak}, Longest Streak: {longest_streak}")

if __name__ == "__main__":
    uname = sys.argv[1] if len(sys.argv) > 1 else "ffzlucky7-coder"
    fetch_contributions(uname)
