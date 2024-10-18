import logging
import traceback
import asyncio
from dataclasses import dataclass
from typing import List, Optional

from core.utils.RestHandler import RestHandler
from core.utils.QrReader import QrReader
from core.utils.settings import settings
from core.models import Order, order_to_dict


@dataclass
class Terminal:
    id: int
    ip: str
    status: str = "unsent"
    order_id: Optional[int] = None
    access_token: str = None
    refresh_token: str = None


class PaymentSystem:
    def __init__(self, rest_handler: RestHandler):
        self.rest = rest_handler
        self.terminals = [Terminal(id=i, ip=ip) for i, ip in enumerate(settings.terminal_ips)]
        self.orders_stack: List[Order] = []
        self.qr_reader = QrReader()

    async def auth_terminals(self) -> bool:
        logging.info('Auth for terminals started')
        try:
            for terminal in self.terminals:
                self.rest.change_base_url(f"https://{terminal.ip}:8080/v2/")
                data = await self.rest.post(f'register?name=terminal{terminal.id}')
                if 'error' in data:
                    logging.error(f"Terminal {terminal.id}: {data['error']}")
                    return False
                elif 'errorText' in data or not 'data' in data:
                    logging.error(f"Terminal {terminal.id}: {data['data']['message']}")
                    return False
                else:
                    terminal.access_token = data['data']['accessToken']
                    terminal.refresh_token = data['data']['refreshToken']
        except Exception as e:
            error_traceback = traceback.format_exc()
            logging.error(f"auth_terminals error: {e}\nTraceback: {error_traceback}")
        return True

    async def update_order_status(self):
        # "wait" | "success" | "fail" | "unknown" | "error" | "unsent"
        if len(self.orders_stack) != 0 :
            logging.info('Update order status')

        for order in self.orders_stack:
            if order.status == 'unsent':
                continue
            terminal = self.get_terminal_by_id(order.terminal_id)
            self.rest.change_base_url(f"https://{terminal.ip}:8080/v2/")
            data = await self.rest.get(url=f"status?processId={order.process_id}", headers={"accesstoken": terminal.access_token})

            if 'data' not in data or 'status' not in data['data']:
                continue

            if order.status != data['data']['status']:
                order.status = data['data']['status']
                self.rest.change_base_url(settings.api_path)
                await self.rest.update(f"food/newPayment/{order.id}/", order_to_dict(order))

            if order.status != 'wait':
                self.remove_order_by_id(order.id)
                terminal.order_id = None
                terminal.status = "unsent"


    async def create_qr_payment(self, terminal: Terminal, order: Order):
        self.rest.change_base_url(f"https://{terminal.ip}:8080/v2/")
        data = await self.rest.get(url=f"payment?amount={order.price}&owncheque=true", headers={"accesstoken": terminal.access_token})

        if "data" in data and "processId" in data["data"]:
            order.process_id = data["data"]["processId"]

        logging.info(f"Создана оплата на терминале {terminal.ip} для заказа {order.id}")
        logging.info(data)


    async def create_payment(self, terminal_id: int, order: Order) -> bool:
        """Привязывает заказ к терминалу и меняет статус"""
        terminal = self.get_terminal_by_id(terminal_id)
        self.orders_stack.append(order)

        if terminal is None:
            logging.error('Create Payment Error: terminal is None')
            return False

        terminal.status = "wait"
        terminal.order_id = order.id
        order.terminal_id = terminal.id
        order.status = "wait"

        await self.create_qr_payment(terminal, order)

        while order.qr is None:
            qrs, status = self.qr_reader.make_photo()

            if status != "Success":
                logging.error(f"self.qr_reader.make_photo error: {status}")
                return False

            if len(qrs) != 0:
                logging.info(f'Photo successfully made: {qrs}')

            for unknown_qr in qrs:
                is_new_qr = True

                for old_order in self.orders_stack:
                    if unknown_qr == old_order.qr:
                        is_new_qr = False
                        break

                if is_new_qr:
                    order.qr = unknown_qr
                    self.rest.change_base_url(settings.api_path)
                    data = await self.rest.update(f"food/newPayment/{order.id}/", order_to_dict(order))
                    logging.info(f"Updated order {data}")

            await asyncio.sleep(0.2)

        return True

    def get_order_status(self, order_id: int) -> str:
        """Возвращает статус заказа по ID"""
        order = self.get_order_by_id(order_id)
        if order:
            return order.status
        return "Order not found"

    def get_first_free_terminal(self) -> Optional[Terminal]:
        """Находит первый свободный терминал (status: 'unsent')"""
        for terminal in self.terminals:
            if terminal.status == "unsent":
                return terminal
        return None

    def get_terminal_by_id(self, terminal_id: int) -> Optional[Terminal]:
        """Возвращает терминал по его ID"""
        for terminal in self.terminals:
            if terminal.id == terminal_id:
                return terminal
        return None

    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        """Возвращает заказ по его ID"""
        for order in self.orders_stack:
            if order.id == order_id:
                return order
        return None

    def remove_order_by_id(self, order_id: int) -> Order | None:
        """Удаляет заказ из стека по его ID"""
        order = self.get_order_by_id(order_id)
        if order:
            self.orders_stack.remove(order)
            print(f"Заказ с ID {order_id} удалён.")
            return order
        else:
            print(f"Заказ с ID {order_id} не найден.")

