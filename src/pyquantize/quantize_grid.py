# i feel like quantize should even be able to take a set of possible values and return the closest one in value to the one given. is that too much?
# we intentionally do not use a match case just for compatibility with older python versions

from typing import Literal, Union
from math import floor, ceil, copysign, isinf, isnan
from random import random, randint

def quantize_grid(
		number             : Union[int, float]               ,
		quantum            : Union[int, float] = 1           ,
		offset             : Union[int, float] = 0           ,
		centre             : Union[int, float] = 0           ,
		tie_point          : Union[int, float] = 0.5         ,
		rank               : int               = 1           ,
		mode               : str               = 'stochastic',
		tie                : str               = 'random'    ,
		) -> Union[int,float]:
	"""quantize a real number to a grid of multiples

	parameters.
	----------
	number: int or float
		the value to quantize

	quantum: int or float, default = 1
		the number will be quantized to multiples of this

	offset: int or float, default = 0
		the grid will be shifted by this amount

	centre: int or float, default = 0
		(see 'toward' and 'away' modes) the centre of the grid

	tie_point: int or float, default = 0.5
		point from which the fractional part is considered to be closer up or down or tied

	mode: {'near', 'far', 'floor', 'ceil', 'toward', 'away', 'even', 'odd', 'rank', 'alternate', 'random', 'stochastic'}, default = 'near'
		Quantization method. options are:
		'near'       → quantize to closest multiple
		'far'        → quantize to second-closest multiple
		'floor'      → quantize down toward -∞
		'ceil'       → quantize up toward +∞
		'even'       → quantize to nearest even multiple
		'odd'        → quantize to nearest odd multiple
		'toward'     → quantize toward centre
		'away'       → quantize away from centre
		'rank'       → quantize to n-th closest multiple
		'alternate'  → (non-deterministic!) quantize up or down alternately according to quantize_grid.alternate_last
		'random'     → (non-deterministic!) quantize up or down randomly
		'stochastic' → (non-deterministic!) quantize up or down according to stochastic probability (default)

	tie: {'floor', 'ceil', 'toward', 'away', 'even', 'odd', 'alternate', 'random', 'stochastic'}, default = 'even'
		tie-breaking method. options are:
		'floor'      → break ties down toward -∞
		'ceil'       → break ties up toward +∞
		'toward'     → break ties toward centre
		'away'       → break ties away from centre
		'even'       → break ties toward nearest even multiple
		'odd'        → break ties toward nearest odd mulltiple
		'alternate'  → (non-deterministic!) break ties up or down alternately according to quantize.alternate_last
		'random'     → (non-deterministic!) break ties up or down randomly (default)

	returns
	-------
	int or float
		the quantized value

	raises
	------
	ValueError
		- if quantum is 0 (otherwise the grid would be continuous and so no quantization need occur)
		- if mode or tie are not recognized options

	examples
	--------
	>>> quantize(3.14, 0.5, mode='stochastic')
	3 # or occasionally 3.5
	>>> quantize(3.7, quantum=1)
	4
	>>> quantize(3.7, quantum=2, mode='floor')
	2

	notes
	-----
	the function keeps track of state when using mode='alternate' via the attribute quantize.alternate_last (bool)

	the function preserves signage for zeroes like +0.0 or -0.0

	the function returns +∞ or -∞ as-is (infinity is only close to itself)

	the function propagates nan

	the function does not yet check if tie_point ∈ [0, 1] or not

	mathematically, 'floor' and 'ceil' modes are redundant (since they are generalized by 'toward' and 'away' modes) but they require lesser computation so they are kept for practical purposes. similarly for 'near' and 'far' with 'order'

	no i will not change 'centre' to 'center' >:[
	"""
	if quantum == 0:
		raise ValueError("quantum cannot be zero")

	if not isinstance(order, int) or order <= 0:
		raise ValueError("order must be an int > 0")

	if isinf(number) or isnan(number):	# since infinity is only close to itself, and nan should be propagated
		return number

	number_scaled = (number - offset) / quantum	# the number is now scaled to the grid

	index_lower: int = floor(number_scaled)    # index of lower nearest grid point
	index_upper: int =  ceil(number_scaled)    # index of upper nearest grid point

	if mode != 'rank' and index_lower == index_upper:	# unanimous decision, yknow?
		result = quantum * index_lower + offset
		return copysign(0.0, number) if result == 0 else result

	frac = number_scaled - index_lower    # fractional part, on the grid

	multiple_lower = quantum * index_lower + offset
	multiple_upper = quantum * index_upper + offset

	if frac != tie_point:
		if mode == 'near':
			result = multiple_upper if frac > tie_point else multiple_lower
		elif mode == 'far':
			result = multiple_lower if frac > tie_point else multiple_upper
		elif mode == 'floor':
			result = multiple_lower
		elif mode == 'ceil':
			result = multiple_upper
		elif mode == 'toward':
			result = multiple_lower if abs(multiple_lower-centre) < abs(multiple_upper-centre) else multiple_upper
		elif mode == 'away':
			result = multiple_upper if abs(multiple_lower-centre) < abs(multiple_upper-centre) else multiple_lower
		elif mode == 'even':
			result = multiple_upper if index_upper % 2 == 0 else multiple_lower
		elif mode == 'odd':
			result = multiple_lower if index_upper % 2 == 0 else multiple_upper
		elif mode == 'rank':
			upper_is_nearer: bool = frac > tie_point
			index_nearer: int = index_upper if upper_is_nearer else index_lower
			result_index: int = index_nearer + rank // 2 * -1 ** (rank + upper_is_nearer)	# (-1)ˣ is a sign alternating "trick", if you can even call it that. elementary, my dear watson
			result = quantum * result_index + offset
		elif mode == 'alternate':
			quantize_grid.alternate_last = not quantize.alternate_last
			result = multiple_lower if quantize_grid.alternate_last else multiple_upper
		elif mode == 'random':
			result = multiple_lower if randint(0, 1) else multiple_upper
		elif mode == 'stochastic':
			result = multiple_upper if random() < frac else multiple_lower
		else:
			raise ValueError("invalid mode. must be one of {'near', 'far', 'floor', 'ceil', 'toward', 'away', 'even', 'odd', 'rank', 'alternate', 'random', 'stochastic'}")
	else:
		elif tie == 'floor':
			result = multiple_lower
		elif tie == 'ceil':
			result = multiple_upper
		elif tie == 'toward':
			result = multiple_lower if abs(multiple_lower-centre) < abs(multiple_upper-centre) else multiple_upper
		elif tie == 'away':
			result = multiple_upper if abs(multiple_lower-centre) < abs(multiple_upper-centre) else multiple_lower
		elif tie == 'even':
			result = multiple_upper if index_upper % 2 == 0 else multiple_lower
		elif tie == 'odd':
			result = multiple_lower if index_upper % 2 == 0 else multiple_upper
		elif tie == 'alternate':
			quantize_grid.alternate_last: bool = not quantize_grid.alternate_last
			result = multiple_lower if quantize_grid.alternate_last else multiple_upper
		elif tie == 'random':
			result = multiple_lower if randint(0, 1) else multiple_upper
		else:
			raise ValueError("invalid tie. must be one of {'floor', 'ceil', 'toward', 'away', 'even', 'odd', 'alternate', 'random'}")
	
	return (copysign(0.0, number) if result == 0 else result)
	
