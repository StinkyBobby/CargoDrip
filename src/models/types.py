from enum import Enum

class role_enum_new(Enum):
    admin = "admin"
    driver = "driver"

class DeliveryStatus(Enum):
    waiting = "Waiting"
    on_way = "On way"
    delivered = "Delivered"
