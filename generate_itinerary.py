from PIL import Image, ImageDraw, ImageFont
import os

# Setup
width, height = 1200, 1700
img = Image.new('RGB', (width, height), '#FFFFFF')
draw = ImageDraw.Draw(img)

# Fonts
font_path = "C:/Windows/Fonts/msjh.ttc"
font_bold_path = "C:/Windows/Fonts/msjhbd.ttc"

title_font = ImageFont.truetype(font_bold_path, 36)
header_font = ImageFont.truetype(font_bold_path, 24)
body_font = ImageFont.truetype(font_path, 20)
small_font = ImageFont.truetype(font_path, 16)

# Colors
title_bg = '#1a5276'
header_bg = '#2980b9'
row_even = '#eaf2f8'
row_odd = '#FFFFFF'
border_color = '#1a5276'
text_dark = '#1a1a1a'
text_white = '#FFFFFF'

y = 30

# Title block
draw.rectangle([40, y, width - 40, y + 80], fill=title_bg)
draw.text((width // 2, y + 40), "臺灣旅遊行程表", font=title_font, fill=text_white, anchor="mm")
y += 100

# Applicant info
info_lines = [
    "申請人國籍：中國（持新加坡永久居民身份）",
    "旅遊目的：觀光旅遊",
    "入境日期：2026年5月7日　　　離境日期：2026年5月13日",
    "旅遊天數：7天6夜",
    "旅遊地點：臺北市、花蓮縣",
]
for line in info_lines:
    draw.text((60, y), line, font=body_font, fill=text_dark)
    y += 35

y += 20

# Table setup
col_x = [40, 200, 420, 780, width - 40]
headers = ["日期", "目的地", "住宿", "行程安排"]

# Table header
draw.rectangle([col_x[0], y, col_x[-1], y + 45], fill=header_bg)
for i, h in enumerate(headers):
    cx = (col_x[i] + col_x[i + 1]) // 2
    draw.text((cx, y + 22), h, font=header_font, fill=text_white, anchor="mm")
y += 45

# Itinerary data
itinerary = [
    {
        "date": "5月7日\n（星期四）",
        "dest": "臺北市",
        "hotel": "臺北車站附近\n飯店",
        "plan": "抵達臺灣桃園國際機場\n搭乘機場捷運前往臺北車站\n入住飯店，休息調整\n晚間漫步西門町商圈"
    },
    {
        "date": "5月8日\n（星期五）",
        "dest": "臺北市",
        "hotel": "臺北車站附近\n飯店",
        "plan": "上午：參觀故宮博物院\n下午：遊覽士林官邸\n傍晚：士林夜市品嚐美食"
    },
    {
        "date": "5月9日\n（星期六）",
        "dest": "臺北市",
        "hotel": "臺北車站附近\n飯店",
        "plan": "上午：參觀中正紀念堂\n下午：登臺北101觀景臺\n傍晚：信義區購物\n晚間：饒河街夜市"
    },
    {
        "date": "5月10日\n（星期日）",
        "dest": "花蓮縣",
        "hotel": "花蓮市區\n飯店",
        "plan": "上午：搭乘臺鐵前往花蓮\n下午：抵達花蓮，入住飯店\n傍晚：花蓮東大門夜市"
    },
    {
        "date": "5月11日\n（星期一）",
        "dest": "花蓮縣",
        "hotel": "花蓮市區\n飯店",
        "plan": "全日：太魯閣國家公園\n（燕子口步道、長春祠、\n　砂卡礑步道）"
    },
    {
        "date": "5月12日\n（星期二）",
        "dest": "臺北市",
        "hotel": "臺北車站附近\n飯店",
        "plan": "上午：七星潭風景區\n下午：搭乘臺鐵返回臺北\n晚間：寧夏夜市"
    },
    {
        "date": "5月13日\n（星期三）",
        "dest": "離境",
        "hotel": "—",
        "plan": "上午：整理行李，退房\n前往桃園國際機場\n搭乘航班離開臺灣"
    },
]

row_height = 120

for idx, day in enumerate(itinerary):
    bg = row_even if idx % 2 == 0 else row_odd
    draw.rectangle([col_x[0], y, col_x[-1], y + row_height], fill=bg)
    # Draw cell borders
    for cx in col_x:
        draw.line([(cx, y), (cx, y + row_height)], fill=border_color, width=1)
    draw.line([(col_x[0], y), (col_x[-1], y)], fill=border_color, width=1)

    fields = [day["date"], day["dest"], day["hotel"], day["plan"]]
    for i, text in enumerate(fields):
        lines = text.split('\n')
        text_y = y + 10
        for line in lines:
            if i == 0:
                cx = (col_x[i] + col_x[i + 1]) // 2
                draw.text((cx, text_y), line, font=body_font, fill=text_dark, anchor="mt")
            else:
                draw.text((col_x[i] + 15, text_y), line, font=body_font, fill=text_dark)
            text_y += 28
    y += row_height

# Bottom border
draw.line([(col_x[0], y), (col_x[-1], y)], fill=border_color, width=2)

y += 30

# Notes
draw.text((60, y), "備註：", font=header_font, fill=text_dark)
y += 35
notes = [
    "1. 以上行程僅供參考，實際行程可能依當地天氣及交通狀況調整。",
    "2. 住宿地點將於出發前確認預訂。",
    "3. 全程自由行，不參加旅行團。",
]
for note in notes:
    draw.text((60, y), note, font=small_font, fill='#555555')
    y += 28

# Outer border
draw.rectangle([40, 30, width - 40, y + 20], outline=border_color, width=3)

# Save
output_path = os.path.join(os.path.dirname(__file__), "臺灣旅遊行程表.jpg")
img.save(output_path, "JPEG", quality=95)
print("Saved successfully")
