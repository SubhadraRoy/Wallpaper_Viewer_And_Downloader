import os
import json
import urllib.parse
import struct
import re

def get_image_size(filepath):
    """Extract image width and height from PNG or JPEG headers without external dependencies."""
    try:
        with open(filepath, 'rb') as f:
            data = f.read(32)
            # Check PNG
            if data.startswith(b'\x89PNG\r\n\x1a\n'):
                w, h = struct.unpack('>II', data[16:24])
                return w, h
            # Check JPEG
            f.seek(0)
            buf = f.read()
            if buf.startswith(b'\xff\xd8'):
                idx = 2
                while idx < len(buf) - 8:
                    if buf[idx] != 0xff:
                        idx += 1
                        continue
                    marker = buf[idx+1]
                    if marker in (0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7, 0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf):
                        h, w = struct.unpack('>HH', buf[idx+5:idx+9])
                        return w, h
                    length = struct.unpack('>H', buf[idx+2:idx+4])[0]
                    idx += 2 + length
    except Exception:
        pass
    return None

def build_index():
    pictures_dir = os.path.join(os.path.dirname(__file__), 'Pictures')
    if not os.path.exists(pictures_dir):
        print(f"Directory not found: {pictures_dir}")
        return

    files = os.listdir(pictures_dir)
    wallpapers = []
    id_counter = 1

    for f in sorted(files):
        fp = os.path.join(pictures_dir, f)
        if os.path.isfile(fp):
            ext = os.path.splitext(f)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp']:
                continue

            size_bytes = os.path.getsize(fp)
            dimensions = get_image_size(fp)

            w = dimensions[0] if dimensions else 1080
            h = dimensions[1] if dimensions else 1920
            ratio = round(w / h, 2)

            if ratio >= 1.2:
                category = 'desktop'
            elif ratio <= 0.85:
                category = 'phone'
            else:
                category = 'both'

            # Clean name & extract tags
            clean_name = os.path.splitext(f)[0]
            raw_tags = re.findall(r'#?\w+', clean_name)
            tags = sorted(list(set([t.lower().replace('#', '') for t in raw_tags if len(t) > 1 and not t.isdigit()])))

            display_title = clean_name.replace('_', ' ').replace('#', ' ').strip()
            display_title = re.sub(r'\s+', ' ', display_title)
            if len(display_title) > 36:
                display_title = display_title[:33] + '...'

            # File size string
            if size_bytes > 1024 * 1024:
                size_str = f'{size_bytes / (1024 * 1024):.2f} MB'
            else:
                size_str = f'{size_bytes / 1024:.1f} KB'

            rel_path = f'Pictures/{f}'
            encoded_path = f'Pictures/{urllib.parse.quote(f)}'

            wallpapers.append({
                'id': id_counter,
                'filename': f,
                'title': display_title if display_title else f"Wallpaper #{id_counter}",
                'path': rel_path,
                'encodedPath': encoded_path,
                'width': w,
                'height': h,
                'aspectRatio': ratio,
                'category': category,
                'size': size_str,
                'sizeBytes': size_bytes,
                'tags': tags
            })
            id_counter += 1

    out_path = os.path.join(os.path.dirname(__file__), 'wallpapers.json')
    with open(out_path, 'w', encoding='utf-8') as out_f:
        json.dump(wallpapers, out_f, indent=2)

    print(f"Successfully indexed {len(wallpapers)} wallpapers into {out_path}")

if __name__ == '__main__':
    build_index()
