from PIL import Image, ImageDraw

CANVAS_SIZE=128
CIRCLE_WIDTH=12
CIRCLE_MARGIN=1  # 円の塗りつぶし時に隙間を空ける
GRAY=(180,180,180)
WHITE=(255,255,255)
BLACK=(0,0,0)

# 36度ごとに塗りつぶした画像を出力
for i in range(0, 11):
    img = Image.new('RGBA', (128, 128), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((8, 8, 120, 120), outline=WHITE, width=CIRCLE_WIDTH)

    # 塗りつぶし部分
    START_XY = (CIRCLE_WIDTH * 2) + CIRCLE_MARGIN
    END_XY = CANVAS_SIZE - (CIRCLE_WIDTH * 2) - CIRCLE_MARGIN
    draw.pieslice((START_XY, START_XY, END_XY, END_XY), -90, (i * 36)- 90, fill=WHITE,  outline=BLACK)

    img.save(f'circle_{i}.png')

if True:
    img = Image.new('RGBA', (128, 128), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((8, 8, 120, 120), outline=GRAY, width=CIRCLE_WIDTH)
    img.save(f'circle_gray.png')
