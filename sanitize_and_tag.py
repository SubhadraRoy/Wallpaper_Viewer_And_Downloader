import os
import re
import json
import urllib.parse
import colorsys
from PIL import Image, ImageFilter, ImageStat

def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"

def analyze_image_properties(img):
    img_rgb = img.convert('RGB')
    small_img = img_rgb.resize((60, 60))
    colors = small_img.getcolors(3600)
    
    if not colors:
        return "#6366f1", "blue", 128, 0.5, 0.5, 50.0

    colors.sort(key=lambda x: x[0], reverse=True)
    
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

    gray = img.convert('L').resize((120, 120))
    edges = gray.filter(ImageFilter.FIND_EDGES)
    stat = ImageStat.Stat(edges)
    edge_std = stat.stddev[0]

    return hex_color, color_family, hue_deg, s, v, edge_std

def sanitize_filename(filename):
    name, ext = os.path.splitext(filename)
    clean = name.replace('#', '').replace(' ', '_').replace('-', '_')
    clean = re.sub(r'__+', '_', clean).strip('_')
    if not clean:
        clean = "wallpaper"
    return clean.lower() + ext.lower()

def determine_genres(filename, category, color_family, sat, val, edge_std):
    lower_f = filename.lower()
    genres = set()

    movie_keywords = ['got', 'game_of_thrones', 'mentalist', 'cinema', 'movie', 'series', 'character', 'anime', 'hero', 'joker', 'batman', 'marvel']
    if any(k in lower_f for k in movie_keywords):
        genres.add('movies_series')

    spiritual_keywords = ['krishna', 'radhe', 'buddha', 'god', 'divine', 'statue', 'spiritual', 'devotional', 'temple', 'sacred']
    if any(k in lower_f for k in spiritual_keywords):
        genres.add('spiritual_divine')

    nature_keywords = ['mountain', 'nature', 'sunset', 'landscape', 'tree', 'fuji', 'scenery', 'autumn', 'lake', 'sunrise', 'alpes', 'sea', 'sky', 'milky_way', 'stars', 'forest']
    if any(k in lower_f for k in nature_keywords) or color_family in ['green', 'gold'] and edge_std > 20:
        genres.add('nature_landscape')

    if 'generative_ai' in lower_f or 'abstract' in lower_f or 'vector' in lower_f or '3d' in lower_f or edge_std < 24:
        genres.add('animated_graphical')
    elif any(k in lower_f for k in ['pexels', 'unsplash', 'nikon', 'canon', 'scenic', 'eberhardgross', 'pawel']):
        genres.add('reality_photo')

    if val < 0.35 or color_family == 'dark':
        genres.add('dark_amoled')

    if val > 0.70 and sat < 0.25 or color_family == 'white':
        genres.add('light_minimal')

    if not genres:
        if edge_std > 25:
            genres.add('reality_photo')
        else:
            genres.add('animated_graphical')

    genre_priority = ['movies_series', 'spiritual_divine', 'nature_landscape', 'animated_graphical', 'reality_photo', 'dark_amoled', 'light_minimal']
    primary = 'animated_graphical'
    for p in genre_priority:
        if p in genres:
            primary = p
            break

    return primary, sorted(list(genres))

