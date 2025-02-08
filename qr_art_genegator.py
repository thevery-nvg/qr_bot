import io

import cv2
import segno
from PIL import Image
import numpy as np
from aiogram.types import BufferedInputFile
import tempfile
import os


def art_generator(qr_data: str, img: Image):
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
        img.save(tmp_file, format='PNG')
        tmp_file_path = tmp_file.name

    qrcode = segno.make(qr_data, error='h')
    qrcode.to_artistic(background=tmp_file_path, target="img.png", scale=8)

