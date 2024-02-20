from db.model import Order
from dto.dto import *


def convert_order(order: Order):
    if order is None:
        return EmptyDTO()
    return OrderDTO(id=order.id, customer_name=order.user.name, total_price=order.total_price,
                    date=order.date.strftime("%Y/%m/%d"))


def convert_orders(orders: List[Order]):
    order_list = list()
    for order in orders:
        order_dto = convert_order(order)
        order_list.append(order_dto)
    return OrdersDTO(order_list=order_list)


def convert_order_details(order: Order):
    if order is None:
        return None
    item_details = list()
    for item in order.items:
        item_details.append(
            OrderDetailItemDTO(price=item.product.price, name=item.product.name, quantity=item.count))
    return OrderDetailsDTO(items=item_details)
