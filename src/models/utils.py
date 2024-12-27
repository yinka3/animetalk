import re
from enum import Enum

class UserRole(Enum):
    USER = "user"
    BUYER = "buyer"
    SELLER = "seller"
    BOTH = "both"
    NONE = "none"

class ContentType(Enum):
    POST = "post"
    FANART = "fanart"
    COMMENT = "comment"

class OrderStatus(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    INPROGRESS = "inprogress"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class JobStatus(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class Proficiency(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"

def parse_mentions(content):
    return re.findall(r"@(\w+)", content)