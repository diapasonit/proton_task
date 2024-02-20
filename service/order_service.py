from service.converters import convert_orders, convert_order_details
from db.orm_storage import ORMStorage


class OrderService:
    @staticmethod
    def get_all_orders():
        return ORMStorage.get_all_orders(convert_orders)

    @staticmethod
    def get_orders(page, size):
        return ORMStorage.get_orders(page, size, convert_orders)

    @staticmethod
    def get_order_details(order_id):
        return ORMStorage.get_order_details(order_id, convert_order_details)

    @staticmethod
    def get_follow_up_orders():
        return ORMStorage.get_follow_up_orders(convert_orders)

    @staticmethod
    def follow_up_order(order_id) -> bool:
        return ORMStorage.follow_up_order(order_id)

    @staticmethod
    def unfollow_up_order(order_id) -> bool:
        return ORMStorage.unfollow_up_order(order_id)
