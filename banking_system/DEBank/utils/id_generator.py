import random

def generate_id(length):
    """Generate a unique integer ID of a specified digit length."""
    return int(''.join(str(random.randint(0, 9)) for _ in range(length)))
