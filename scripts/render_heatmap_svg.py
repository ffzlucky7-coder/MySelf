import os
import sys
import json
import random
from datetime import datetime, timedelta, timezone

PALETTE = [
    "#161b22",  # 0: no contributions
    "#0e4429",  # 1: low
    "#006d32",  # 2: medium-low
    "#26a641",  # 3: medium
    "#39d353",  # 4: high
    "#69f0a0",  # 5: neon top
]

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def generate_boosted_contributions(seed=42):
    random.seed(seed)
    days = []
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=364)
    
    total_cnt = 0
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    
    cur = start_date
    for _ in range(365):
        date_str = cur.strftime("%Y-%m-%d")
        # 82% chance of activity for a rich, vibrant graph
        is_active = random.random() < 0.82
        if is_active:
            level = random.choices([1, 2, 3, 4, 5], weights=[20, 30, 25, 15, 10])[0]
            count = level * random.randint(2, 5)
        else:
            level = 0
            count = 0
            
        total_cnt += count
        if count > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0
            
        days.append({
            "date": date_str,
            "level": level,
            "count": count
        })
        cur += timedelta(days=1)
        
    current_streak = temp_streak if temp_streak > 0 else random.randint(12, 35)
    
    return {
        "username": "ffzlucky7-coder",
        "total_contributions": total_cnt,
        "current_streak": current_streak,
        "longest_streak": max(longest_streak, 48),
        "days": days
    }

def render_heatmap_svg(json_path="data/contributions.json", output_path="contrib-heatmap.svg", boost=True):
    data = None
    if os.path.exists(json_path) and not boost:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
    if not data or boost or data.get("total_contributions", 0) < 50:
        data = generate_boosted_contributions()
        
    days = data.get("days", [])
    total_cnt = data.get("total_contributions", 1482)
    current_streak = data.get("current_streak", 28)
    longest_streak = data.get("longest_streak", 52)
    username = data.get("username", "ffzlucky7-coder")
    
    # Grid Layout
    box_size = 11
    box_gap = 4
    col_width = box_size + box_gap
    row_height = box_size + box_gap
    
    margin_left = 44
    margin_top = 62
    
    num_weeks = (len(days) + 6) // 7
    width = margin_left + num_weeks * col_width + 24
    height = margin_top + 7 * row_height + 58
    
    svg_parts = []
    svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg_parts.append('<style>')
    svg_parts.append('''
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600;700&amp;display=swap');
        .card-bg { fill: #0d1117; rx: 12px; ry: 12px; stroke: #30363d; stroke-width: 1px; }
        .font-mono { font-family: 'Fira Code', 'Courier New', monospace; }
        .header-title { font-size: 13px; fill: #8b949e; font-weight: 600; }
        .axis-label { font-size: 10px; fill: #7d8590; font-family: 'Fira Code', monospace; }
        .footer-text { font-size: 11px; fill: #8b949e; font-family: 'Fira Code', monospace; }
        .stat-highlight { fill: #39d353; font-weight: 700; }
        
        .dot { rx: 6px; ry: 6px; }
        .dot-red { fill: #ff5f56; }
        .dot-yellow { fill: #ffbd2e; }
        .dot-green { fill: #27c93f; }
        
        .day-box {
            rx: 2.5px;
            ry: 2.5px;
            opacity: 0;
            animation: diagReveal 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }
        
        @keyframes diagReveal {
            0% {
                opacity: 0;
                transform: scale(0.2) translateY(-12px);
            }
            60% {
                opacity: 0.8;
                transform: scale(1.1) translateY(2px);
            }
            100% {
                opacity: 1;
                transform: scale(1) translateY(0);
            }
        }
    ''')
    svg_parts.append('</style>')
    
    # Background Card
    svg_parts.append(f'<rect width="{width}" height="{height}" class="card-bg" />')
    
    # Header Controls
    svg_parts.append('<circle cx="20" cy="18" r="5.5" class="dot dot-red" />')
    svg_parts.append('<circle cx="36" cy="18" r="5.5" class="dot dot-yellow" />')
    svg_parts.append('<circle cx="52" cy="18" r="5.5" class="dot dot-green" />')
    svg_parts.append(f'<text x="{width // 2}" y="22" text-anchor="middle" class="font-mono header-title">{username}@github ~ contribution-graph.sh</text>')
    svg_parts.append(f'<line x1="0" y1="36" x2="{width}" y2="36" stroke="#30363d" stroke-width="1" />')
    
    # Month Labels with collision prevention (min 3 cols apart)
    last_month = None
    last_col = -10
    
    for idx, day in enumerate(days):
        col = idx // 7
        row = idx % 7
        if row == 0:
            dt = datetime.strptime(day["date"], "%Y-%m-%d")
            month_name = MONTH_NAMES[dt.month - 1]
            if month_name != last_month and (col - last_col) >= 3:
                x_pos = margin_left + col * col_width
                svg_parts.append(f'<text x="{x_pos}" y="{margin_top - 10}" class="axis-label">{month_name}</text>')
                last_month = month_name
                last_col = col
                
    # Day Labels
    day_labels = [("Mon", 1), ("Wed", 3), ("Fri", 5)]
    for d_name, d_row in day_labels:
        y_pos = margin_top + d_row * row_height + 9
        svg_parts.append(f'<text x="14" y="{y_pos}" class="axis-label">{d_name}</text>')
        
    # Render Day Boxes with Slower, Satisfying Staggered Animation
    for idx, day in enumerate(days):
        col = idx // 7
        row = idx % 7
        
        x_pos = margin_left + col * col_width
        y_pos = margin_top + row * row_height
        
        level = min(day.get("level", 0), len(PALETTE) - 1)
        fill_color = PALETTE[level]
        
        # Extended stagger timing (spread across 3.5 seconds)
        delay = round(0.2 + (col * 0.05 + row * 0.04), 3)
        
        svg_parts.append(
            f'<rect x="{x_pos}" y="{y_pos}" width="{box_size}" height="{box_size}" '
            f'fill="{fill_color}" class="day-box" style="animation-delay: {delay}s;" />'
        )
        
    # Footer Stats & Legend
    footer_y = margin_top + 7 * row_height + 32
    
    svg_parts.append(f'<text x="24" y="{footer_y}" class="footer-text">')
    svg_parts.append(f'<tspan class="stat-highlight">{total_cnt:,}</tspan> contributions in the last year | ')
    svg_parts.append(f'Current Streak: <tspan class="stat-highlight">{current_streak} days</tspan> (Best: {longest_streak} days)')
    svg_parts.append('</text>')
    
    legend_x_start = width - 180
    svg_parts.append(f'<text x="{legend_x_start - 36}" y="{footer_y}" class="axis-label">Less</text>')
    for l_idx, p_color in enumerate(PALETTE[:5]):
        lx = legend_x_start + l_idx * (box_size + 3)
        ly = footer_y - 10
        svg_parts.append(f'<rect x="{lx}" y="{ly}" width="{box_size}" height="{box_size}" fill="{p_color}" rx="2.5" ry="2.5" />')
    svg_parts.append(f'<text x="{legend_x_start + 5 * (box_size + 3) + 4}" y="{footer_y}" class="axis-label">More</text>')
    
    svg_parts.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))
    print(f"Enhanced Heatmap SVG saved to {output_path}")

if __name__ == "__main__":
    render_heatmap_svg("data/contributions.json", "contrib-heatmap.svg", boost=True)
