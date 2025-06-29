import time
import random
import string
from exacting import Exact, field


def gen_str(length: int) -> str:
    return "".join(random.choices(string.ascii_letters, k=length))
