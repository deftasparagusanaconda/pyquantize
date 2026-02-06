__version__ = '0.3.0'

# NOTE: numpy is lazily loaded in AffineLattice.forward_transform and AffineLattice.inverse_transform
# NOTE: metric and norm are not properly implemented yet. only FinitePoints follows them for now
# NOTE: we do NOT handle anything that requires optimization. for now... hehe

# NOTE: we only do metric projections (i.e. choosing the closest point) for now. later, ill generalize to any projection (the idempotent operation, like from abstract algebra) that isnt necessarily the metrically closest

import math
from abc import ABC, abstractmethod
from numbers import Real, Integral
from collections.abc import Callable, Sequence
import heapq	# for nsmallest and nlargest in FinitePoints
from typing import TypeAlias, Literal
import random

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

_np = None
_numpy_checked: bool = False

def _get_numpy():
	global _np, _numpy_checked
	
	if _numpy_checked:
		return _np
	
	_numpy_checked = True
	
	try:
		import numpy as _np
	except ImportError:
		return None	
'''	
def lp_norm(quantity: Real | Vector, p: Real = 2) -> Real:
	if isinstance(quantity, Real):
		return abs(quantity) 
	if p == 2:
		return math.hypot(*quantity)
	return sum(abs(scalar) ** p for scalar in quantity) ** (1 / p)

def lp_metric(a: Real | Vector, b: Real | Vector, p: Real = 2) -> Real:
	if isinstance(a, Real):
		return abs(a - b)
	return lp_norm(tuple(x - y for x, y in zip(a, b, strict = True)), p)
'''
def vec_add_vec(v1: Vector, v2: Vector) -> Vector: 
	return type(quantity)(s1 + s2 for s1, s2 in zip(v1, v2, strict = True))

def vec_sub_vec(v1: Vector, v2: Vector) -> Vector:
	return type(quantity)(s1 - s2 for s1, s2 in zip(v1, v2, strict = True))

def vec_mul_mat(vec: Vector, mat: Sequence[Vector]) -> Vector:
	# ai-generated slop, this
	return type(vec)(sum(m*v for m,v in zip(row, vec, strict = True)) for row in mat)

def vec_div_mat(vec: Vector, mat: Sequence[Vector]) -> Vector:
	# ai-generated slop, this

	n = len(vec)
	# create augmented matrix [mat | vec]
	A = [row[:] + [val] for row,val in zip(mat, vec, strict = True)]
	
	# forward elimination
	for i in range(n):
		if A[i][i] == 0:
			for k in range(i+1, n):
				if A[k][i] != 0:
					A[i], A[k] = A[k], A[i]
					break
			else:
				raise ValueError("singular matrix, cannot solve")
		pivot = A[i][i]
		for j in range(i, n+1):
			A[i][j] /= pivot
		for k in range(i+1, n):
			factor = A[k][i]
			for j in range(i, n+1):
				A[k][j] -= factor * A[i][j]

	# back substitution
	x = [0]*n
	for i in range(n-1, -1, -1):
		x[i] = A[i][n] - sum(A[i][j]*x[j] for j in range(i+1, n))
	
	return x

# classes ---------------------------------------------------------------------

class Space(ABC):
	'a discrete space'
	def __init__(self, dimension: Integral):
		self.dimension: Integral = dimension
		#self.norm: Norm = norm
		#self.metric: Metric = metric

	# make __mul__ and __rmul__ so we can have product spaces, perhaps? that would be cool

	@abstractmethod
	def project(self, quantity: Real | Vector) -> Real | Vector:
		'project a scalar or a vector onto the nearest point in the discrete space. formally, this is known as a metric projection'
		...
	
	#def show(self, center: Real, point_count: int = 5) -> None:
	#	'show some points on the space to get a feel for what its like'
	#	points = {self.project(0) for i in range(1, point_count + 1)}
	#	print('{' + …, … + '}')
	
class FinitePoints(Space):
	def __init__(self, points: set[Real] | set[Vector]) -> None:
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
		
		super().__init__(dimension)
	
	def project(self, quantity: Real | Vector) -> Real | Vector:
		if math.isinf(quantity):
			return (min if quantity < 0 else max)(self.points)
		
		key = lambda x: abs(x - quantity)	# we assume an euclidean space, with euclidean distance metric

		return heapq.nsmallest(1, self.points, key = key)[-1]

