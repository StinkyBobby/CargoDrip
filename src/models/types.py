from enum import Enum

class UserType(Enum):
    admin = "Admin"
    worker = "Worker"

class DeliveryStatus(Enum):
    waiting = "Waiting"
    on_way = "On way"
    delivered = "Delivered"

class AcceptionStatus(Enum):
    accepted = "Accepted"
    declined = "Declined"
    in_process = "In process"
    
