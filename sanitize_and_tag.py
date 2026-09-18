import os
import re
import json
import urllib.parse
import colorsys
from PIL import Image

def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"

def analyze_image_colors(img):
    """Analyze image using PIL to extract dominant RGB, hex color, and color family."""
    img_rgb = img.convert('RGB')
    small_img = img_rgb.resize((60, 60))
    colors = small_img.getcolors(3600)
    
    if not colors:
        return "#6366f1", "blue", 128, 0.5, 0.5

    # Sort by frequency
    colors.sort(key=lambda x: x[0], reverse=True)
    
    # Filter out pure black / extreme white to find dominant vibrant/hue color if possible
    dom_rgb = colors[0][1]
    for count, (r, g, b) in colors[:15]:
        h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
        if 0.15 < s < 0.95 and 0.15 < v < 0.95:
            dom_rgb = (r, g, b)
            break
            
    r, g, b = dom_rgb
    hex_color = rgb_to_hex(r, g, b)
    h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
    hue_deg = h * 360.0

    # Color Family Categorization
    if v < 0.20:
        color_family = "dark"
    elif s < 0.12:
        color_family = "white" if v > 0.8 else "dark"
    elif hue_deg >= 340 or hue_deg < 15:
        color_family = "red"
    elif 15 <= hue_deg < 45:
        color_family = "gold"
    elif 45 <= hue_deg < 70:
        color_family = "gold"
    elif 70 <= hue_deg < 165:
        color_family = "green"
    elif 165 <= hue_deg < 210:
        color_family = "cyan"
    elif 210 <= hue_deg < 255:
        color_family = "blue"
    elif 255 <= hue_deg < 290:
        color_family = "purple"
    elif 290 <= hue_deg < 340:
        color_family = "pink"
    else:
        color_family = "blue"

    return hex_color, color_family, hue_deg, s, v

def sanitize_filename(filename):
    """Clean filename by removing # and special symbols, replacing spaces with underscores."""
    name, ext = os.path.splitext(filename)
    clean = name.replace('#', '').replace(' ', '_').replace('-', '_')
    clean = re.sub(r'__+', '_', clean).strip('_')
    if not clean:
        clean = "wallpaper"
    return clean.lower() + ext.lower()

def run_sanitization_and_tagging():
    pictures_dir = os.path.join(os.path.dirname(__file__), 'Pictures')
    if not os.path.exists(pictures_dir):
        print(f"Pictures directory missing at {pictures_dir}")
        return

    files = sorted(os.listdir(pictures_dir))
    print(f"Processing {len(files)} files in Pictures/")

    wallpapers = []
    id_counter = 1

    # First Pass: Rename files on disk to clean web-safe names
    renamed_count = 0
    for f in files:
        old_fp = os.path.join(pictures_dir, f)
        if not os.path.isfile(old_fp):
            continue

        ext = os.path.splitext(f)[1].lower()
        if ext not in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
            continue

        clean_f = sanitize_filename(f)
        if clean_f != f:
            new_fp = os.path.join(pictures_dir, clean_f)
            # Avoid overwriting
            if os.path.exists(new_fp) and new_fp != old_fp:
                clean_f = f"{id_counter}_{clean_f}"
                new_fp = os.path.join(pictures_dir, clean_f)
            
            try:
                os.rename(old_fp, new_fp)
                f = clean_f
                renamed_count += 1
            except Exception as err:
                print(f"Failed to rename {old_fp} -> {new_fp}: {err}")

        # Process metadata
        fp = os.path.join(pictures_dir, f)
        size_bytes = os.path.getsize(fp)

        try:
            with Image.open(fp) as img:
                w, h = img.size
                ratio = round(w / h, 2)
                hex_color, color_family, hue, sat, val = analyze_image_colors(img)
        except Exception as e:
            print(f"Error opening image {f}: {e}")
            w, h = 1080, 1920
            ratio = 0.56
            hex_color, color_family, sat, val = "#6366f1", "blue", 0.5, 0.5

        # Device Category
        if ratio >= 1.25:
            category = 'desktop'
        elif ratio <= 0.85:
            category = 'phone'
        else:
            category = 'both'

        # Extract Semantic Tags
        tags = set()
        tags.add(color_family)
        
        if category == 'phone':
            tags.add('mobile')
            tags.add('portrait')
        elif category == 'desktop':
            tags.add('desktop')
            tags.add('landscape')
            tags.add('monitor')
        else:
            tags.add('universal')
            tags.add('square')

        if w >= 2500 or h >= 2500:
            tags.add('4k')
            tags.add('ultra_hd')

        if val < 0.30:
            tags.add('dark')
            tags.add('amoled')
        elif val > 0.80 and sat < 0.2:
            tags.add('light')
            tags.add('minimal')

        if sat > 0.55:
            tags.add('vibrant')
            tags.add('neon')

        # Check filename keywords
        lower_name = f.lower()
        if any(k in lower_name for k in ['krishna', 'radhe', 'pink', 'pinterest', 'god', 'divine']):
            tags.update(['krishna', 'radheradhe', 'spiritual', 'devotional', 'aesthetic'])
        if any(k in lower_name for k in ['mountain', 'nature', 'sunset', 'scenery', 'picjumbo']):
            tags.update(['nature', 'mountains', 'sunset', 'landscape'])
        if any(k in lower_name for k in ['abstract', 'neon', 'circle']):
            tags.update(['abstract', 'neon', 'cyberpunk', 'art'])

        # Generate Friendly Title
        clean_stem = os.path.splitext(f)[0].replace('_', ' ').title()
        
        if 'Krishna' in clean_stem or 'Radheradhe' in clean_stem:
            display_title = "Radhe Krishna Divine Aesthetic"
        elif 'Nature' in clean_stem or 'Mountain' in clean_stem:
            display_title = "Breathtaking Mountain Landscape"
        elif 'Abstract' in clean_stem or 'Neon' in clean_stem:
            display_title = "Neon Cyber Abstract Horizon"
        elif re.match(r'^(Img|Photo|\d+)', clean_stem, re.IGNORECASE):
            # Create human-friendly title based on color and category
            color_prefix = color_family.capitalize()
            cat_suffix = "Portrait" if category == 'phone' else "Desktop" if category == 'desktop' else "Wallpaper"
            display_title = f"{color_prefix} {cat_suffix} #{id_counter:03d}"
        else:
            display_title = clean_stem

        if len(display_title) > 36:
            display_title = display_title[:33] + '...'

        # File size display string
        if size_bytes > 1024 * 1024:
            size_str = f'{size_bytes / (1024 * 1024):.2f} MB'
        else:
            size_str = f'{size_bytes / 1024:.1f} KB'

        rel_path = f'Pictures/{f}'
        encoded_path = f'Pictures/{urllib.parse.quote(f)}'

        wallpapers.append({
            'id': id_counter,
            'filename': f,
            'title': display_title,
            'path': rel_path,
            'encodedPath': encoded_path,
            'width': w,
            'height': h,
            'aspectRatio': ratio,
            'category': category,
            'hexColor': hex_color,
            'colorFamily': color_family,
            'size': size_str,
            'sizeBytes': size_bytes,
            'tags': sorted(list(tags))
        })
        id_counter += 1

    out_path = os.path.join(os.path.dirname(__file__), 'wallpapers.json')
    with open(out_path, 'w', encoding='utf-8') as out_f:
        json.dump(wallpapers, out_f, indent=2)

    print(f"Renamed {renamed_count} files on disk.")
    print(f"Successfully processed {len(wallpapers)} wallpapers into {out_path}")

if __name__ == '__main__':
    run_sanitization_and_tagging()

