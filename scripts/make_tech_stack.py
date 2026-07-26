import os
import sys

def build_tech_stack_svg(output_path="tech-stack.svg"):
    width = 860
    height = 180
    
    # Skills with vibrant eye-catching gradient color stops
    skills = [
        ("🤖 Artificial Intelligence", "grad1"),
        ("⚡ AI Automation", "grad2"),
        ("🎬 Video Editing", "grad3"),
        ("📈 AI Ads & Marketing", "grad4"),
        ("🧠 LLMs & Prompts", "grad5"),
        ("🐍 Python & ML", "grad6"),
        ("🐙 Git & CI/CD", "grad7"),
    ]
    
    svg_parts = []
    svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    
    # Gradients & Filters
    svg_parts.append('<defs>')
    # Gradient 1: Pink Red Neon
    svg_parts.append('''
        <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#FF416C"/>
            <stop offset="100%" stop-color="#FF4B2B"/>
        </linearGradient>
        <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#8A2387"/>
            <stop offset="50%" stop-color="#E94057"/>
            <stop offset="100%" stop-color="#F27121"/>
        </linearGradient>
        <linearGradient id="grad3" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#00F2FE"/>
            <stop offset="100%" stop-color="#4FACFE"/>
        </linearGradient>
        <linearGradient id="grad4" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#FF8008"/>
            <stop offset="100%" stop-color="#FFC837"/>
        </linearGradient>
        <linearGradient id="grad5" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#B224EF"/>
            <stop offset="100%" stop-color="#7579FF"/>
        </linearGradient>
        <linearGradient id="grad6" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#11998e"/>
            <stop offset="100%" stop-color="#38ef7d"/>
        </linearGradient>
        <linearGradient id="grad7" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#FF512F"/>
            <stop offset="100%" stop-color="#DD2476"/>
        </linearGradient>
        
        <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
            <feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#000000" flood-opacity="0.4"/>
        </filter>
    ''')
    svg_parts.append('</defs>')
    
    svg_parts.append('<style>')
    svg_parts.append('''
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@600;700&amp;display=swap');
        .card-bg { fill: #0d1117; rx: 12px; ry: 12px; stroke: #30363d; stroke-width: 1px; }
        .font-mono { font-family: 'Fira Code', 'Courier New', monospace; }
        .header-title { font-size: 13px; fill: #8b949e; font-weight: 600; }
        .pill-text { font-family: 'Fira Code', sans-serif; font-size: 12px; font-weight: 700; fill: #ffffff; }
        
        .dot { rx: 6px; ry: 6px; }
        .dot-red { fill: #ff5f56; }
        .dot-yellow { fill: #ffbd2e; }
        .dot-green { fill: #27c93f; }
        
        .pill {
            rx: 18px;
            ry: 18px;
            filter: url(#shadow);
            opacity: 0;
            animation: pillFade 0.5s ease-out forwards;
        }
        
        @keyframes pillFade {
            0% { opacity: 0; transform: translateY(8px) scale(0.95); }
            100% { opacity: 1; transform: translateY(0) scale(1); }
        }
    ''')
    svg_parts.append('</style>')
    
    # Background Card
    svg_parts.append(f'<rect width="{width}" height="{height}" class="card-bg" />')
    
    # Header Controls
    svg_parts.append('<circle cx="20" cy="18" r="5.5" class="dot dot-red" />')
    svg_parts.append('<circle cx="36" cy="18" r="5.5" class="dot dot-yellow" />')
    svg_parts.append('<circle cx="52" cy="18" r="5.5" class="dot dot-green" />')
    svg_parts.append(f'<text x="{width // 2}" y="22" text-anchor="middle" class="font-mono header-title">lucky@skills ~ eye-catching-gradients.sh</text>')
    svg_parts.append(f'<line x1="0" y1="36" x2="{width}" y2="36" stroke="#30363d" stroke-width="1" />')
    
    # Arrange Gradient Pills in two balanced rows
    row1_skills = skills[:4]
    row2_skills = skills[4:]
    
    # Row 1
    start_x_r1 = 28
    y_r1 = 56
    pill_h = 36
    gap_x = 16
    
    cur_x = start_x_r1
    for idx, (label, grad_id) in enumerate(row1_skills):
        p_width = len(label) * 9 + 32
        delay = round(0.1 + idx * 0.1, 2)
        
        svg_parts.append(f'<g class="pill" style="animation-delay: {delay}s;">')
        svg_parts.append(f'<rect x="{cur_x}" y="{y_r1}" width="{p_width}" height="{pill_h}" fill="url(#{grad_id})" class="pill" />')
        svg_parts.append(f'<text x="{cur_x + p_width // 2}" y="{y_r1 + 22}" text-anchor="middle" class="pill-text">{label}</text>')
        svg_parts.append('</g>')
        cur_x += p_width + gap_x
        
    # Row 2
    start_x_r2 = 80
    y_r2 = 112
    cur_x = start_x_r2
    for idx, (label, grad_id) in enumerate(row2_skills):
        p_width = len(label) * 9 + 36
        delay = round(0.5 + idx * 0.1, 2)
        
        svg_parts.append(f'<g class="pill" style="animation-delay: {delay}s;">')
        svg_parts.append(f'<rect x="{cur_x}" y="{y_r2}" width="{p_width}" height="{pill_h}" fill="url(#{grad_id})" class="pill" />')
        svg_parts.append(f'<text x="{cur_x + p_width // 2}" y="{y_r2 + 22}" text-anchor="middle" class="pill-text">{label}</text>')
        svg_parts.append('</g>')
        cur_x += p_width + gap_x
        
    svg_parts.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))
    print(f"Gradient Tech Stack SVG saved to {output_path}")

if __name__ == "__main__":
    build_tech_stack_svg("tech-stack.svg")
