import os
import sys
import numpy as np
from PIL import Image

RAMP = " .`:-=+*cs#%@"  # bright (sparse) -> dark (dense)

def image_to_ascii(image_path, width=70):
    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found.")
        sys.exit(1)
        
    img = Image.open(image_path).convert('L')
    
    # Calculate aspect ratio adjustment (font characters are taller than wide, ratio ~ 0.52)
    aspect_ratio = img.height / img.width
    font_aspect = 0.52
    height = int(width * aspect_ratio * font_aspect)
    
    img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
    arr = np.array(img_resized)
    
    lines = []
    ramp_len = len(RAMP)
    for row in arr:
        line_chars = []
        for pixel in row:
            # Map pixel brightness [0, 255] to RAMP index
            # Note: 255 is white -> space, 0 is dark -> dense symbol
            idx = int((pixel / 255.0) * (ramp_len - 1))
            line_chars.append(RAMP[idx])
        lines.append("".join(line_chars))
    return lines

def build_animated_ascii_svg(lines, output_path="profile-ascii.svg"):
    font_size = 11
    line_height = 14
    char_width = 6.6
    
    num_rows = len(lines)
    max_cols = max(len(l) for l in lines) if lines else 70
    
    padding_x = 24
    padding_y = 28
    
    width = int(max_cols * char_width + padding_x * 2)
    height = int(num_rows * line_height + padding_y * 2 + 20)
    
    # Animation timings
    total_duration = 3.5  # seconds for full typing
    row_delay = total_duration / max(num_rows, 1)
    
    svg_parts = []
    svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg_parts.append('<style>')
    svg_parts.append('''
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&amp;display=swap');
        .bg { fill: #0d1117; rx: 12px; ry: 12px; stroke: #30363d; stroke-width: 1px; }
        .ascii-text { font-family: 'Fira Code', 'Courier New', Consolas, monospace; font-size: 11px; fill: #58a6ff; white-space: pre; }
        .header-title { font-family: 'Fira Code', monospace; font-size: 12px; fill: #8b949e; font-weight: 600; }
        .dot { rx: 6px; ry: 6px; }
        .dot-red { fill: #ff5f56; }
        .dot-yellow { fill: #ffbd2e; }
        .dot-green { fill: #27c93f; }
        
        .line-reveal {
            animation: lineFade 0.15s ease-out forwards;
            opacity: 0;
        }
        
        @keyframes lineFade {
            from { opacity: 0; transform: translateX(-4px); }
            to { opacity: 1; transform: translateX(0); }
        }
    ''')
    svg_parts.append('</style>')
    
    # Background Card
    svg_parts.append(f'<rect width="{width}" height="{height}" class="bg" />')
    
    # Window Header Controls
    svg_parts.append('<circle cx="20" cy="18" r="5.5" class="dot dot-red" />')
    svg_parts.append('<circle cx="36" cy="18" r="5.5" class="dot dot-yellow" />')
    svg_parts.append('<circle cx="52" cy="18" r="5.5" class="dot dot-green" />')
    svg_parts.append(f'<text x="{width // 2}" y="22" text-anchor="middle" class="header-title">lucky@ascii-art ~ portrait.txt</text>')
    svg_parts.append(f'<line x1="0" y1="36" x2="{width}" y2="36" stroke="#30363d" stroke-width="1" />')
    
    # ASCII Text Rows
    start_y = 56
    for i, line in enumerate(lines):
        y_pos = start_y + i * line_height
        delay = round(i * row_delay, 2)
        # Escape HTML special chars
        escaped_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&#160;")
        svg_parts.append(f'<text x="{padding_x}" y="{y_pos}" class="ascii-text line-reveal" style="animation-delay: {delay}s;">{escaped_line}</text>')
        
    svg_parts.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))
    print(f"Animated ASCII SVG saved to {output_path}")

if __name__ == "__main__":
    prepped_img = "data/source-prepped.png" if os.path.exists("data/source-prepped.png") else "developer_lucky.jpg"
    lines = image_to_ascii(prepped_img, width=60)
    build_animated_ascii_svg(lines, "profile-ascii.svg")
