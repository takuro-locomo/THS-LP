# -*- coding: utf-8 -*-
"""Instagramストーリーズ画像（1080x1920）を作る。上下の操作UIに隠れない範囲に文字を置く。
使い方: python make_stories.py
"""
from PIL import Image, ImageDraw, ImageFont
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "stories")
POSTS = os.path.join(HERE, "posts")
SITE = os.path.join(HERE, "..", "..", "site", "images")
FB = r"C:\Windows\Fonts\BIZ-UDGothicB.ttc"
FR = r"C:\Windows\Fonts\BIZ-UDGothicR.ttc"
INK = (58, 62, 58); BLUE = (45, 127, 184); BLUED = (31, 95, 139); CREAM = (247, 243, 236); GREY = (110, 110, 105)
FOOT = "整形外科専門医が開発｜トータルHipサポーター"
NOTE = "※本品は医療機器ではありません。ご使用は医師の指導のもとで。"
W, H = 1080, 1920
TOP, IMG_T, IMG_B, NOTE_Y, FOOT_Y = 250, 690, 1370, 1400, 1510

STORIES = [
    ("1108_postpartum", ["骨盤ベルトを、", "トイレのたびに", "外していませんか。"], "「履く」なら、そのまま", os.path.join(POSTS, "03_src.png"), 0.85,
     "くわしくはプロフィールのリンクから"),
    ("1109_size", ["迷ったら、", "1〜2サイズ上。"], "圧迫力を強めにつくっているから", os.path.join(SITE, "illust-senior-wear.webp"), 0.5,
     "サイズの相談はDMへ（ウエスト・太もも周りを教えてください）"),
    ("1110_knit", ["靴下メーカーが、", "編んでいます。"], "弱・中・強の3段階は、編み方そのもので", os.path.join(SITE, "illust-senior-zone.webp"), 0.5,
     "富山県高岡市・助野 おたすけのLAB"),
    ("1111_bandage", ["包帯は、巻いた直後しか", "効いていない。"], "だから、「履く」にしました。", os.path.join(POSTS, "01_src.png"), 0.85,
     "くわしくはプロフィールのリンクから"),
    ("1112_catheter", ["手術直後から", "使えるのは、", "開口部があるから。"], "カテーテルを通して履けます", os.path.join(SITE, "illust-surgery-wear.webp"), 0.5,
     "くわしい手順はプロフィールのリンクから"),
    ("1113_wear", ["動くときに履く。", "休むときは脱ぐ。"], "散歩、買い物、リハビリに", os.path.join(SITE, "illust-senior-exercise.webp"), 0.5,
     "自宅でできる体操はプロフィールのリンクから"),
    ("1114_walk", ["散歩に行くとき、", "履く。"], "衣服の下に目立たない、薄手のメッシュ", os.path.join(POSTS, "07_src.png"), 0.8,
     "くわしくはプロフィールのリンクから"),
]


def tw(d, s, f):
    l, t, r, b = d.textbbox((0, 0), s, font=f)
    return r - l


def center(d, y, s, f, fill):
    d.text(((W - tw(d, s, f)) / 2, y), s, font=f, fill=fill)


def fit(d, s, path, max_w, start):
    size = start
    while size > 30 and tw(d, s, ImageFont.truetype(path, size)) > max_w:
        size -= 2
    return ImageFont.truetype(path, size)


def cover(img, w, h, anchor):
    r = max(w / img.width, h / img.height)
    im = img.resize((round(img.width * r), round(img.height * r)), Image.LANCZOS)
    x = (im.width - w) // 2; y = round((im.height - h) * anchor)
    return im.crop((x, y, x + w, y + h))


def make(name, head, sub, src, anchor, note):
    base = Image.new("RGB", (W, H), CREAM)
    base.paste(cover(Image.open(src).convert("RGB"), W, IMG_B - IMG_T, anchor), (0, IMG_T))
    d = ImageDraw.Draw(base)
    size = min(fit(d, s, FB, W * 0.88, 76).size for s in head)
    f = ImageFont.truetype(FB, size)
    y = TOP if len(head) == 3 else TOP + 44
    for line in head:
        center(d, y, line, f, INK); y += int(size * 1.3)
    d.rounded_rectangle((W / 2 - 110, y + 6, W / 2 + 110, y + 14), radius=4, fill=BLUE)
    center(d, y + 34, sub, fit(d, sub, FR, W * 0.88, 38), BLUED)
    center(d, NOTE_Y, note, fit(d, note, FR, W * 0.88, 34), BLUED)
    center(d, NOTE_Y + 52, NOTE, fit(d, NOTE, FR, W * 0.88, 26), GREY)
    center(d, FOOT_Y, FOOT, ImageFont.truetype(FR, 30), INK)
    base.save(os.path.join(OUT, name + ".jpg"), quality=92)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for s in STORIES:
        make(*s)
