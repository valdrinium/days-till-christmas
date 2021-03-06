import os
import sys

from datetime import date, datetime
from PIL import Image, ImageFont, ImageDraw

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.utils.config import config
from src.utils.storage import path_to


def write_container(image, center, text, font, fill, margin = (20, 20)):
    drawCenterX, drawCenterY = center
    marginX, marginY = margin

    draw = ImageDraw.Draw(image)
    textWidth, textHeight = draw.textsize(text, font=font)

    startX = int(drawCenterX - textWidth / 2 - marginX)
    startY = int(drawCenterY - textHeight / 2 - marginY / 2)
    button_size = (int(textWidth + 2 * marginX), int(textHeight + 3 * marginY / 2))

    ribbon_path = path_to(os.path.join('assets', 'ribbon-red-l.png'))
    ribbon = Image.open(ribbon_path).convert('RGBA')

    ribbon_ratio = ribbon.size[0] / ribbon.size[1]
    ribbon_size = (int(button_size[1] * ribbon_ratio), button_size[1])
    ribbon.thumbnail(ribbon_size, Image.ANTIALIAS)

    image.paste(ribbon, (startX - ribbon.size[0] + 40, startY + 20), ribbon)

    ribbon_path = path_to(os.path.join('assets', 'ribbon-red-r.png'))
    ribbon = Image.open(ribbon_path).convert('RGBA')

    ribbon_ratio = ribbon.size[0] / ribbon.size[1]
    ribbon_size = (int(button_size[1] * ribbon_ratio), button_size[1])
    ribbon.thumbnail(ribbon_size, Image.ANTIALIAS)

    image.paste(ribbon, (startX + button_size[0] - 40, startY + 20), ribbon)

    button = Image.new('RGBA', button_size, fill)
    image.paste(button, (startX, startY), button)

    return True


def write_text(image, center, text, font, fill, contour = True):
    drawCenterX, drawCenterY = center

    draw = ImageDraw.Draw(image)
    textWidth, textHeight = draw.textsize(text, font=font)

    textCenterX = int(drawCenterX - textWidth / 2)
    textCenterY = int(drawCenterY - textHeight / 2)

    if contour:
        draw.text((textCenterX - 1, textCenterY), text, font=font, fill=(0, 0, 0))
        draw.text((textCenterX + 1, textCenterY), text, font=font, fill=(0, 0, 0))
        draw.text((textCenterX, textCenterY - 1), text, font=font, fill=(0, 0, 0))
        draw.text((textCenterX, textCenterY + 1), text, font=font, fill=(0, 0, 0))

    draw.text((textCenterX, textCenterY), text, font=font, fill=fill)

    return (textWidth, textHeight)


image_path = path_to(os.path.join('images', 'original.jpg'))
image = Image.open(image_path)

imgWidth, imgHeight = image.size

day = config('edit.targetDate.day')
month = config('edit.targetDate.month')
daysLeft = (date(datetime.now().year, month, day) - date.today()).days
if daysLeft < 0:
    daysLeft = (date(datetime.now().year + 1, month, day) - date.today()).days

daysText = str(daysLeft)
if daysLeft % 100 >= 20 or daysLeft % 100 == 0:
    daysText += ' de'

texts = [
    {
        'font': 'Montserrat',
        'color': (255, 255, 255),
        'contour': True,
        'size': int(min(imgWidth, imgHeight) / 16),
        'top': 0
    },
    {
        'font': 'Montserrat',
        'color': (255, 255, 255),
        'contour': False,
        'size': int(min(imgWidth, imgHeight) / 16),
        'top': int(min(imgWidth, imgHeight) / 24),
        'ribbon': {
            'color': (249, 62, 82)
        }
    },
    {
        'font': 'Great Vibes',
        'color': (249, 62, 82),
        'contour': False,
        'size': int(min(imgWidth, imgHeight) / 8),
        'top': int(min(imgWidth, imgHeight) / 12)
    }
]

for textChoice in config('edit.texts'):
    if textChoice['condition'] == 'eq':
        if daysLeft != textChoice['comparedTo']:
            continue
    if textChoice['condition'] == 'gt':
        if daysLeft <= textChoice['comparedTo']:
            continue
    if textChoice['condition'] == 'gte':
        if daysLeft < textChoice['comparedTo']:
            continue

    for i in range(3):
        texts[i]['text'] = textChoice['value'][i].replace(':days', daysText)
    break

text_height = 0
for text in texts:
    font_path = path_to(os.path.join('fonts', f'{text["font"]}.ttf'))
    font = ImageFont.truetype(font_path, text['size'])

    text_height += text["top"]
    text_center = (imgWidth / 2, imgHeight / 3 + text_height)

    if 'ribbon' in text:
        write_container(image, text_center, text['text'], font, text['ribbon']['color'])
    text_height += write_text(image, text_center, text['text'], font, text['color'], text['contour'])[1]

image.save(path_to(os.path.join('images', 'today.png')), 'PNG')
