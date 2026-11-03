# -*- coding: utf-8 -*-
"""知識シリーズ「圧迫のサイエンス」の紙芝居（1080x1350・7枚）を作る。
台本の正本は docs/instagram/知識シリーズ_圧迫のサイエンス_2026-11-02.md。

使い方:
  python knowledge_cards.py prompts        各回の ChatGPT 用プロンプトを knowledge/epN/chatgpt_prompt.txt に書き出す
  python knowledge_cards.py build 1        第1回を組む。knowledge/ep1/01.png〜06.png（jpg可）があれば背景に使い、
                                           なければ「画像待ち」の仮背景で組む。出力は knowledge/ep1/out/
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "knowledge")
FB = r"C:\Windows\Fonts\BIZ-UDGothicB.ttc"
FR = r"C:\Windows\Fonts\BIZ-UDGothicR.ttc"
INK = (42, 48, 56); BLUE = (45, 127, 184); BLUED = (31, 95, 139); SKY = (234, 244, 251)
CREAM = (247, 243, 236); GREY = (110, 116, 122); ORANGE = (232, 116, 63); WHITE = (255, 255, 255)
W, H = 1080, 1350
SERIES = "圧迫のサイエンス"
FOOT = "整形外科専門医が開発｜トータルHipサポーター"
NOTE = "※研究の紹介です。トータルHipサポーターの効果を示すものではありません。本品は医療機器ではありません。"

COMMON_PROMPT = """以下の条件でイラストを1枚作ってください。
・縦長（縦横比 4:5 に近い縦長）。
・やわらかいフラットイラスト。線は細め、白〜淡いブルー（#EAF4FB）とネイビー（#1F5F8B）基調、差し色に少しだけオレンジ（#E8743F）。
・人物は日本人。表情はおだやかで前向き。
・画面の上側40%は、文字をあとから載せるために、背景色だけの何もない余白にしてください。
・画像の中に文字・数字・ロゴ・記号を一切入れないでください。
・実在の製品や特定の人物に似せないでください。医師の推薦や体験談に見える構図にしないでください。
・ビフォーアフターのような比較構図にしないでください。
シーン："""

# 各スライド: (見出し, 本文, 画像シーン)。⑦（出典）は画像なしで組む
EPISODES = {
    1: {
        "title": "着圧ウェアで、速くなる？",
        "slides": [
            ("着圧ウェアで、速くなる？", "研究をまとめて、見てみました。",
             "夕方の河川敷を、無地のスポーツ用タイツをはいて走る30代の女性。人物は画面の下半分に小さめに。"),
            ("着圧ウェアとは", "体の表面を、外から一定の力で押さえる服。タイツ・ソックス・スリーブなど。",
             "机の上に、無地のスポーツタイツ・ソックス・アームスリーブが並ぶ俯瞰図（ロゴなし）。"),
            ("記録は、ほぼ変わらない", "ランニングの研究をまとめると、タイムや酸素の取り込みに、はっきりした差は出ていません。",
             "陸上トラックを2人のランナーが並んで走っている。どちらが勝っているか分からない構図。"),
            ("回復は、意見が分かれる", "23研究のまとめでは筋力の戻りに小さなプラス。一方、19の比較試験のまとめでは差なし。",
             "天秤のイラスト。左右の皿にそれぞれ書類の束が乗って、つり合っている。"),
            ("「感じ方」は変わる", "運動後の脚の張り感が軽い、関節の位置がつかみやすい、という報告は多くあります。",
             "運動後にベンチで脚を伸ばして休む人。リラックスした表情。"),
            ("まとめ", "着圧は、記録を伸ばす道具ではなく「着心地と安心感」の道具。練習の代わりにはなりません。",
             "走り終えて、タオルを首にかけて空を見上げる人。"),
        ],
        "refs": [
            "Engel FA, Holmberg HC, Sperlich B. Sports Med. 2016;46(12):1939-1952.",
            "Brown F, et al. Sports Med. 2017;47(11):2245-2267.",
            "Négyesi J, et al. Sports Med. 2022.",
            "Ghai S, Driller M, Ghai I. Phys Ther Sport. 2017;25:65-75.",
        ],
        "note": NOTE,
    },
    2: {
        "title": "医療で使われる「圧迫」",
        "slides": [
            ("「押さえる」は医療の基本", "いちばん古くて、いまも使われている技術のひとつです。",
             "両手で、白いガーゼを腕にそっと当てている手元のアップ。血は描かない。"),
            ("けがの出血には", "清潔な布で傷口を直接、強く押さえる。救急車が来るまで押さえ続けます（直接圧迫止血）。",
             "ビニール手袋をした手で、タオルを前腕に当てて押さえている。そばにスマートフォン（画面に文字なし）。血は描かない。"),
            ("血にはさわらない", "手袋がなければ、ビニール袋を手にかぶせて。止血帯を使うのは訓練を受けてから。",
             "ビニール袋を手袋の代わりに手にかぶせている手元。"),
            ("入院中の血栓予防", "医療用の弾性ストッキングは、20の比較試験のまとめで、脚の血栓を21%→9%に減らしました。",
             "病室のベッドで、白い医療用ストッキングをはいて横になっている高齢の男性。看護師がそばで見守る。"),
            ("でも、万能ではない", "脳卒中の患者さん約2500人の試験では、太ももまでのストッキングで血栓は減らず、皮膚トラブルが増えました。",
             "白衣の人物の後ろ姿（顔は描かない）が、窓の外の晴れと曇りが半分ずつの空を見て考えている。"),
            ("まとめ", "圧迫は「誰に・どこを・どれくらい」で結果が変わる。医療用は医師の判断で使うものです。",
             "診察室の机に、聴診器と文字のないカルテが置かれている静物。"),
        ],
        "refs": [
            "日本救急医療財団・日本蘇生協議会 監修『救急蘇生法の指針2020（市民用）』出血の項",
            "Sachdeva A, Dalton M, Lees T. Cochrane Database Syst Rev. 2018;CD001484.",
            "CLOTS Trials Collaboration. Lancet. 2009;373:1958-1965.",
        ],
        "note": "※研究・指針の紹介です。トータルHipサポーターは医療用の弾性ストッキングとは別のもので、血栓予防や止血の効果はありません。本品は医療機器ではありません。",
    },
    3: {
        "title": "サポーターで、姿勢はよくなる？",
        "slides": [
            ("サポーターで、姿勢はよくなる？", "研究でわかっていること・いないこと。",
             "鏡の前で、横向きに自分の立ち姿を確かめる40代の女性。"),
            ("姿勢を決めるもの", "筋力・柔らかさ・毎日の習慣・その日の疲れ。服の力だけで骨格が変わるわけではありません。",
             "立っている人のまわりに、ダンベル・ストレッチマット・ベッド・時計がやさしく配置されたイラスト。"),
            ("骨盤ベルトの研究①", "健康な女性10人で、ベルトは骨盤の関節（仙腸関節）のゆるさを小さくした。効いたのは強さより「位置」。",
             "シンプルな図解風の骨盤の骨格模型に、腰骨のすぐ下の高さで帯が巻かれている。"),
            ("骨盤ベルトの研究②", "妊娠に関連した骨盤まわりの不調がある女性25人でも、ベルトで仙腸関節の動きが小さくなりました。",
             "産後のお母さんが赤ちゃんを抱いて、穏やかに立っている。"),
            ("感覚のヒントになる", "圧迫やテーピングで関節の位置の感覚がよくなる報告がある一方、結果がそろわない研究もあります。",
             "目を閉じて片足立ちのバランス練習をする人。"),
            ("まとめ", "圧迫は姿勢を「つくる」ものではなく、意識する「きっかけ」。姿勢は運動と習慣でつくるものです。",
             "公園でストレッチをする親子。"),
        ],
        "refs": [
            "Damen L, Spoor CW, Snijders CJ, Stam HJ. Clin Biomech. 2002;17(7):495-498.",
            "Mens JMA, Damen L, Snijders CJ, Stam HJ. Clin Biomech. 2006;21(2):122-127.",
            "Ghai S, Driller M, Ghai I. Phys Ther Sport. 2017;25:65-75.",
        ],
        "note": NOTE,
    },
    4: {
        "title": "手術のあと、太ももはいつ一番太くなる？",
        "slides": [
            ("手術のあと、太ももは\nいつ一番太くなる？", "人工股関節の手術を受けた141人のデータから。",
             "病棟の窓辺で、歩行器を使って立つ高齢の女性。外は朝の光。"),
            ("なぜ太くなるの？", "手術のあと、体は治すために血液や水分を集めます。股関節は深い筋肉に囲まれていて、太ももに出やすい。",
             "人体のシルエットで、股関節から太ももの位置がやわらかく光っている図解風イラスト。"),
            ("ピークは術後5日目", "着用しなかった64人では、太ももの太さは術後5日目に手術前の約107%。",
             "7日分のカレンダーのイラスト（数字なし）。5番目のマスだけ色がついている。"),
            ("比べてみると", "手術室から5日間サポーターを着けた77人は、術後1日・5日とも太さの増え方が小さかった。",
             "目盛りや数字のない、2本の線グラフの抽象イラスト。一方の線がゆるやか。"),
            ("その後は差なし", "術後2週・12週では両群に差はなく、サポーターに関連した合併症はありませんでした。",
             "退院して自宅の庭を散歩する高齢の女性。"),
            ("研究の読み方", "くじ引きで分けた研究ではなく、過去のデータを比べた研究。「効果がある」とは言い切れません。",
             "机の上で、文字のない論文を虫めがねで読む手元。"),
        ],
        "refs": [
            "Thigh swelling after total hip arthroplasty: time course and prevention by an adjustable compression supporter.",
            "J Joint Surg Res. 2026;4(3):212-217. doi:10.1016/j.jjoisr.2026.04.002（オープンアクセス）",
        ],
        "note": "※1施設の後ろ向き研究で、効果を保証するものではありません。本品は医療機器ではありません。ご使用は医師の指導のもとで。",
    },
}


def tw(d, s, f):
    l, t, r, b = d.textbbox((0, 0), s, font=f)
    return r - l


def wrap(d, text, font, max_w):
    lines, line = [], ""
    for ch in text:
        if ch == "\n":
            lines.append(line); line = ""; continue
        if tw(d, line + ch, font) > max_w and line:
            # 句読点・閉じかっこを行頭に送らない
            if ch in "、。」）・":
                line += ch; continue
            lines.append(line); line = ch
        else:
            line += ch
    if line:
        lines.append(line)
    return lines


def fit_cover(img, w, h):
    r = max(w / img.width, h / img.height)
    im = img.resize((round(img.width * r), round(img.height * r)), Image.LANCZOS)
    x = (im.width - w) // 2
    y = (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def background(ep_dir, idx, scene):
    for ext in (".png", ".jpg", ".jpeg", ".webp"):
        p = os.path.join(ep_dir, f"{idx:02d}{ext}")
        if os.path.exists(p):
            return fit_cover(Image.open(p).convert("RGB"), W, H), True
    im = Image.new("RGB", (W, H), SKY)
    d = ImageDraw.Draw(im)
    d.rectangle((60, 620, W - 60, H - 140), outline=(190, 210, 228), width=3)
    f = ImageFont.truetype(FR, 28)
    d.text((90, 650), f"画像待ち（{idx:02d}）", font=f, fill=GREY)
    for i, ln in enumerate(wrap(d, scene, f, W - 180)[:8]):
        d.text((90, 700 + i * 44), ln, font=f, fill=GREY)
    return im, False


def chrome(d, idx, total):
    # シリーズ名と枚数、フッター
    f = ImageFont.truetype(FB, 26)
    label = SERIES
    lw = tw(d, label, f) + 36
    d.rounded_rectangle((48, 44, 48 + lw, 92), radius=24, fill=BLUED)
    d.text((66, 54), label, font=f, fill=WHITE)
    fn = ImageFont.truetype(FR, 26)
    num = f"{idx} / {total}"
    d.text((W - 48 - tw(d, num, fn), 56), num, font=fn, fill=BLUED)
    d.rectangle((0, H - 72, W, H), fill=CREAM)
    ff = ImageFont.truetype(FR, 26)
    d.text(((W - tw(d, FOOT, ff)) / 2, H - 52), FOOT, font=ff, fill=INK)


def slide(ep_dir, idx, total, head, body, scene):
    im, has_img = background(ep_dir, idx, scene)
    d = ImageDraw.Draw(im, "RGBA")
    cover = idx == 1
    hf = ImageFont.truetype(FB, 76 if cover else 60)
    bf = ImageFont.truetype(FR, 40 if cover else 38)
    max_w = W - 160
    hl = []
    for part in head.split("\n"):
        hl += wrap(d, part, hf, max_w)
    bl = wrap(d, body, bf, max_w)
    hh = int(hf.size * 1.3) * len(hl)
    bh = int(bf.size * 1.6) * len(bl)
    top = 128
    panel_h = 60 + hh + 34 + bh + 40
    d.rounded_rectangle((48, top, W - 48, top + panel_h), radius=28, fill=(255, 255, 255, 225))
    y = top + 40
    for ln in hl:
        x = (W - tw(d, ln, hf)) / 2 if cover else 80
        d.text((x, y), ln, font=hf, fill=INK)
        y += int(hf.size * 1.3)
    bar_x = W / 2 - 70 if cover else 80
    d.rounded_rectangle((bar_x, y + 6, bar_x + 140, y + 14), radius=4, fill=ORANGE if cover else BLUE)
    y += 34
    for ln in bl:
        x = (W - tw(d, ln, bf)) / 2 if cover else 80
        d.text((x, y), ln, font=bf, fill=BLUED if cover else INK)
        y += int(bf.size * 1.6)
    chrome(d, idx, total)
    return im, has_img


def refs_slide(idx, total, ep):
    im = Image.new("RGB", (W, H), SKY)
    d = ImageDraw.Draw(im)
    hf = ImageFont.truetype(FB, 56)
    d.text((80, 150), "出典", font=hf, fill=BLUED)
    d.rounded_rectangle((80, 230, 220, 238), radius=4, fill=BLUE)
    rf = ImageFont.truetype(FR, 32)
    y = 290
    for r in ep["refs"]:
        lines = wrap(d, r, rf, W - 200)
        d.text((80, y), "・", font=rf, fill=INK)
        for ln in lines:
            d.text((120, y), ln, font=rf, fill=INK)
            y += 48
        y += 18
    nf = ImageFont.truetype(FR, 30)
    nl = wrap(d, ep["note"], nf, W - 200)
    ny = H - 120 - len(nl) * 46 - 40
    d.rounded_rectangle((60, ny - 30, W - 60, ny + len(nl) * 46 + 10), radius=20, fill=WHITE)
    for i, ln in enumerate(nl):
        d.text((90, ny + i * 46), ln, font=nf, fill=GREY)
    chrome(d, idx, total)
    return im


def write_prompts():
    for no, ep in EPISODES.items():
        ep_dir = os.path.join(ROOT, f"ep{no}")
        os.makedirs(ep_dir, exist_ok=True)
        out = [f"# 第{no}回「{ep['title']}」 ChatGPT用プロンプト",
               "1つの会話で、上から順に1枚ずつ送ってください（絵柄がそろいます）。",
               "できた画像は 01.png〜06.png の名前でこのフォルダに保存してください。", ""]
        for i, (_, _, scene) in enumerate(ep["slides"], 1):
            out += [f"―――― {i:02d}.png ――――", COMMON_PROMPT + scene, ""]
        with open(os.path.join(ep_dir, "chatgpt_prompt.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(out))
        print("wrote", os.path.join(ep_dir, "chatgpt_prompt.txt"))


def build(no):
    ep = EPISODES[no]
    ep_dir = os.path.join(ROOT, f"ep{no}")
    out_dir = os.path.join(ep_dir, "out")
    os.makedirs(out_dir, exist_ok=True)
    total = len(ep["slides"]) + 1
    missing = []
    for i, (head, body, scene) in enumerate(ep["slides"], 1):
        im, ok = slide(ep_dir, i, total, head, body, scene)
        if not ok:
            missing.append(i)
        im.save(os.path.join(out_dir, f"ep{no}_{i:02d}.jpg"), quality=92)
    refs_slide(total, total, ep).save(os.path.join(out_dir, f"ep{no}_{total:02d}.jpg"), quality=92)
    print("built", out_dir, "missing images:", missing or "none")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "prompts":
        write_prompts()
    elif cmd == "build":
        for n in (sys.argv[2:] or EPISODES):
            build(int(n))
    else:
        print(__doc__)
