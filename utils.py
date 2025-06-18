# utils/pin.py
import random
import string

def generate_pin(length=7):
    return ''.join(random.choices(string.digits, k=4) + random.choices(string.ascii_lowercase, k=3))
