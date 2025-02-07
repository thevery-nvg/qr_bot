import qrcode
from PIL import Image, ImageDraw
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import cv2


# 2. Создание градиента
def create_gradient(width, height, start_color, end_color):
    base = Image.new('RGB', (width, height), start_color)
    draw = ImageDraw.Draw(base)
    for y in range(height):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * y / height)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * y / height)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * y / height)
        draw.line((0, y, width, y), fill=(r, g, b))
    return base


def generate(qr_data, style_image):
    # 1. Генерация QR-кода
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert('RGBA')

    gradient = create_gradient(img.width, img.height, (255, 0, 0), (0, 0, 255))  # Красный -> Синий
    gradient.paste(img, (0, 0), img)  # Наложение QR-кода
    # gradient.save("styled_qr.png")

    # 3. Применение стиля с помощью нейросети
    hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

    # Преобразование изображений в float32
    qr_image = np.array(gradient) / 255.0
    qr_image = qr_image.astype(np.float32)  # Преобразуем в float32

    # style_image = np.array(Image.open("style.jpg").resize(img.size)) / 255.0
    # style_image = style_image.astype(np.float32)  # Преобразуем в float32

    # Применение стиля
    stylized_image = \
    hub_model(tf.constant(qr_image[np.newaxis, ...]), tf.constant(style_image[np.newaxis, ...]))[0]
    result = Image.fromarray((stylized_image[0].numpy() * 255).astype(np.uint8))
    # result.save("stylized_qr.png")
    return result

    # 4. Проверка читаемости
    # detector = cv2.QRCodeDetector()
    # data, _, _ = detector.detectAndDecode(cv2.imread("stylized_qr.png"))
    # if data:
    #     print("QR-код читаем! Данные:", data)
    # else:
    #     print("QR-код не читаем.")
