import random
import string

def generate_short_code(length=6):
    """Generate a random alphanumeric short code of the given length."""
    characters = string.ascii_letters + string.digits
    code = "".join(random.choice(characters) for _ in range(length))
    return code