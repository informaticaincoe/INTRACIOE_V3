# tu_app/templatetags/qr_tags.py
from django import template
from django.utils.safestring import mark_safe
from io import BytesIO
import base64, qrcode
from PIL import Image

register = template.Library()

@register.simple_tag
def qr_src(data, size=96, border=1, ec='M'):
    """
    Devuelve un data URI PNG con el QR de `data`.
    size: tamaño final en px (se reescala manteniendo bordes nítidos)
    border: borde QR (módulos)
    ec: nivel de corrección L/M/Q/H
    """
    if data is None:
        data = ""
    err = {
        'L': qrcode.constants.ERROR_CORRECT_L,
        'M': qrcode.constants.ERROR_CORRECT_M,
        'Q': qrcode.constants.ERROR_CORRECT_Q,
        'H': qrcode.constants.ERROR_CORRECT_H,
    }.get(str(ec).upper(), qrcode.constants.ERROR_CORRECT_M)

    qr = qrcode.QRCode(version=None, error_correction=err, box_size=4, border=int(border))
    qr.add_data(str(data))
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("L")

    # Escalar exactamente al tamaño deseado (sin difuminar)
    size = int(size)
    if size > 0:
        img = img.resize((size, size), Image.NEAREST)

    buf = BytesIO()
    img.save(buf, format="PNG", optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return mark_safe(f"data:image/png;base64,{b64}")
