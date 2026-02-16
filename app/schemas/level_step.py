from enum import Enum

class LevelStep(str, Enum):
    L1 = "입문자"
    L2 = "초보자"
    L3 = "중급자"
    L4 = "고급자"
    L5 = "전문자"