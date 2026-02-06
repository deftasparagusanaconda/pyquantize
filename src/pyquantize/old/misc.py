import math
from abc import ABC, abstractmethod
from .typehints import Scalar, Vector, Norm, Metric
from numbers import Real, Integral

def lp_norm(quantity: Scalar | Vector, p: Real = 2) -> Real:
	if isinstance(quantity, Real):
		return abs(quantity) 
	if p == 2:
		return math.hypot(*quantity)
	return sum(abs(scalar) ** p for scalar in quantity) ** (1 / p)

def lp_metric(a: Scalar | Vector, b: Scalar | Vector, p: Real = 2) -> Real:
	if isinstance(a, Real):
		return abs(a - b)
	return lp_norm(tuple(x - y for x, y in zip(a, b)), p)

class Space(ABC):
	def __init__(self, dimension: Integral, *, norm: Norm = lp_norm, metric: Metric = lp_metric):
		self.dimension: Integral = dimension
		self.norm: Norm = norm
		self.metric: Metric = metric

	@abstractmethod
	def project(self, quantity: Scalar | Vector) -> Scalar | Vector:
		...

	def show_(self, center: Scalarpoint_count: int = 5) -> None:
		'show some points on the space to get a feel for what its like'
		points = {self.project(0, rank = i) for i in range(1, point_count + 1)}
		print('{' + …, … + '}')
	
'''
def qdivmod(dividend, divisor, *args, **kwargs):
	result = nearest(dividend/divisor, *args, **kwargs)
	return result, dividend-result*divisor

def qround(number: int | float, digits: int | float = 0, *args, **kwargs):
	return nearest(number, quantum = 10 ** -digits, *args, **kwargs)
'''

