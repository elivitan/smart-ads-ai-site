"""Resize Lea founder photos for web — JPG, optimized."""
from PIL import Image
import os

SRC = r'C:\Users\BSDAO\Downloads'
DST = r'C:\V\smart-ads-ai-site\founder'
os.makedirs(DST, exist_ok=True)

# Map source -> (output_name, target_width, target_height_or_None)
JOBS = {
    'Founder Standing Portrait.png':       ('lea-portrait.jpg',   720, 960),
    'Boss in Office - Meeting Table.png':  ('lea-office.jpg',     960, 720),
    'Solo Office - Working on Laptop.png': ('lea-building.jpg',   960, 720),
    'Solo Office - Writing in Notebook.png': ('lea-thinking.jpg', 960, 720),
    'Solo Office - Phone Call.png':        ('lea-calls.jpg',      960, 720),
    'Solo Office - Leaning on Desk.png':   ('lea-leaning.jpg',    960, 720),
    'Meeting Scene - Matched Face v1.png': ('lea-meeting.jpg',    960, 720),
}


def cover_crop(img, tw, th):
    ratio = max(tw / img.width, th / img.height)
    nw, nh = int(img.width * ratio), int(img.height * ratio)
    rs = img.resize((nw, nh), Image.LANCZOS)
    ox, oy = (nw - tw) // 2, (nh - th) // 2
    return rs.crop((ox, oy, ox + tw, oy + th))


for src_name, (out_name, tw, th) in JOBS.items():
    src_path = os.path.join(SRC, src_name)
    if not os.path.exists(src_path):
        print(f'MISSING: {src_name}')
        continue
    img = Image.open(src_path).convert('RGB')
    out = cover_crop(img, tw, th)
    out_path = os.path.join(DST, out_name)
    out.save(out_path, 'JPEG', quality=85, optimize=True, progressive=True)
    print(f'{out_name}  {tw}x{th}  {os.path.getsize(out_path)//1024} KB')

print('Done.')
