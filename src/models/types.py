from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    driver = "driver"

class DeliveryStatus(str, Enum):
    waiting = "waiting"
    on_way = "on_way"
    delivered = "delivered"

    @property
    def label(self) -> str:
        return {
            DeliveryStatus.waiting: "Waiting",
            DeliveryStatus.on_way: "On way",
            DeliveryStatus.delivered: "Delivered",
        }[self]