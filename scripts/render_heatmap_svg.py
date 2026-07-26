import os
import sys
import json
from datetime import datetime, timezone

PALETTE = [
    "#161b22",  # 0: no contributions (dark slate)
    "#0e4429",  # 1: low
    "#006d32",  # 2: medium-low
    "#26a641",  # 3: medium
    "#39d353",  # 4: high
    "#69f0a0",  # 5: neon top end
]

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def render_heatmap_svg(json_path="data/contributions.json", output_path="contrib-heatmap.svg"):
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        sys.exit(1)
        
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    days = data.get("days", [])
    total_cnt = data.get("total_contributions", 0)
    current_streak = data.get("current_streak", 0)
    longest_streak = data.get("longest_streak", 0)
    username = data.get("username", "ffzlucky7-coder")
    
    # Layout dimensions
    box_size = 11
    box_gap = 4
    col_width = box_size + box_gap
    row_height = box_size + box_gap
    
    margin_left = 42
    margin_top = 58
    
    num_weeks = (len(days) + 6) // 7
    width = margin_left + num_weeks * col_width + 24
    height = margin_top + 7 * row_height + 55
    
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
            animation: diagReveal 0.25s ease-out forwards;
        }
        
        @keyframes diagReveal {
            from {
                opacity: 0;
                transform: scale(0.3) translateY(-10px);
            }
            to {
                opacity: 1;
                transform: scale(1) translateY(0);
            }
        }
    ''')
    svg_parts.append('</style>')
    
    # Background Card
    svg_parts.append(f'<rect width="{width}" height="{height}" class="card-bg" />')
    
    # Header Window Controls
    svg_parts.append('<circle cx="20" cy="18" r="5.5" class="dot dot-red" />')
    svg_parts.append('<circle cx="36" cy="18" r="5.5" class="dot dot-yellow" />')
    svg_parts.append('<circle cx="52" cy="18" r="5.5" class="dot dot-green" />')
    svg_parts.append(f'<text x="{width // 2}" y="22" text-anchor="middle" class="font-mono header-title">{username}@github ~ contributions.sh</text>')
    svg_parts.append(f'<line x1="0" y1="36" x2="{width}" y2="36" stroke="#30363d" stroke-width="1" />')
    
    # Month Labels
    last_month = None
    for idx, day in enumerate(days):
        col = idx // 7
        row = idx % 7
        if row == 0:
            dt = datetime.strptime(day["date"], "%Y-%m-%d")
            month_name = MONTH_NAMES[dt.month - 1]
            if month_name != last_month:
                x_pos = margin_left + col * col_width
                svg_parts.append(f'<text x="{x_pos}" y="{margin_top - 10}" class="axis-label">{month_name}</text>')
                last_month = month_name
                
    # Day Labels (Mon, Wed, Fri)
    day_labels = [("Mon", 1), ("Wed", 3), ("Fri", 5)]
    for d_name, d_row in day_labels:
        y_pos = margin_top + d_row * row_height + 9
        svg_parts.append(f'<text x="14" y="{y_pos}" class="axis-label">{d_name}</text>')
        
    # Render Day Boxes with Diagonal Animation
    for idx, day in enumerate(days):
        col = idx // 7
        row = idx % 7
        
        x_pos = margin_left + col * col_width
        y_pos = margin_top + row * row_height
        
        level = min(day.get("level", 0), len(PALETTE) - 1)
        fill_color = PALETTE[level]
        
        # Calculate diagonal stagger delay based on col + row
        delay = round(0.1 + (col + row) * 0.015, 3)
        
        svg_parts.append(
            f'<rect x="{x_pos}" y="{y_pos}" width="{box_size}" height="{box_size}" '
            f'fill="{fill_color}" class="day-box" style="animation-delay: {delay}s;" />'
        )
        
    # Footer Stats & Legend
    footer_y = margin_top + 7 * row_height + 30
    
    # Left Stats Text
    svg_parts.append(f'<text x="24" y="{footer_y}" class="footer-text">')
    svg_parts.append(f'<tspan class="stat-highlight">{total_cnt:,}</tspan> contributions in the last year | ')
    svg_parts.append(f'Streak: <tspan class="stat-highlight">{current_streak}d</tspan> (Best: {longest_streak}d)')
    svg_parts.append('</text>')
    
    # Right Legend (Less -> More)
    legend_x_start = width - 180
    svg_parts.append(f'<text x="{legend_x_start - 36}" y="{footer_y}" class="axis-label">Less</text>')
    for l_idx, p_color in enumerate(PALETTE[:5]):
        lx = legend_x_start + l_idx * (box_size + 3)
        ly = footer_y - 10
        svg_parts.append(f'<rect x="{lx}" y="{ly}" width="{box_size}" height="{box_size}" fill="{p_color}" rx="2" ry="2" />')
    svg_parts.append(f'<text x="{legend_x_start + 5 * (box_size + 3) + 4}" y="{footer_y}" class="axis-label">More</text>')
    
    svg_parts.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))
    print(f"Heatmap SVG saved to {output_path}")

if __name__ == "__main__":
    json_p = sys.argv[1] if len(sys.argv) > 1 else "data/contributions.json"
    render_heatmap_svg(json_p, "contrib-heatmap.svg")
