import os
import sys

def build_info_card(output_path="info-card.svg"):
    width = 500
    height = 420
    
    # Key-value rows to render in Neofetch format
    items = [
        ("OS", "Linux / Web Developer OS", "#58a6ff"),
        ("Host", "ffzlucky7-coder / MySelf", "#79c0ff"),
        ("Role", "Full-Stack Developer & Innovator 🚀", "#7ee787"),
        ("Uptime", "Building Cool Projects Daily ⚡", "#ffa657"),
        ("Languages", "Python, JavaScript, TypeScript, C++", "#d2a8ff"),
        ("Frontend", "React, HTML5, CSS3, TailwindCSS", "#58a6ff"),
        ("Backend", "Node.js, Express, REST APIs", "#7ee787"),
        ("Tools", "Git, GitHub Actions, VS Code, Docker", "#ff7b72"),
        ("Passions", "UI/UX Aesthetics & Automation 💻", "#ffa657"),
        ("Status", "Available for Projects & Tech Discussions 🤝", "#3fb950"),
    ]
    
    svg_parts = []
    svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg_parts.append('<style>')
    svg_parts.append('''
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600;700&amp;display=swap');
        .card-bg { fill: #0d1117; rx: 12px; ry: 12px; stroke: #30363d; stroke-width: 1px; }
        .font-mono { font-family: 'Fira Code', 'Courier New', monospace; }
        .header-title { font-size: 13px; fill: #8b949e; font-weight: 600; }
        .prompt-user { fill: #7ee787; font-weight: 700; font-size: 13px; }
        .prompt-host { fill: #58a6ff; font-weight: 700; font-size: 13px; }
        .prompt-symbol { fill: #c9d1d9; font-size: 13px; }
        
        .label { font-weight: 600; font-size: 12px; fill: #58a6ff; }
        .val { font-size: 12px; fill: #c9d1d9; }
        .sep { fill: #8b949e; font-size: 12px; }
        
        .dot { rx: 6px; ry: 6px; }
        .dot-red { fill: #ff5f56; }
        .dot-yellow { fill: #ffbd2e; }
        .dot-green { fill: #27c93f; }
        
        .row-anim {
            opacity: 0;
            animation: fadeInRow 0.3s ease-out forwards;
        }
        
        @keyframes fadeInRow {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .palette-box { rx: 4px; ry: 4px; }
    ''')
    svg_parts.append('</style>')
    
    # Background Card
    svg_parts.append(f'<rect width="{width}" height="{height}" class="card-bg" />')
    
    # Window Header Controls
    svg_parts.append('<circle cx="20" cy="18" r="5.5" class="dot dot-red" />')
    svg_parts.append('<circle cx="36" cy="18" r="5.5" class="dot dot-yellow" />')
    svg_parts.append('<circle cx="52" cy="18" r="5.5" class="dot dot-green" />')
    svg_parts.append(f'<text x="{width // 2}" y="22" text-anchor="middle" class="font-mono header-title">lucky@neofetch ~ stats</text>')
    svg_parts.append(f'<line x1="0" y1="36" x2="{width}" y2="36" stroke="#30363d" stroke-width="1" />')
    
    # Header Prompt: ffzlucky7-coder@github ~ neofetch
    svg_parts.append('<g class="row-anim" style="animation-delay: 0.1s;">')
    svg_parts.append('<text x="24" y="62" class="font-mono">')
    svg_parts.append('<tspan class="prompt-user">ffzlucky7-coder</tspan>')
    svg_parts.append('<tspan class="prompt-symbol">@</tspan>')
    svg_parts.append('<tspan class="prompt-host">github</tspan>')
    svg_parts.append('<tspan class="prompt-symbol">:~$ neofetch</tspan>')
    svg_parts.append('</text>')
    svg_parts.append(f'<line x1="24" y1="72" x2="{width - 24}" y2="72" stroke="#21262d" stroke-width="1.5" />')
    svg_parts.append('</g>')
    
    # Render Items
    start_y = 96
    row_height = 26
    
    for i, (key, val, key_color) in enumerate(items):
        y_pos = start_y + i * row_height
        delay = round(0.2 + i * 0.1, 2)
        
        svg_parts.append(f'<g class="row-anim" style="animation-delay: {delay}s;">')
        svg_parts.append(f'<text x="24" y="{y_pos}" class="font-mono">')
        svg_parts.append(f'<tspan class="label" style="fill: {key_color};">{key}</tspan>')
        svg_parts.append('<tspan class="sep"> &#10145; </tspan>')
        svg_parts.append(f'<tspan class="val">{val}</tspan>')
        svg_parts.append('</text>')
        svg_parts.append('</g>')
        
    # Color Palette Footer
    palette_y = start_y + len(items) * row_height + 12
    colors = ["#ff5f56", "#ffbd2e", "#27c93f", "#58a6ff", "#bc8cff", "#7ee787", "#ffa657", "#c9d1d9"]
    box_w = 24
    box_h = 14
    box_gap = 8
    start_x = 24
    
    delay = round(0.2 + len(items) * 0.1, 2)
    svg_parts.append(f'<g class="row-anim" style="animation-delay: {delay}s;">')
    svg_parts.append(f'<line x1="24" y1="{palette_y - 12}" x2="{width - 24}" y2="{palette_y - 12}" stroke="#21262d" stroke-width="1.5" />')
    for idx, c in enumerate(colors):
        x = start_x + idx * (box_w + box_gap)
        svg_parts.append(f'<rect x="{x}" y="{palette_y}" width="{box_w}" height="{box_h}" fill="{c}" class="palette-box" />')
    svg_parts.append('</g>')
    
    svg_parts.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))
    print(f"Info Card SVG saved to {output_path}")

if __name__ == "__main__":
    build_info_card("info-card.svg")
