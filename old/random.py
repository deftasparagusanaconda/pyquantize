import hashlib
import struct

FACTOR = 2 ** -64

def hash_random(x: float) -> float:
	# encode x as bytes
	b: bytes = struct.pack('d', x)
	h: bytes = hashlib.blake2b(b, digest_size=8).digest()

	# convert to 64-bit unsigned integer
	i: int = int.from_bytes(h)
	
	# 3. scale to [0, 1)
	return i * FACTOR

