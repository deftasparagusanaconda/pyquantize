from typing import Callable
from .misc import Space, lp_norm, lp_metric
from .typehints import Scalar, Vector, Norm, Metric
from .lattice import Lattice

class TransformedLattice(Space):
	def __init__(self, 
			transform: Callable[[Scalar], Scalar] | Callable[[Vector], Vector], 
			lattice: Lattice = None
			) -> None:
		self.transform: Callable[[Scalar], Scalar] | Callable[[Vector], Vector] = transform
		self.lattice: Lattice = Lattice() if lattice is None else lattice
		super().__init__(lattice.dimension, norm = lattice.norm, metric = lattice.metric)
		
	def project(self, 
			quantity: Scalar | Vector,
			return_scaled: bool = False,
			bounds: tuple[int, int] = (-2 ** 30 + 1, 2 ** 30 - 1)
			) -> Scalar | Vector:
		"""quantize to an arbitrary grid. the grid is determined by scaler which scales the integers to a set of numbers on the real number line
		
		parameters
		----------
		
		number: int or float
			the number to be quantized
		
		scaler: function (int → float)
			a function that scales the integers to a set of real numbers. this is how we describe the grid. mathematically, it is ℤ → ℝ. for the function to be 100% accurate, the scaler should be monotonic (i.e. either never decreasing or never increasing) 
		
		scaler_is_monotonic: bool, default = True
			if the scaler is monotonic, the answer is guaranteed to be accurate and fast (a greedy iterative optimization algorithm with difference inference is used)
			if the scaler is not monotonic, the answer may or may not be the best answer, depending on the optimizer
		
		notes
		-----
		when scaler is not monotonic and 
		"""
		
		
		
		raise NotImplementedError
