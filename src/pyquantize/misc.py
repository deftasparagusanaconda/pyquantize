from abc import ABC, abstractmethod
from .typehints import Scalar, Vector, Norm, Metric
from numbers import Real

def lp_norm(quantity: Scalar | Vector, p: Real = 2) -> Real:
	if isinstance(quantity, Scalar):
		return abs(quantity) 
	else:
		return math.hypot(*quantity) if p == 2 else sum(scalar ** p for scalar in quantity) ** (1 / p)

def lp_metric(a: Scalar | Vector, b: Scalar | Vector, p: Real = 2) -> Real:
	# lets just assume a and b are same type. im not gonna assert it or raise an exception here. deal with it.
	#if isinstance(a, Scalar):
	raise NotImplementedError	
	
class Space(ABC):
    def __init__(self, norm: Norm = lp_norm, metric: Metric = lp_metric):
        self.norm = norm
        self.metric = metric

    @abstractmethod
    def project(self, quantity: Scalar | Vector) -> Scalar | Vector:
        ...

'''
def qdivmod(dividend, divisor, *args, **kwargs):
	result = nearest(dividend/divisor, *args, **kwargs)
	return result, dividend-result*divisor

def qround(number: int | float, digits: int | float = 0, *args, **kwargs):
	return nearest(number, quantum = 10 ** -digits, *args, **kwargs)
'''

