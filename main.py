import hashlib
import hmac
import os
from typing import Tuple


# adapted from Mark Amery - https://stackoverflow.com/a/56915300
def hash_password(password: str) -> Tuple[bytes, bytes]:
    salt = os.urandom(16)
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 1000000)
    return salt, password_hash


def check_password(salt: bytes, password_hash: bytes, password: str) -> bool:
    return hmac.compare_digest(
        password_hash,
        hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 1000000)
    )
