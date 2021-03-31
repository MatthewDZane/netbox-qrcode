import base64
import qrcode

from io import BytesIO
from PIL import Image, ImageFont, ImageDraw

from pkg_resources import resource_stream
import os


def get_qr_with_text(qr, descr):
    dsi = get_qr_text(qr.size, descr)
    resimg = get_concat(qr, dsi)
    return get_img_b64(resimg)


def get_qr(text, **kwargs):
    qr = qrcode.QRCode(**kwargs)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image()
    img = img.get_image()
    return img


def get_img_b64(img):
    stream = BytesIO()
    img.save(stream, format='png')
    return str(base64.b64encode(stream.getvalue()), encoding='ascii')


def get_qr_text(size, text, font='ArialMT'):
    img = Image.new('L', size, 'white')
    font_size = 100
    flag = True
    font_success = ''
    while flag:
        #file_path = resource_stream(__name__, 'fonts/{}.ttf'.format(font))
        #file = open(r'/opt/netbox/venv/lib/python3.8/site-packages/netbox_qrcode/fonts/TahomaBold.ttf', "rb")
        #bytes_font = BytesIO(file.read())
        try:
            fnt = ImageFont.truetype(os.path.join(os.path.dirname(__file__), 'tahomatest.ttf'),font_size)
            font_success = 'Success'
        except Exception:
            fnt = ImageFont.load_default()
            flag = False
            font_success = 'Failed getting ' + os.path.join(os.path.dirname(__file__), 'tahomatest.ttf')

        draw = ImageDraw.Draw(img)
        w, h = draw.textsize(text, font=fnt)
        if w < size[0] - 4 and h < size[1] - 4:
            flag = False
        font_size -= 1
    W, H = size
    draw.text(((W-w)/2, (H-h)/2), text, font=fnt, fill='black')

    files = os.listdir(os.path.dirname(__file__))
    return img,font_success, files


def get_concat(im1, im2):
    dst = Image.new('L', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst
