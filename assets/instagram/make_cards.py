# -*- coding: utf-8 -*-
"""文字中心のInstagramカルーセル（1080x1350）を作る。#02 サイズ／#06 使い方。
使い方: python make_cards.py
"""
from PIL import Image, ImageDraw, ImageFont
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "posts")
SITE = os.path.join(HERE, "..", "..", "site", "images")
FB = r"C:\Windows\Fonts\BIZ-UDGothicB.ttc"
FR = r"C:\Windows\Fonts\BIZ-UDGothicR.ttc"
INK = (58, 62, 58); BLUE = (45, 127, 184); BLUED = (31, 95, 139); CREAM = (247, 243, 236)
SKY = (234, 244, 251); ORANGE = (232, 116, 63); GREY = (110, 110, 105); WHITE = (255, 255, 255)
FOOT = "整形外科専門医が開発｜トータルHipサポーター"
W, H = 1080, 1350


def tw(d, s, f):
    l, t, r, b = d.textbbox((0, 0), s, font=f)
    return r - l


def center(d, y, s, f, fill):
    d.text(((W - tw(d, s, f)) / 2, y), s, font=f, fill=fill)


def foot(d):
    d.rectangle((0, H - 84, W, H), fill=CREAM)
    f = ImageFont.truetype(FR, 30)
    center(d, H - 60, FOOT, f, INK)


def cover(head, sub, kicker, out, note=None):
    im = Image.new("RGB", (W, H), SKY)
    d = ImageDraw.Draw(im)
    d.ellipse((620, -260, 1340, 460), outline=(205, 226, 242), width=4)
    d.ellipse((-300, 900, 420, 1620), outline=(205, 226, 242), width=4)
    f_k = ImageFont.truetype(FB, 34)
    kw = tw(d, kicker, f_k) + 56
    d.rounded_rectangle(((W - kw) / 2, 300, (W + kw) / 2, 362), radius=31, fill=BLUED)
    center(d, 310, kicker, f_k, WHITE)
    y = 440
    for line in head:
        f = ImageFont.truetype(FB, 92)
        while tw(d, line, f) > W * 0.88:
            f = ImageFont.truetype(FB, f.size - 4)
        center(d, y, line, f, INK)
        y += int(f.size * 1.32)
    d.rounded_rectangle((W / 2 - 110, y + 14, W / 2 + 110, y + 22), radius=4, fill=BLUE)
    y += 64
    f2 = ImageFont.truetype(FR, 42)
    for line in sub:
        center(d, y, line, f2, BLUED)
        y += 64
    if note:
        f3 = ImageFont.truetype(FR, 30)
        center(d, H - 160, note, f3, GREY)
    foot(d)
    im.save(out, quality=92)


