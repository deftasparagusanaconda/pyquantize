from typing import Callable

from . import 

def quantize(number: int | float, arg, *args, **kwargs):
	if isinstance(arg, (int, float)):
		return (number, arg, *args, **kwargs)
	elif isinstance(arg, Callable):
		return quantize_to_arbitrary_set(number, arg, *args, **kwargs)
	elif isinstance(arg, (set, list)):
		return quantize_to_arbitrary_set(number, arg, *args, **kwargs)
	else:
		raise ValueError(f'could not dispatch appropriate function for {arg}: unrecognized type ({type(arg)})')
