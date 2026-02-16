from enum import Enum

class GStringEnum(str, Enum):
    normal = "일반줄"
    coting = "코팅줄"