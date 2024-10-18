import asyncio
import logging

from core.main_handler import MainHandler
from core.utils.PaymentSystem import PaymentSystem
from core.utils.RestHandler import RestHandler


async def main():
    with open('data/history.log', 'w') as file:
        file.write('')
    logging.basicConfig(
        filemode='a',
        filename=f'data/history.log',
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
        encoding='utf-8',
    )

    rest_handler = RestHandler()
    payment_rest_handler = RestHandler(verify_ssl=False)
    payment_handler = PaymentSystem(payment_rest_handler)
    main_handler = MainHandler(rest_handler, payment_handler)

    await main_handler.start()

if __name__ == '__main__':
    asyncio.run(main())