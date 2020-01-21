import random
import string


def random_port():
    return random.randint(1024, 65536)


def random_string(k=5):
    return ''.join(random.choices(string.ascii_lowercase, k=k))


def random_int(a=0, b=10):
    return random.randint(a, b)
