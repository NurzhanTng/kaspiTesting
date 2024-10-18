from dataclasses import dataclass
from typing import Optional


@dataclass
class Order:
    id: int
    price: int
    status: str = "unsent"
    terminal_id: Optional[int] | None = None
    process_id: Optional[int] | None = None
    qr: str | None = None


# Функция для создания экземпляра Order из словаря
def dict_to_order(data: dict) -> Order:
    return Order(
        id=data.get('order_id'),
        price=data.get('price'),
        status=data.get('status', "unsent"),
        terminal_id=None,
        process_id=data.get('process_id'),
        qr=data.get('qr_link')
    )


# Функция для преобразования экземпляра Order в словарь
def order_to_dict(order: Order) -> dict:
    return {
        "order_id": order.id,
        "price": order.price,
        "status": order.status,
        "process_id": order.process_id,
        "qr_link": order.qr,
    }

