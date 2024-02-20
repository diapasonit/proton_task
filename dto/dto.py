from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class OrderDTO:
    id: int
    customer_name: str
    total_price: float
    date: str


@dataclass_json
@dataclass
class EmptyDTO:
    pass


@dataclass_json
@dataclass
class OrdersDTO:
    order_list: List[OrderDTO]


@dataclass_json
@dataclass
class OrderDetailItemDTO:
    price: float
    quantity: int
    name: str


@dataclass_json
@dataclass
class OrderDetailsDTO:
    items: List[OrderDetailItemDTO]
