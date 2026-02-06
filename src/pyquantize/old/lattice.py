from .misc import Space, lp_norm, lp_metric
from .typehints import Scalar, Vector, Norm, Metric
from numbers import Real, Integral
import math
from collections.abc import Sequence

class Lattice(Space):
	'an affine lattice'
	def __init__(
			self, 
			quantum: Scalar | Vector = 1, 
			offset: Scalar | Vector = 0, 
			*,
			norm: Norm = lp_norm, 
			metric: Metric = lp_metric):
		
		scalar_case = isinstance(quantum, Real) and isinstance(offset, Real)
		vector_case = isinstance(quantum, Sequence) and isinstance(offset, sequence)
		
		if not (scalar_case or vector_case):
			raise ValueError('quantum and offset must be both Scalar or both Vector')
		
		if vector_case and len(quantum) != len(offset):
			raise ValueError('dimension mismatch. len(quantum) ≠ len(offset)')
		
		dimension = 1 if scalar_case else len(quantum)
		
		super().__init__(dimension, norm = norm, metric = metric)
		self.quantum = quantum
		self.offset = offset
	
	def project(self,
		quantity     : Scalar | Vector,
		tie_fraction : Real      = 0.5,
		rank         : Integral  = 1  ,
		) -> Scalar | Vector:
		'quantize a number to the n-th nearest number in a shifted (affine) uniform (equally-spaced) grid of numbers (lattice)'
		if not isinstance(quantity, Real):
			raise NotImplementedError('havent made this yet')

		number = quantity	# alias

		number_scaled = (number - self.offset) / self.quantum
		fraction, index_lower = math.modf(number_scaled)
		
		# tied condition
		if fraction == tie_fraction:
			raise NotImplementedError('havent made this yet')

		upper_is_nearer: bool = fraction > tie_fraction
		
		result_nearest_index: int = index_lower + upper_is_nearer
		
		# get the n-th nearest result, where n is rank
		ranked_result_index: int = result_nearest_index + rank // 2 * (-1) ** (rank + upper_is_nearer)	
		# (-1)ˣ is a sign alternating "trick", if you can even call it that. elementary, my dear watson

		ranked_result: Real = ranked_result_index * self.quantum + self.offset
		
		return ranked_result

def quantize_to_uniform_grid_toward(
		number       : Real          ,
		quantum      : Real     = 1  ,
		offset       : Real     = 0  ,
		tie_fraction : Real     = 0.5,
		rank         : Integral = 1  ,
		*                            ,
		centre       : Real     = 0  ,
		rank_tolerace: Integral = 2  ,
		) -> Real:
	'quantize a number to an uniform (equally-spaced) grid of numbers, allowing a deviation from the nearest grid point towards centre'
	
	number_scaled = (number - offset) / quantum
	fraction, index_lower = math.modf(number_scaled)
	
	# tied condition
	if fraction == tie_fraction:
		raise NotImplementedError('havent made this yet')
	
	upper_is_nearer: bool = fraction > tie_fraction
	
	result_nearest_index: int = index_lower + upper_is_nearer



from typing import Literal, Union
from collections.abc import Callable, MutableSequence
from math import floor, ceil, copysign, isinf, isnan
import random

