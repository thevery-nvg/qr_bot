import asyncio
import logging
import sys

from create_bot import dp, bot
from handlers import router_main
from loguru import logger


def on_start_up() -> None:
    dp.include_router(router_main)
    logger.info("Бот успешно запущен")


async def main():
    on_start_up()
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Бот успешно остановлен вручную')
    finally:
        logger.info('Бот успешно остановлен')