quantize_grid.alternate_last: bool = False

"""
from typing import Literal, Union
from math import floor, ceil, copysign, isinf, isnan
from random import random, randint

def quantize(
		number             :Union[int,float],
		quantum            :Union[int,float] = 1,
		offset             :Union[int,float] = 0,
		centre             :Union[int,float] = 0,
		threshold          :Union[int,float] = 0.5,
		directed           :bool             = False,
		signed_zero        :bool             = True,
		threshold_inclusive:bool             = True,
		mode               :str              = 'even',
		) -> Union[int,float]:
	if isinf(number) or isnan(number):
		return number

	if mode == 'stochastic' and not directed:
		raise ValueError(f"mode={mode} requires directed={True}")

	number_scaled = (number-offset) / quantum # the number is now scaled to the grid

	index_lower = floor(number_scaled)    # index of lower nearest grid point
	index_upper =  ceil(number_scaled)    # index of upper nearest grid point
	frac = number_scaled - index_lower    # fractional part, on the grid

	multiple_lower = quantum*index_lower + offset
	multiple_upper = quantum*index_upper + offset

	if not directed and frac != 0.5:
		result = multiple_lower if (frac <= threshold if threshold_inclusive else frac < threshold) else multiple_upper
	else:
		if mode == 'threshold':
			result = multiple_lower if (frac <= threshold if threshold_inclusive else frac < threshold) else multiple_upper
		elif mode == 'floor':
			result = multiple_lower
		elif mode == 'ceil':
			result = multiple_upper
		elif mode == 'toward':
			result = multiple_lower if abs(multiple_lower-centre) < abs(multiple_upper-centre) else multiple_upper
		elif mode == 'away':
			result = multiple_upper if abs(multiple_lower-centre) < abs(multiple_upper-centre) else multiple_lower
		elif mode == 'even':
			result = multiple_upper if index_upper % 2 == 0 else multiple_lower
		elif mode == 'odd':
			result = multiple_lower if index_upper % 2 == 0 else multiple_upper
		elif mode == 'alternate':
			quantize.alternate_last = not quantize.alternate_last
			result = multiple_lower if quantize.alternate_last else multiple_upper
		elif mode == 'random':
			result = multiple_lower if randint(0, 1) else multiple_upper
		elif mode == 'stochastic':
			result = multiple_upper if random() < frac else multiple_lower
		else:
			raise ValueError("invalid mode. must be one of {'threshold','floor','ceil','toward','away','even','odd','alternate','random','stochastic'}")
	
	if signed_zero and result == 0:
		result = copysign(0.0, number)
	
	return result

quantize.alternate_last = False
"""