def quantize_to_uniform_grid(
		number        : Union[int, float]                     ,
		quantum       : Union[int, float]      = 1            ,
		offset        : Union[int, float]      = 0            ,
		centre        : Union[int, float]      = 0            ,
		tie_frac      : Union[int, float]      = 0.5          ,
		rank          : int                    = 1            ,
		mode          : str                    = 'rank'       ,
		tie           : str                    = 'even'       ,
		rng           : Callable[[...], float] = random.random,
		alternate_last: MutableSequence[bool]  = [False]      ,
		) -> Union[int, float]:
	"""quantize a number to a uniform (equally-spaced) grid of numbers
	
	parameters
	----------
	number: int or float
		the value to quantize
	
	quantum: int or float, default = 1
		the number will be quantized to multiples of this
	
	offset: int or float, default = 0
		the grid will be offset by this amount
	
	centre: int or float, default = 0
		the centre of the grid. (see 'toward' and 'away' modes)
	
	tie_frac: int or float, default = 0.5
		the multiple closest to the tie_frac is considered the nearest one
	
	mode: {'rank', 'near', 'away', 'alternate', 'random', 'stochastic'}, default = 'rank'
		Quantization method. options are:
		'rank'       → quantize to n-th closest multiple
		'toward'     → quantize toward centre with n-th closest multiple
		'away'       → quantize away from centre with n-th closest multiple
		'alternate'  → (non-deterministic!) quantize up or down alternately according to quantize_grid.alternate_last
		'random'     → (non-deterministic!) quantize up or down randomly
		'stochastic' → (non-deterministic!) quantize up or down stochastically
	
	tie: {'even', 'odd', 'near', 'away', 'alternate', 'random'}, default = 'even'
		tie-breaking method. options are:
		'even'       → break ties to even indices in the grid
		'odd'        → break ties to odd indices in the grid
		'toward'     → break ties toward centre
		'away'       → break ties away from centre
		'alternate'  → (non-deterministic!) break ties up or down alternately according to quantize.alternate_last
		'random'     → (non-deterministic!) break ties up or down randomly
	
	alternate_last: list of bool (len = 1)
		a container for a boolean that remembers whether the last result was rounded up or down when mode was 'alternate'
		
	returns
	-------
	int or float
		the quantized value
	
	raises
	------
	ValueError
		- if quantum is 0 (otherwise the grid would be continuous and so no quantization need occur)
		- if rank is not an int or is 0
		- 
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
	- the function keeps track of state when using mode='alternate' via the attribute quantize_grid.alternate_last (bool)
	- the function preserves signage for zeroes like +0.0 or -0.0
	- the function returns +∞ or -∞ as-is (∵ infinity is only close to itself)
	- the function propagates nan (returns as-is)
	- no i will not change 'centre' to 'center' >:[
	- no, it will not support complex input. the semantics of ℂ do not belong in quantize_grid
	- the default settings allow the function to follow IEEE rounding, i.e. to nearest integer, with even tie-breaking
	"""
	# special cases -----------------------------------------------------------
	
	if quantum == 0:
		raise ValueError("quantum cannot be zero. grid would be infinitely dense")
	
	# check invalid rank value
	if not isinstance(rank, int) or rank <= 0:
		raise ValueError("rank must be an int > 0")
	
	# since infinity is only close to itself, and nan should be propagated
	if isinf(number) or isnan(number):
		return number
	
	# scale number to grid ----------------------------------------------------

	return (number - offset) / quantum

	number_scaled = scale_number_to_uniform_grid(number, quantum, offset)
	
	index_lower: int = floor(number_scaled)    # index of lower nearest grid point
	index_upper: int =  ceil(number_scaled)    # index of upper nearest grid point
	
	if mode != 'rank' and index_lower == index_upper:	# unanimous decision, yknow? it landed directly on a number on the grid
		result = quantum * index_lower + offset
		return copysign(0.0, number) if result == 0 else result
	
	frac = number_scaled - index_lower    # fractional part, on the grid
	
	if mode == 'rank':
		upper_is_nearer: bool = frac > tie_frac
		index_nearer: int = index_upper if upper_is_nearer else index_lower
		result_index: int = index_nearer + rank // 2 * -1 ** (rank + upper_is_nearer)	# (-1)ˣ is a sign alternating "trick", if you can even call it that. elementary, my dear watson
		return quantum * result_index + offset
	
	multiple_lower = quantum * index_lower + offset
	multiple_upper = quantum * index_upper + offset
	
	if frac != tie_frac:
		# not a tie
		if mode == 'toward':
			return multiple_lower if abs(multiple_lower-centre) < abs(multiple_upper-centre) else multiple_upper
		elif mode == 'away':
			return multiple_lower if abs(multiple_lower-centre) > abs(multiple_upper-centre) else multiple_upper
		elif mode == 'alternate':
			quantize_grid.alternate_last = not quantize_grid.alternate_last
			return multiple_lower if quantize_grid.alternate_last else multiple_upper
		elif mode == 'random':
			return multiple_lower if rng() > tie_frac else multiple_upper
		elif mode == 'stochastic':
			return multiple_lower if rng() > frac else multiple_upper
		else:
			raise ValueError("invalid mode. must be one of {'rank', 'toward', 'away', 'alternate', 'random', 'stochastic'}")
	else:
		# a tie
		if tie == 'toward':
			return multiple_lower if abs(multiple_lower-centre) < abs(multiple_upper-centre) else multiple_upper
		elif tie == 'away':
			return multiple_lower if abs(multiple_lower-centre) > abs(multiple_upper-centre) else multiple_upper
		# TOWARD AND AWAY ARE FLAWED. they bias when in the condition where, for example, number = 0.5 and centre = 0.5
		elif tie == 'even':
			return multiple_lower if index_lower % 2 == 0 else multiple_upper
		elif tie == 'odd':
			return multiple_lower if index_lower % 2 == 1 else multiple_upper
		elif tie == 'alternate':
			alternate_last[0] = not alternate_last[0]
			return multiple_lower if alternate_last[0] else multiple_upper
		elif tie == 'random':
			return multiple_lower if rng() > tie_frac else multiple_upper
		else:
			raise ValueError("invalid tie. must be one of {'even', 'odd', 'toward', 'away', 'alternate', 'random'}")
