import binascii;
import random;
import string;

def _create_random_string():
    "Creates random string with length of 10"
    return ''.join(random.SystemRandom().choice(string.uppercase + string.digits) for _ in xrange(10))

def _hash(text):
    "Creates crc32 hash formatted as hex value"
    return '%08x' % (binascii.crc32(text) & 0xffffffff);

def create_paste_hash(obj, title):
    """
    Calculates hash of a title, or random string if the title is not present.
    It generates hashes as long as one is not unique.
    """
    text = title or _create_random_string()

    hash = _hash(text)

    while obj.objects.filter(hash=hash).count() > 0:
        hash = _hash(_create_random_string())

    return hash