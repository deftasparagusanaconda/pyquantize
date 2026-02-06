__version__ = '0.3.0'

#from . import misc
#from .quantize import quantize
#from .lattice import Lattice
#from .transformed_lattice import TransformedLattice
#from .finite_points import FinitePoints
from .space import IntegerLattice, TransformedSpace, AffineLattice, FinitePoints

__dir__ = lambda: [
		#'quantize',
		'IntegerLattice',
		'TransformedSpace',
		'AffineLattice'
		'FinitePoints',
		#'misc'
		]
