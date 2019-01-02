import os
import sys

from datetime import date, datetime
from PIL import Image, ImageFont, ImageDraw

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))\
from src.utils.storage import path_to


def write_container(image, center, text, font, fill, margin = (20, 20)):
    drawCenterX, drawCenterY = center
    marginX, marginY = margin

    draw = ImageDraw.Draw(image)
    textWidth, textHeight = draw.textsize(text, font=font)

    startX = int(drawCenterX - textWidth / 2 - marginX)
    startY = int(drawCenterY - textHeight / 2 - marginY / 2)
    button_size = (int(textWidth + 2 * marginX), int(textHeight + 3 * marginY / 2))

    ribbon_ratio = 262 / 168

    ribbon_path = path_to(os.path.join('assets', 'ribbon-red-l.png'))
    ribbon = Image.open(ribbon_path).convert('RGBA')

    ribbon_size = (int(button_size[1] * ribbon_ratio), button_size[1])
    ribbon.thumbnail(ribbon_size, Image.ANTIALIAS)

    image.paste(ribbon, (startX - ribbon.size[0] + 40, startY + 20), ribbon)

    ribbon_path = path_to(os.path.join('assets', 'ribbon-red-R.png'))
    ribbon = Image.open(ribbon_path).convert('RGBA')

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

daysLeft = (date(datetime.now().year, 12, 24) - date.today()).days
if daysLeft < 0:
    daysLeft = (date(datetime.now().year + 1, 12, 24) - date.today()).days

daysText = str(daysLeft)
if daysLeft % 100 >= 20 or daysLeft % 100 == 0:
    daysText += ' de'
daysText += ' ZILE'

texts = [
    {
        'text': 'AU MAI RĂMAS DOAR',
        'font': 'Montserrat',
        'color': (255, 255, 255),
        'contour': True,
        'size': int(min(imgWidth, imgHeight) / 16),
        'top': 0
    },
    {
        'text': daysText,
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
        'text': 'pănă la Crăciun',
        'font': 'Great Vibes',
        'color': (249, 62, 82),
        'contour': False,
        'size': int(min(imgWidth, imgHeight) / 8),
        'top': int(min(imgWidth, imgHeight) / 12)
    }
]

if daysLeft == 0:
    texts[0]['text'] = 'GATA, AZI VINE'
    texts[1]['text'] = ' Moș Crăciun '
    texts[2]['text'] = 'Sper că ai fost cuminte'

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
