
from pwdlib import PasswordHash

# Create password hashing instance
password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Convert plain password into a secure hash."""
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify entered password against stored hash."""
    return password_hash.verify(plain_password, hashed_password)
