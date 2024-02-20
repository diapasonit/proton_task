from db.db_adapter import DBAdapter
from service.converters import *


class ORMStorage:
    @staticmethod
    def get_all_orders(converter):
        with DBAdapter().get_session() as session:
            orders = session.query(Order).filter_by(follow_up=False).all()
            return converter(orders)

    @staticmethod
    def get_orders(page, size, converter):
        with DBAdapter().get_session() as session:
            orders = session.query(Order).filter_by(follow_up=False).limit(size).offset(size * (page - 1)).all()
            return converter(orders)

    @staticmethod
    def get_order_details(order_id, converter):
        with DBAdapter().get_session() as session:
            order = session.query(Order).filter_by(id=order_id).first()
            return converter(order)

    @staticmethod
    def get_follow_up_orders(converter):
        with DBAdapter().get_session() as session:
            orders = session.query(Order).filter_by(follow_up=True).all()
            return converter(orders)

    @staticmethod
    def follow_up_order(order_id) -> bool:
        with DBAdapter().get_session() as session:
            session.begin()
            order = session.query(Order).filter_by(id=order_id).first()
            if order is None:
                return False
            order.follow_up = True
            session.add(order)
            return True

    @staticmethod
    def unfollow_up_order(order_id) -> bool:
        with DBAdapter().get_session() as session:
            session.begin()
            order = session.query(Order).filter_by(id=order_id).first()
            if order is None:
                return False
            order.follow_up = False
            session.add(order)
            return True