def generate_natural_title(filename, primary_genre, color_family, index):
    name_stem = os.path.splitext(filename)[0]
    clean = re.sub(r'^\d+_', '', name_stem)
    clean = re.sub(r'img_\d+_\d+_\d+|\d+_\d+_\d+_\d+', '', clean, flags=re.IGNORECASE)
    clean = re.sub(r'[a-f0-9]{8}_[a-f0-9]{4}_[a-f0-9]{4}_[a-f0-9]{4}_[a-f0-9]{12}', '', clean, flags=re.IGNORECASE)
    clean = clean.replace('_', ' ').replace('-', ' ').strip()

    lower_f = filename.lower()
    if 'got' in lower_f or 'game_of_thrones' in lower_f:
        return f"Game of Thrones Artwork #{index}"
    if 'mentalist' in lower_f:
        return f"The Mentalist Art #{index}"
    if 'krishna' in lower_f or 'radhe' in lower_f:
        return f"Radhe Krishna Divine Art #{index}"
    if 'fuji' in lower_f:
        return f"Mount Fuji Landscape #{index}"
    if 'joker' in lower_f:
        return f"The Joker Cyber Art #{index}"
    if 'batman' in lower_f:
        return f"Dark Knight Batman #{index}"

    words = clean.split()
    valid_words = [w.capitalize() for w in words if not w.isdigit() and len(w) > 2 and w.lower() not in ['img', 'picjumbo', 'com', 'jpeg', 'jpg', 'png', 'webp', 'px', 'hd', 'wallpaper', 'wallpapers', 'pinterest', 'download']]

    if valid_words and len(" ".join(valid_words)) >= 4:
        title = " ".join(valid_words)
        if len(title) > 36:
            title = title[:34] + '...'
        return title

    color_descriptors = {
        'dark': ['Obsidian', 'Midnight', 'Shadow', 'Eclipse', 'Onyx', 'Dark Cyber'],
        'cyan': ['Neon Cyan', 'Electric Cyan', 'Aqua Horizon', 'Cyan Cyber', 'Azure Stream'],
        'blue': ['Deep Cobalt', 'Celestial Blue', 'Oceanic Depth', 'Sapphire', 'Cosmic Blue'],
        'purple': ['Mystic Violet', 'Cosmic Purple', 'Amethyst Glow', 'Nebula Purple', 'Velvet Dusk'],
        'pink': ['Vibrant Magenta', 'Neon Pink', 'Cyberpunk Pink', 'Rose Glow', 'Sakura Pulse'],
        'gold': ['Solar Amber', 'Golden Horizon', 'Autumn Gold', 'Gilded Sun', 'Radiant Dawn'],
        'green': ['Emerald Nature', 'Verdant Forest', 'Jade Horizon', 'Bio Green', 'Forest mist'],
        'red': ['Crimson Flare', 'Scarlet Cyber', 'Inferno Red', 'Ruby Ember', 'Magma Glow'],
        'white': ['Minimalist Ivory', 'Pure Monolith', 'Crystal White', 'Snow Apex', 'Luminous Frost']
    }

    genre_descriptors = {
        'movies_series': 'Cinematic Artwork',
        'spiritual_divine': 'Sacred Devotional',
        'nature_landscape': 'Nature Horizon',
        'animated_graphical': 'Abstract Render',
        'reality_photo': 'Scenic Photograph',
        'dark_amoled': 'AMOLED Edition',
        'light_minimal': 'Minimal Aesthetic'
    }

    colors_list = color_descriptors.get(color_family, ['Chroma', 'Lumina', 'Vivid'])
    color_prefix = colors_list[(index - 1) % len(colors_list)]
    genre_suffix = genre_descriptors.get(primary_genre, 'Visual Art')

    return f"{color_prefix} {genre_suffix} #{index}"

def run_sanitization_and_tagging():
    pictures_dir = os.path.join(os.path.dirname(__file__), 'Pictures')
    if not os.path.exists(pictures_dir):
        print(f"Pictures directory missing at {pictures_dir}")
        return

    files = sorted(os.listdir(pictures_dir))
    wallpapers = []
    id_counter = 1

    for f in files:
        fp = os.path.join(pictures_dir, f)
        if not os.path.isfile(fp):
            continue

        ext = os.path.splitext(f)[1].lower()
        if ext not in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
            continue

        size_bytes = os.path.getsize(fp)

        try:
            with Image.open(fp) as img:
                w, h = img.size
                ratio = round(w / h, 2)
                hex_color, color_family, hue, sat, val, edge_std = analyze_image_properties(img)
        except Exception as e:
            w, h = 1080, 1920
            ratio = 0.56
            hex_color, color_family, sat, val, edge_std = "#6366f1", "blue", 0.5, 0.5, 30.0

        if ratio >= 1.25:
            category = 'desktop'
        elif ratio <= 0.85:
            category = 'phone'
        else:
            category = 'both'

        primary_genre, genre_list = determine_genres(f, category, color_family, sat, val, edge_std)

        tags = set(genre_list)
        tags.add(color_family)
        
        if category == 'phone':
            tags.update(['mobile', 'portrait'])
        elif category == 'desktop':
            tags.update(['desktop', 'landscape', 'monitor'])
        else:
            tags.update(['universal', 'square'])

        if w >= 2500 or h >= 2500:
            tags.update(['4k', 'ultra_hd'])

        lower_name = f.lower()
        if any(k in lower_name for k in ['krishna', 'radhe', 'god', 'divine']):
            tags.update(['krishna', 'radheradhe', 'spiritual', 'devotional'])
        if any(k in lower_name for k in ['mountain', 'nature', 'sunset', 'landscape']):
            tags.update(['nature', 'mountains', 'sunset'])

        display_title = generate_natural_title(f, primary_genre, color_family, id_counter)

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
            'primaryGenre': primary_genre,
            'genres': genre_list,
            'hexColor': hex_color,
            'colorFamily': color_family,
            'size': size_str,
            'sizeBytes': size_bytes,
            'tags': sorted(list(tags))
        })
        id_counter += 1

    json_path = os.path.join(os.path.dirname(__file__), 'wallpapers.json')
    with open(json_path, 'w', encoding='utf-8') as out_f:
        json.dump(wallpapers, out_f, indent=2)

    js_path = os.path.join(os.path.dirname(__file__), 'wallpapers.js')
    with open(js_path, 'w', encoding='utf-8') as out_f:
        out_f.write('window.WALLPAPERS_DATA = ' + json.dump_s(wallpapers) if hasattr(json, 'dump_s') else 'window.WALLPAPERS_DATA = ' + json.dumps(wallpapers, indent=2) + ';')

    print(f"Successfully generated wallpapers.json and wallpapers.js ({len(wallpapers)} items)")

if __name__ == '__main__':
    run_sanitization_and_tagging()
