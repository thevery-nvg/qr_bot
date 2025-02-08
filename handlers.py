import cv2
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import any_state
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.types import FSInputFile
from PIL import Image
import numpy as np
import io

from loguru import logger
from qr_generator import generate
from states import Menus


router_main = Router()


@router_main.message(CommandStart())
async def main_menu(msg: Message, state: FSMContext, bot: Bot):
    await state.clear()
    await msg.answer("Введите данные")
    await state.set_state(Menus.prompt)


@router_main.message(Menus.prompt)
async def prompt(msg: Message, state: FSMContext):
    await state.update_data(prompt=msg.text)
    await msg.answer("Отправьте фото для стилизации")
    await state.set_state(Menus.image)


@router_main.message(Menus.image, F.content_type == "photo")
async def image(msg: Message, state: FSMContext, bot: Bot):
    file_id = msg.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path

    # Скачиваем изображение
    downloaded_file = await bot.download_file(file_path)
    # Преобразуем изображение в PIL Image
    image_stream = io.BytesIO(downloaded_file.read())
    style_image = Image.open(image_stream)
    # Преобразуем изображение в NumPy array и нормализуем
    style_image = np.array(style_image.resize((370, 370))) / 255.0
    style_image = style_image.astype(np.float32)

    await state.update_data(style_image=style_image)

    data = await state.get_data()
    prompt = data.get("prompt")

    try:

        stylized_image = generate(prompt, style_image)
    except Exception as e:
        logger.error(f"Ошибка при генерации изображения: {e}")
        await msg.reply("Произошла ошибка при обработке изображения.")
        return

    result = Image.fromarray((stylized_image[0].numpy() * 255).astype(np.uint8))

    img_np = np.array(result)
    if img_np.shape[2] == 4:
        img_np = cv2.cvtColor(img_np, cv2.COLOR_RGBA2RGB)
    else:
        img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(img_np)
    image_stream = io.BytesIO()
    result.save(image_stream, format="PNG")  # Сохранение в формате PNG
    result.seek(0)

    input_file = BufferedInputFile(image_stream.getvalue(), filename="image.png")

    await bot.send_photo(msg.from_user.id, input_file, caption=data if data else "qr is unreadable")
    await state.clear()
