import math
from abc import ABC, abstractmethod
#from .typehints import Vector, Norm, Metric
from numbers import Real, Integral
from collections.abc import Callable, Collection, Sequence
from heapq import nsmallest
from typing import TypeAlias

# an int or a float, usually. not a bool though heh. stuff like 1, 2, -1, 1.0, 5.5, …
#Scalar: TypeAlias = Real

# a recursive sequence of scalar values. this actually admits a ragged tensor, interestingly.
Tensor: TypeAlias = Real | Sequence['Tensor']

# a 1-rank tensor
Vector: TypeAlias = Sequence[Real]

# a distance-like function that collapses scalars and vectors to a +ve real number
Norm  : TypeAlias = Callable[[Real | Vector], Real]

# a comparison function that returns the distance between two points
Metric: TypeAlias = Callable[[Real, Real], Real] | Callable[[Vector, Vector], Real]



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

	@abstractmethod
	def project(self, quantity: Real | Vector) -> Real | Vector:
		...
	
	#def show(self, center: Real, point_count: int = 5) -> None:
	#	'show some points on the space to get a feel for what its like'
	#	points = {self.project(0, rank = i) for i in range(1, point_count + 1)}
	#	print('{' + …, … + '}')
	
class IntegerLattice(Space):
	def project(self, quantity: Real | Vector) -> Real | Vector:
		return round(quantity) if isinstance(quantity, Real) else type(quantity)(round(scalar) for scalar in quantity)
	
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
	
	def project(self, quantity: Real | Vector) -> Real | Vector:
		if self.inverse_transform:
			return self.forward_transform(round(self.inverse_transform(quantity)))
		else:
			raise NotImplementedError

class AffineLattice(TransformedSpace):
	def __init__(self, 
			  quantum: Real | Vector, 
			  offset: Real | Vector, 
			  *, 
			  norm: Norm = lp_norm, 
			  metric: Metric = lp_metric
			  ) -> None:
		self.quantum = quantum
		self.offset = offset
		
		forward_transform = lambda x: x * self.quantum + self.offset
		inverse_transform = lambda x: (x - self.offset) / self.quantum
		
		dimension = len(quantum) if isinstance(quantum, Sequence) else 1
		space = IntegerLattice(dimension, norm = norm, metric = metric)

		super().__init__(space, forward_transform, inverse_transform)

class FinitePoints(Space):
	def __init__(self,
			points: Collection[Real] | Collection[Vector],
			*, 
			norm: Norm = lp_norm, 
			metric: Metric = lp_metric,
			) -> None:
		self.points: Collection[Real] | Collection[Vector] = points
		some_point = next(iter(points))
		dimension: Integral = len(some_point) if isinstance(some_point, Sequence) else 1
		super().__init__(dimension)

	def project(
			self, 
			quantity: Real | Vector,
			*,
			rank: Integral = 1,
			) -> Real | Vector:
		return nsmallest(rank, self.points, key = lambda x: self.metric(x, quantity))[-1]

'''
def qdivmod(dividend, divisor, *args, **kwargs):
	result = nearest(dividend/divisor, *args, **kwargs)
	return result, dividend-result*divisor

def qround(number: int | float, digits: int | float = 0, *args, **kwargs):
	return nearest(number, quantum = 10 ** -digits, *args, **kwargs)
'''

