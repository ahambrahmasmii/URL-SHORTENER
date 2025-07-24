import hashlib
import string
from urllib.parse import urlparse

ALPHANUM = string.digits + string.ascii_letters

def base62_encode(num, length=6):
    base = 62
    s = []
    while num > 0:
        num, rem = divmod(num, base)
        s.append(ALPHANUM[rem])
    return ''.join(reversed(s)).rjust(length, '0')[:length]

def generate_deterministic_code(long_url, length=6):
    hash_digest = hashlib.sha256(long_url.encode()).hexdigest()
    hash_int = int(hash_digest, 16)
    return base62_encode(hash_int, length)

def is_valid_url(url):
    try:
        result = urlparse(url)
        return result.scheme in ('http', 'https') and result.netloc
    except:
        return False
