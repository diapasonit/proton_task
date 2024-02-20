import csv
import os
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from db.model import *


# from db.orm_storage import get_all_orders


def add_product(db_session, products_ids, product_id, product_name, price):
    if not (product_id in products_ids):
        product = Product(id=product_id, name=product_name, price=price)
        db_session.add(product)
        products_ids.add(product_id)
    else:
        product = db_session.query(Product).filter_by(id=product_id).first()
    return product


def add_order(db_session, orders_ids, date, order_id, quantity, product, total_price):
    if not (order_id in orders_ids):
        order_item = OrderItem(quantity=quantity, product=product)
        db_session.add(order_item)
        orders_ids.add(order_id)
        return Order(id=order_id, date=date, items=[order_item], total_price=total_price)
    else:
        order = db_session.query(Order).filter_by(id=order_id).first()
        order_item = OrderItem(quantity=quantity, product=product)
        order.total_price += total_price
        db_session.add(order_item)
        order.items.append(order_item)
        return order


def add_user(db_session, users_ids, customer_id, customer_name, order):
    if not (customer_id in users_ids):
        user = User(id=customer_id, name=customer_name)
        users_ids.add(customer_id)
    else:
        user = db_session.query(User).filter_by(id=customer_id).first()
    user.orders.append(order)
    db_session.add(order)
    db_session.add(user)


def import_data(active_session, data_file_name):
    users_ids = set()
    orders_ids = set()
    products_ids = set()
    with open(data_file_name, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            order_id = int(row['Order ID'])
            customer_id = row['Customer ID']
            customer_name = row['Customer Name']
            product_id = int(row['Product ID'])
            product_name = row['Product Name']
            quantity = int(row['Quantity'])
            total_price = float(row['Total Price'])
            date = datetime.strptime(row['Date'], '%Y-%m-%d').date()
            product = add_product(active_session, products_ids, product_id, product_name, total_price / quantity)
            order = add_order(active_session, orders_ids, date, order_id, quantity, product, total_price)
            add_user(active_session, users_ids, customer_id, customer_name, order)
            active_session.commit()


def db_creation(data_file_name: str):
    os.remove("sqlite.txt")
    engine = create_engine('sqlite:///sqlite.txt')
    Base.metadata.create_all(engine)
    with Session(engine, autoflush=False) as session:
        import_data(session, data_file_name)
        session.commit()


if __name__ == "__main__":
    db_creation('homework_order_lines.csv')