class IntegerLattice(Space):
	def project(self, 
			quantity: Real | Vector, 
			tie: Literal  = 'even',	# what to do when quantity is equidistant to two integers
			) -> Real | Vector:
		"""project a number onto ℤⁿ
		
		parameters
		----------		
		quantity: scalar (int or float) or vector (sequence of scalar)
			the number or vector to project
		
		returns
		-------
		scalar (int or float) or vector (sequence of scalar)
			the project
		"""
		if not isinstance(quantity, Real):	# vector
			return type(quantity)(self.project(scalar) for scalar in quantity)

		# infinity is close only to itself, and nan should be propagated
		if not math.isfinite(quantity):
			return quantity

		fraction = quantity % 1
		
		if fraction == 0.5:	# a tie
			lower = math.floor(quantity)
			upper = math.ceil(quantity)
			
			if   tie == 'floor' : return lower
			elif tie == 'ceil'  : return upper
			elif tie == 'up'    : return lower if quantity < 0 else upper
			elif tie == 'down'  : return lower if quantity > 0 else upper
			elif tie == 'even'  : return lower if lower % 2 == 0 else upper
			elif tie == 'odd'   : return lower if lower % 2 == 1 else upper
			elif tie == 'random': return random.choice(lower, upper)
			else: 
				raise ValueError("tie can be one of {'floor', 'ceil', 'up', 'down', 'even', 'odd', 'random'}")
		else:
			return round(quantity)

class TransformedSpace(Space):
	def __init__(
			self, 
			space: Space, 
			forward_transform: Callable[[Real], Real] | Callable[[Vector], Vector], 
			inverse_transform: Callable[[Real], Real] | Callable[[Vector], Vector], 
			) -> None:
		self.space = space
		self.forward_transform = forward_transform
		self.inverse_transform = inverse_transform
		super().__init__(space.dimension)
	
	def project(self, quantity: Real | Vector, *args, return_preimage: bool = False, **kwargs) -> Real | Vector:
		
		#if self.inverse_transform:
		#	preimage = self.space.project(self.inverse_transform(quantity), *args, **kwargs)
		#else:
		#	# since we dont have an inverse transform, we have to perform discrete optimization
		#	# unfortunately, we might not always get a globally optimum result.
		#	raise NotImplementedError('i havent implemented discrete optimization yet')

		preimage = self.space.project(self.inverse_transform(quantity), *args, **kwargs)
		return preimage if return_preimage else self.forward_transform(preimage)

class AffineLattice(TransformedSpace):
	def __init__(self, basis: Real | Sequence[Vector], offset: Real | Vector) -> None:
		if isinstance(basis, Real) and isinstance(offset, Real):	# scalar
			dimension = 1
		elif isinstance(basis, Sequence) and isinstance(offset, Vector):	# vector
			dimension = len(offset)
			if VERIFY_STRUCTURES and not all (len(vector) == dimension for vector in basis):
				raise ValueError('basis and offset have incompatible dimension')
		else:
			raise ValueError('basis & offset must be either Real & Real or Sequence[Vector] & Vector')
		
		space = IntegerLattice(dimension)
		
		self.basis = basis
		self.offset = offset
		super().__init__(space, self.forward_transform, self.inverse_transform)
	
	def forward_transform(self, quantity: Real | Vector) -> Real | Vector:
		if self.dimension == 1:	# scalar
			return quantity * self.basis + self.offset	# you could use math.fma for this, yknow
		else:	# vector
			if _get_numpy():
				return _np.add(_np.dot(self.basis, quantity), self.offset)
			else:
				return vec_add_vec(vec_mul_mat(quantity, self.basis), self.offset)
	
	def inverse_transform(self, quantity: Real | Vector) -> Real | Vector:
		# NOTE: this function uses a precompiled self._inverse_basis, so it doesnt have to compute the inverse of the basis everytime it is called
	
		if self.dimension == 1:	# scalar
			return (quantity - self.offset) / self.basis
		else:	# vector
			if _get_numpy():
				return _np.linalg.solve(self.basis, _np.subtract(quantity, self.offset)) 
			else:
				return vec_div_mat(vec_sub_vec(quantity, self.offset), self.basis)
	
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

# clean up the module's autocomplete ------------------------------------------

__dir__ = lambda: [
		# classes
		'IntegerLattice'  ,
		'TransformedSpace',
		'AffineLattice'   ,
		'FinitePoints'	,
		
		# functions
		'quantize'		,
		'qdivmod'		 ,
		'qround'		  ,
		]
