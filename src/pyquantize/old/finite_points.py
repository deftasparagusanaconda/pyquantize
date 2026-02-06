from collections.abc import Collection
from .misc import Space, lp_norm, lp_metric
from .typehints import Scalar, Vector, Norm, Metric
from heapq import nsmallest
from numbers import Integral
from typing import Literal

class FinitePoints(Space):
	def __init__(
			self, 
			points: Collection[Scalar] | Collection[Vector] = None, 
			*, 
			norm: Norm = lp_norm,
			metric: Metric = lp_metric,
			):
		super().__init__(norm, metric)
		self.points: Collection[Scalar] | Collection[Vector] = set() if points is None else points
		
		
	def project(self,
			quantity: Scalar | Vector,
			mode    : Literal           = 'rank',
			tie     : Literal           = 'even',
			rank    : Integral          = 1,
			) -> Scalar | Vector:
		"""quantize a number to a set of values. finds the number in the set closest to the given number. 
		
		parameters
		----------
		number: int or float
			the value to quantize
		
		returns
		-------
		int or float
			the quantized value
		
		examples
		--------
		
		
		notes
		-----
		"""
		
		if mode == 'rank':
			return nsmallest(rank, self.points, key = lambda x: self.metric(x, quantity))[-1]
