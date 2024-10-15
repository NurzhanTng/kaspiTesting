import asyncio
import logging

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

    logging.info(f"Bot started")
    return

if __name__ == '__main__':
    asyncio.run(main())