import logging
import time
import asyncio

from core.models import dict_to_order
from core.utils.PaymentSystem import PaymentSystem
from core.utils.RestHandler import RestHandler


class MainHandler:
    def __init__(self, rest_handler: RestHandler, payment_system: PaymentSystem):
        self.rest = rest_handler
        self.payment_system = payment_system


    async def check_new_orders(self):
        while True:
            terminal = self.payment_system.get_first_free_terminal()
            if terminal is None:
                await asyncio.sleep(0.5)
                continue

            new_payment_dict = await self.rest.get("food/newPayment/")
            if 'error' in new_payment_dict:
                time.sleep(1)
                continue
            order = dict_to_order(new_payment_dict)
            logging.info(f"New payment {order}")

            await self.payment_system.create_payment(terminal_id=terminal.id, order=order)


    async def check_order_status(self):
        while True:
            await self.payment_system.update_order_status()
            await asyncio.sleep(0.5)


    async def show_orders(self):
        while True:
            logging.info(f"Showing orders")
            for order in self.payment_system.orders_stack:
                logging.info(f"Order {order}")

            logging.info(f"Showing terminals")
            for terminal in self.payment_system.terminals:
                logging.info(f"Terminal {terminal}")

            await asyncio.sleep(1)


    async def start(self):
        """
            Добавить task3 если нужно просмотреть состояние приложения
        """
        logging.info(f"Bot started")

        is_authenticated = await self.payment_system.auth_terminals()

        if not is_authenticated:
            logging.error("Errors with terminals authentication")
            return

        task1 = asyncio.create_task(self.check_new_orders())
        task2 = asyncio.create_task(self.check_order_status())
        # task3 = asyncio.create_task(self.show_orders())

        await asyncio.gather(task1, task2)