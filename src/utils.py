import re
from enum import Enum

import bcrypt


class UserRole(Enum):
    USER = "USER"
    BUYER = "BUYER"
    SELLER = "SELLER"
    BOTH = "BOTH"

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

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))