from numbers import Real
from .misc import Space

def quantize(number, space: Space, *args, **kwargs) -> Real:
	return space.project(number, *args, **kwargs)

def quantize(number, quantum, offset, *args, **kwargs) -> Real:
	return Lattice(quantum, offset).project(number, *args, **kwargs)

#def quantize()
