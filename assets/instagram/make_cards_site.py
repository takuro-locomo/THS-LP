# -*- coding: utf-8 -*-
"""公式サイトの用途別ページから作るカルーセル（2026-11-09）。
#12 スポーツ／#13 介護／#14 骨盤帯痛／#15 つくる人。氏名は入れない（FOOTは肩書きのみ）。
使い方: python make_cards_site.py
"""
import os
from PIL import Image, ImageDraw, ImageFont
from make_cards import (OUT, SITE, FB, FR, INK, BLUE, BLUED, SKY, GREY, W, H,
                        tw, center, foot, cover, fit_image, text_slide)


def pic_cover(kicker, head, src, out, note="※イラストはイメージです"):
    """上に見出し、下にサイトのイラスト。"""
    im = Image.new("RGB", (W, H), SKY)
    d = ImageDraw.Draw(im)
    f_k = ImageFont.truetype(FB, 34)
    kw = tw(d, kicker, f_k) + 56
    d.rounded_rectangle(((W - kw) / 2, 90, (W + kw) / 2, 152), radius=31, fill=BLUED)
    center(d, 100, kicker, f_k, (255, 255, 255))
    y = 200
    for line in head:
        f = ImageFont.truetype(FB, 84)
        while tw(d, line, f) > W * 0.9:
            f = ImageFont.truetype(FB, f.size - 4)
        center(d, y, line, f, INK)
        y += int(f.size * 1.3)
    d.rounded_rectangle((W / 2 - 110, y + 10, W / 2 + 110, y + 18), radius=4, fill=BLUE)
    pic = Image.open(src).convert("RGB")
    pw = W - 80
    pic = pic.resize((pw, round(pic.height * pw / pic.width)), Image.LANCZOS)
    top = H - 84 - 60 - pic.height
    im.paste(pic, (40, top))
    center(d, H - 84 - 46, note, ImageFont.truetype(FR, 26), GREY)
    foot(d)
    im.save(out, quality=92)


def pic_text(src, out, title, lines, note):
    """横長の図＋その下に短い説明。"""
    im = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(im)
    center(d, 80, title, ImageFont.truetype(FB, 54), BLUED)
    d.rounded_rectangle((W / 2 - 90, 166, W / 2 + 90, 174), radius=4, fill=BLUE)
    pic = Image.open(src).convert("RGB")
    pw = W - 80
    pic = pic.resize((pw, round(pic.height * pw / pic.width)), Image.LANCZOS)
    im.paste(pic, (40, 210))
    y = 210 + pic.height + 50
    f = ImageFont.truetype(FR, 40)
    for line in lines:
        center(d, y, line, f, INK)
        y += 64
    center(d, H - 84 - 56, note, ImageFont.truetype(FR, 26), GREY)
    foot(d)
    im.save(out, quality=92)


def img(name):
    return os.path.join(SITE, name)


def o(name):
    return os.path.join(OUT, name)


