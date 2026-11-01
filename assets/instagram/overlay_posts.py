# -*- coding: utf-8 -*-
"""Instagram投稿画像：文字なしイラストに見出しを重ねる（1080x1350）。
使い方: python overlay_posts.py <post_no> <元画像> <出力jpg>
"""
import sys
from PIL import Image, ImageDraw, ImageFont

FONT_B = r"C:\Windows\Fonts\BIZ-UDGothicB.ttc"
FONT_R = r"C:\Windows\Fonts\BIZ-UDGothicR.ttc"
INK = (58, 62, 58); BLUE = (45, 127, 184); BLUED = (31, 95, 139); CREAM = (247, 243, 236); GREIGE = (150, 140, 128)
FOOT = "整形外科専門医 上野琢郎 開発｜トータルHipサポーター"

POSTS = {
    "01": {"head": ["包帯は、巻いた直後しか", "効いていない。"], "sub": "だから、「履く」にしました。"},
    "02": {"head": ["迷ったら、", "1〜2サイズ上。"], "sub": "圧迫力が強めだから、大きめでも効きます"},
    "03": {"head": ["骨盤ベルトを、", "トイレのたびに外していませんか。"], "sub": "「履く」なら、そのまま"},
    "04": {"head": ["靴下メーカーが、", "サポーターを編む理由。"], "sub": "富山・助野 おたすけのLAB"},
    "06": {"head": ["カテーテルは、", "ここを通します。"], "sub": "手術室で麻酔から覚めたあとから"},
    "07": {"head": ["散歩に行くとき、", "履く。"], "sub": "衣服の下に目立たない、薄手のメッシュ"},
    "08": {"head": ["お求めは、", "村中医療器へ。"], "sub": "病院・施設・個人の方へ"},
    "09": {"head": ["おむつ交換の邪魔を", "しない、薄さ。"], "sub": "介護施設・在宅介護に"},
    "10": {"head": ["依存ではなく、", "自立支援のために。"], "sub": "動くときに履く。休むときは脱ぐ。"},
}

def fit_cover(img, w, h, anchor_y=0.5):
    r = max(w / img.width, h / img.height)
    im = img.resize((round(img.width * r), round(img.height * r)), Image.LANCZOS)
    x = (im.width - w) // 2; y = round((im.height - h) * anchor_y)
    return im.crop((x, y, x + w, y + h))

def tw(d, s, f):
    l, t, r, b = d.textbbox((0, 0), s, font=f); return r - l

def fit_font(d, s, path, max_w, start, minimum=30):
    size = start
    while size > minimum:
        f = ImageFont.truetype(path, size)
        if tw(d, s, f) <= max_w: return f
        size -= 2
    return ImageFont.truetype(path, minimum)

def make(no, src, out):
    W, H = 1080, 1350
    base = fit_cover(Image.open(src), W, H, 0.5).convert("RGB")
    d = ImageDraw.Draw(base)
    p = POSTS[no]
    y = 96
    for line in p["head"]:
        f = fit_font(d, line, FONT_B, W * 0.9, 80)
        d.text(((W - tw(d, line, f)) / 2, y), line, font=f, fill=INK); y += int(f.size * 1.3)
    d.rounded_rectangle((W/2 - 110, y + 8, W/2 + 110, y + 16), radius=4, fill=BLUE)
    y += 40
    f2 = fit_font(d, p["sub"], FONT_R, W * 0.9, 40)
    d.text(((W - tw(d, p["sub"], f2)) / 2, y), p["sub"], font=f2, fill=BLUED)
    band = 84
    d.rectangle((0, H - band, W, H), fill=CREAM)
    f3 = ImageFont.truetype(FONT_R, 30)
    d.text(((W - tw(d, FOOT, f3)) / 2, H - band + 24), FOOT, font=f3, fill=INK)
    base.save(out, quality=92)

if __name__ == "__main__":
    make(sys.argv[1], sys.argv[2], sys.argv[3]); print("done", sys.argv[3])
