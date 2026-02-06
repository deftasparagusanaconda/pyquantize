# TODO: make IntegerLattice.project more advanced. wayyyyy more advanced

import math
from abc import ABC, abstractmethod
#from .typehints import Vector, Norm, Metric
from numbers import Real, Integral
from collections.abc import Callable, Sequence
from heapq import nsmallest
from typing import TypeAlias

VERIFY_STRUCTURES: bool = True

# typehints -------------------------------------------------------------------

# an int or a float, usually. not a bool though heh. stuff like 1, 2, -1, 1.0, 5.5, …
#Scalar: TypeAlias = Real

# a recursive sequence of scalar values. this actually admits a ragged tensor, interestingly.
Tensor: TypeAlias = Real | Sequence['Tensor']

# a 1-rank tensor
Vector: TypeAlias = Sequence[Real]

# a distance-like function that collapses scalars and vectors to a +ve real number
Norm: TypeAlias = Callable[[Real | Vector], Real]

# a comparison function that returns the distance between two points
Metric: TypeAlias = Callable[[Real, Real], Real] | Callable[[Vector, Vector], Real]

# functions -------------------------------------------------------------------

def lp_norm(quantity: Real | Vector, p: Real = 2) -> Real:
	if isinstance(quantity, Real):
		return abs(quantity) 
	if p == 2:
		return math.hypot(*quantity)
	return sum(abs(scalar) ** p for scalar in quantity) ** (1 / p)

def lp_metric(a: Real | Vector, b: Real | Vector, p: Real = 2) -> Real:
	if isinstance(a, Real):
		return abs(a - b)
	return lp_norm(tuple(x - y for x, y in zip(a, b)), p)

# classes ---------------------------------------------------------------------

class Space(ABC):
	def __init__(
			self, 
			dimension: Integral, 
			*, 
			norm: Norm = lp_norm, 
			metric: Metric = lp_metric):
		self.dimension: Integral = dimension
		self.norm: Norm = norm
		self.metric: Metric = metric

	# make __mul__ and __rmul__ so we can have product spaces, perhaps? that would be cool

	@abstractmethod
	def project(self, quantity: Real | Vector) -> Real | Vector:
		...
	
	#def show(self, center: Real, point_count: int = 5) -> None:
	#	'show some points on the space to get a feel for what its like'
	#	points = {self.project(0, rank = i) for i in range(1, point_count + 1)}
	#	print('{' + …, … + '}')
	
class FinitePoints(Space):
	def __init__(self,
			points: set[Real] | set[Vector],
			*, 
			norm: Norm = lp_norm, 
			metric: Metric = lp_metric,
			) -> None:
		self.points: set[Real] | set[Vector] = points
		
		iterator = iter(points)
		some_point = next(iter(points))
		dimension: Integral = len(some_point) if isinstance(some_point, Sequence) else 1
		
		if VERIFY_STRUCTURES:
			if dimension == 1:
				if not all(isinstance(point, Real) for point in points):
					raise ValueError('points have inconsistent dimension')
			else:
				if not all(len(point) == dimension for point in points):
					raise ValueError('points have inconsistent dimension')
		
		super().__init__(dimension, norm = norm, metric = metric)

	def project(
			self, 
			quantity: Real | Vector,
			*,
			rank: Integral = 1,
			) -> Real | Vector:
		return nsmallest(rank, self.points, key = lambda x: self.metric(x, quantity))[-1]

class IntegerLattice(Space):
	def project(self, quantity: Real | Vector) -> Real | Vector:

		if isinstance(quantity, Real):	# scalar
			return round(quantity)
		else:	# vector
			return type(quantity)(round(scalar) for scalar in quantity)

class TransformedSpace(Space):
	def __init__(
			self, 
			space: Space, 
			forward_transform: Callable[[Real], Real] | Callable[[Vector], Vector], 
			inverse_transform: Callable[[Real], Real] | Callable[[Vector], Vector] | None = None, 
			) -> None:
		self.space = space
		self.forward_transform = forward_transform
		self.inverse_transform = inverse_transform
		super().__init__(space.dimension, norm = space.norm, metric = space.metric)
	
	def project(self, quantity: Real | Vector, return_preimage: bool = False, *args, **kwargs) -> Real | Vector:
		if self.inverse_transform:
			preimage = self.space.project(self.inverse_transform(quantity), *args, **kwargs)
		else:
			#preimage = optimize...
			raise NotImplementedError
		
		return preimage if return_preimage else self.forward_transform(preimage)

class AffineLattice(TransformedSpace):
	def __init__(self, 
			basis: Real | Sequence[Vector], 
			offset: Real | Vector, 
			*, 
			norm: Norm = lp_norm, 
			metric: Metric = lp_metric
			) -> None:
		if isinstance(basis, Real) and isinstance(offset, Real):	# scalar
			dimension = 1
		elif isinstance(basis, Sequence) and isinstance(offset, Vector):	# vector
			dimension = len(offset)
			if VERIFY_STRUCTURES and not all (len(vector) == dimension for vector in basis):
				raise ValueError('basis and offset have incompatible dimension')
		else:
			raise ValueError('basis & offset must be either Real & Real or Sequence[Vector] & Vector')
		
		space = IntegerLattice(dimension, norm = norm, metric = metric)

		self.basis = basis
		self.offset = offset
		super().__init__(space, self.forward_transform, self.inverse_transform)
	
	def forward_transform(self, quantity: Real | Vector) -> Real | Vector:
		if self.dimension == 1:	# scalar
			return quantity * self.basis + self.offset
		else:	# vector
			raise NotImplementedError
	
	def inverse_transform(self, quantity: Real | Vector) -> Real | Vector:
		# NOTE: this function uses a precompiled self._inverse_basis, so it doesnt have to compute the inverse of the basis everytime it is called
	
		if self.dimension == 1:	# scalar
			return (quantity - self.offset) / self.basis
		else:	# vector
			raise NotImplementedError
	
# convenience functions -------------------------------------------------------

def quantize(number: Real, quantum: Real = 1, offset: Real = 0, *args, **kwargs):
	'quantize a number to multiples of quantum'
	return AffineLattice(quantum, offset).project(number, *args, **kwargs)

def qdivmod(dividend, divisor, *args, **kwargs) -> tuple[Real, Real]:
	'like divmod, but with quantization'
	quotient = quantize(dividend/divisor, *args, **kwargs)
	remainder = dividend - quotient * divisor
	return quotient, remainder

def qround(number: Real, digits: Real = 0, *args, **kwargs):
	return quantize(number, quantum = 10 ** -digits, *args, **kwargs)