if __name__ == "__main__":
    # #12 スポーツ（/sports/）
    pic_cover("スポーツ｜鼠径部のサポート", ["鼠径部に、", "面で届く圧迫。"], img("illust-sports-wear.webp"), o("12_1_cover.jpg"))
    pic_text(img("illust-sports-zone.webp"), o("12_2_zone.jpg"), "どこに圧がかかるのか",
             ["テーピングやベルトでは届きにくい", "恥骨の外側から太ももの内側上部へ、", "面で圧がかかります。"],
             "※範囲のイメージ図です。実際の圧の数値・範囲ではありません")
    text_slide("サポーターは「ツール」", [
        ("安定", "骨盤・股関節まわりを全周から面で包み、動くときのブレを支えます。"),
        ("圧迫", "編み分けた3段階の圧。鼠径部は強めに、ウエストと裾は快適に。"),
        ("意識づけ", "皮膚への圧迫は、体の位置感覚への入力になるとされています。"),
    ], o("12_3_tool.jpg"))
    text_slide("先にやるべきは、運動", [
        ("いちばん根拠があるのは運動", "鼠径部のトラブルで最も強い根拠があるのは、内転筋の強化などの運動です。"),
        ("履くのは動くとき", "競技復帰のときや、高負荷のトレーニングのときに。"),
        ("休むときは外す", "休息時・就寝時は外して、頼りきりを防ぎます。"),
    ], o("12_4_exercise.jpg"), note="メニューはトレーナー・理学療法士と相談してください")

    # #13 介護（/care/）
    pic_cover("介護施設・在宅介護の方へ", ["介助の手を、", "妨げない。"], img("illust-care-wear.webp"), o("13_1_cover.jpg"))
    text_slide("介護の現場で使いやすい理由", [
        ("薄手", "厚いパッドがなく、トイレ介助・更衣介助がしやすいつくりです。"),
        ("履くだけ", "ベルトのような位置合わせは不要。下着の上から履くだけです。"),
        ("洗える", "洗濯ネットを使って繰り返し洗えます（漂白剤・タンブラー乾燥は不可）。"),
    ], o("13_2_features.jpg"))
    pic_text(img("illust-facility-activity.webp"), o("13_3_scene.jpg"), "動く時間に履く",
             ["歩行練習・機能訓練・レク・散歩など、", "動く時間を中心に着用して、", "休むときは外します。"],
             "※イラストはイメージです")
    text_slide("使う前に確認したいこと", [
        ("おむつとの併用", "厚手のおむつの上からは履けません。下着程度の厚さの上から。"),
        ("皮膚の様子", "かゆみ・発疹・圧迫痕が出たら、すぐに使用を中止してください。"),
        ("就寝中", "寝ているあいだの着用は避けてください。"),
    ], o("13_4_check.jpg"), note="導入前に主治医・看護師・リハビリ担当者にご相談ください")

    # #14 骨盤帯痛（/pelvic-pain/）
    pic_cover("骨盤まわりの痛み（骨盤帯痛）", ["骨盤を締めると、", "何が分かっている？"], img("illust-pelvic-wear.webp"), o("14_1_cover.jpg"))
    pic_text(img("illust-pelvic-zone.webp"), o("14_2_zone.jpg"), "痛む場所は、うしろと前",
             ["うしろの仙腸関節と、前の恥骨結合。", "このまわりの痛みや不安定感を", "「骨盤帯痛」と呼びます。"],
             "※イメージ図です。実際の圧の数値・範囲ではありません")
    text_slide("研究で分かっていること", [
        ("ゆるみは小さくなる", "骨盤ベルトで、仙腸関節のゆるみが力学的に小さくなったという報告があります。"),
        ("その場の動作は楽に", "着けた直後は、脚を上げる動作のつらさが下がったという報告があります。"),
        ("痛みは有意差なし", "7つの研究をまとめると、痛みの差は統計学的に有意ではありませんでした。"),
    ], o("14_3_evidence.jpg"), note="いずれも骨盤ベルトの研究で、本製品の研究ではありません")
    cover(["動きやすいことと、", "治ることは、別の話。"], ["痛みが続く場合は、", "医師にご相談ください。"],
          "まとめ", o("14_4_summary.jpg"))

    # #15 つくる人（/company/・トップの助野の紹介）
    cover(["靴下メーカーが、", "サポーターを編む。"], ["富山県高岡市の", "助野株式会社 おたすけのLAB。"],
          "つくる人", o("15_1_cover.jpg"), note="スワイプで、つくり方 →")
    text_slide("3段階の圧は、編み方でつくる", [
        ("弱・中・強", "生地を貼り合わせるのではなく、編み方そのものを変えています。"),
        ("靴下と同じ発想", "足首はしっかり、ふくらはぎはやさしく。その考え方を股関節に。"),
        ("全周で包む", "必要な場所には強い圧を、それ以外は快適さを優先しています。"),
    ], o("15_2_knit.jpg"))
    text_slide("考えた人・つくる人・届ける人", [
        ("開発・監修", "整形外科専門医"),
        ("企画・製造", "助野株式会社 おたすけのLAB（富山県高岡市）"),
        ("販売", "村中医療器株式会社"),
    ], o("15_3_team.jpg"), note="ご購入は、プロフィールのリンク（公式サイト）から")
    print("done")
