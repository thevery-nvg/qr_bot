import asyncio
import logging
import sys

from create_bot import dp, bot
from handlers import router_main


def on_start_up() -> None:
    dp.include_router(router_main)
    print(f"Бот успешно запущен")


async def main():
    on_start_up()
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот успешно остановлен_1')
    finally:
        print('Бот успешно остановлен_2')