def fit_image(src, out, title, caption):
    im = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FB, 46)
    center(d, 40, title, f, BLUED)
    pic = Image.open(src).convert("RGB")
    box_w, box_h = W - 60, H - 84 - 120 - 70
    r = min(box_w / pic.width, box_h / pic.height)
    pic = pic.resize((round(pic.width * r), round(pic.height * r)), Image.LANCZOS)
    im.paste(pic, ((W - pic.width) // 2, 112))
    f2 = ImageFont.truetype(FR, 28)
    center(d, H - 84 - 52, caption, f2, GREY)
    foot(d)
    im.save(out, quality=92)


def text_slide(title, rows, out, note=None):
    """rows: list of (bold_label, text)"""
    im = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FB, 54)
    center(d, 90, title, f, BLUED)
    d.rounded_rectangle((W / 2 - 90, 176, W / 2 + 90, 184), radius=4, fill=BLUE)
    y = 250
    fb = ImageFont.truetype(FB, 44)
    fr = ImageFont.truetype(FR, 38)
    for i, (lab, txt) in enumerate(rows, 1):
        d.ellipse((80, y + 2, 140, y + 62), fill=BLUE)
        n = str(i)
        d.text((110 - tw(d, n, fb) / 2, y + 4), n, font=fb, fill=WHITE)
        d.text((168, y + 4), lab, font=fb, fill=INK)
        y += 66
        # wrap txt
        line = ""
        for ch in txt:
            if tw(d, line + ch, fr) > W - 168 - 80 and ch not in "。、）」":
                d.text((168, y), line, font=fr, fill=GREY)
                y += 54
                line = ch
            else:
                line += ch
        if line:
            d.text((168, y), line, font=fr, fill=GREY)
            y += 54
        y += 34
    if note:
        f3 = ImageFont.truetype(FR, 30)
        center(d, H - 84 - 60, note, f3, GREY)
    foot(d)
    im.save(out, quality=92)


def size_table(out):
    im = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(im)
    center(d, 90, "サイズ表（男女兼用）", ImageFont.truetype(FB, 54), BLUED)
    d.rounded_rectangle((W / 2 - 90, 176, W / 2 + 90, 184), radius=4, fill=BLUE)
    rows = [("M", "68〜78cm"), ("L", "78〜88cm"), ("LL", "88〜100cm"), ("3L", "100〜112cm"), ("4L", "112〜124cm")]
    x0, x1, x2 = 150, 420, 930
    y = 250
    fh = ImageFont.truetype(FB, 40)
    d.rectangle((x0, y, x2, y + 80), fill=BLUED)
    d.text((x0 + 60, y + 18), "サイズ", font=fh, fill=WHITE)
    d.text((x1 + 60, y + 18), "ウエスト（目安）", font=fh, fill=WHITE)
    y += 80
    fb = ImageFont.truetype(FB, 48)
    fr = ImageFont.truetype(FR, 44)
    for i, (s, w) in enumerate(rows):
        bg = SKY if i % 2 == 0 else WHITE
        d.rectangle((x0, y, x2, y + 96), fill=bg)
        d.text((x0 + 70, y + 22), s, font=fb, fill=INK)
        d.text((x1 + 60, y + 24), w, font=fr, fill=INK)
        y += 96
    d.rectangle((x0, 330, x2, y), outline=(214, 226, 236), width=2)
    y += 50
    d.rounded_rectangle((110, y, W - 110, y + 250), radius=24, fill=(255, 247, 241), outline=(243, 211, 194), width=2)
    center(d, y + 34, "迷ったら、1〜2サイズ上を。", ImageFont.truetype(FB, 46), ORANGE)
    f2 = ImageFont.truetype(FR, 34)
    center(d, y + 110, "腹囲100cmを超える方は4Lで十分です。", f2, INK)
    center(d, y + 166, "よく使われているのは LL・3L。", f2, INK)
    foot(d)
    im.save(out, quality=92)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    # #06 使い方（カテーテル）
    cover(["カテーテルは、", "ここを通します。"], ["手術室で麻酔から覚めたあとから", "履けるのは、股の開口部があるから。"],
          "使い方｜股関節の手術のあと", os.path.join(OUT, "06_1_cover.jpg"), note="スワイプで6ステップ →")
    fit_image(os.path.join(SITE, "lp2-donning-6steps.webp"), os.path.join(OUT, "06_2_steps.jpg"),
              "看護師さんの介助で履かせる6ステップ", "※カテーテルと採尿バッグは接続したまま操作します")
    text_slide("術後の使い方の目安", [
        ("手術当日", "手術室で、防水被覆材の上から着用します。"),
        ("術後24時間", "カテーテルは開口部に通したまま、連続して着用します。"),
        ("術後1週間", "洗濯しながら連続使用。洗い替えがあると便利です。"),
        ("退院後", "散歩やリハビリなど、動くときに履きます。"),
    ], os.path.join(OUT, "06_3_schedule.jpg"), note="必ず主治医・病棟スタッフの指示に従ってください")
    # #02 サイズ
    cover(["迷ったら、", "1〜2サイズ上。"], ["試着アンケートでいちばん多かった声は", "「きつい」でした。"],
          "サイズの選び方", os.path.join(OUT, "02_1_cover.jpg"), note="スワイプでサイズ表 →")
    size_table(os.path.join(OUT, "02_2_table.jpg"))
    text_slide("大きめをすすめる理由", [
        ("圧迫力が強めの設計", "ウエストと太ももの付け根が、きつく感じやすいつくりです。"),
        ("大きめでも圧がかかる", "必要な場所には、しっかり圧がかかるように編んでいます。"),
        ("迷ったらDMで", "ウエストと太ももの付け根の周囲を教えてください。目安をお返しします。"),
    ], os.path.join(OUT, "02_3_why.jpg"))
    print("done")
