from numbers import Real
from collections.abc import Sequence
from typing import TypeAlias, Callable

# an int or a float, usually. not a bool though heh. stuff like 1, 2, -1, 1.0, 5.5, …
Scalar: TypeAlias = Real

# a recursive sequence of scalar values. this actually admits a ragged tensor, interestingly.
Tensor: TypeAlias = Scalar | Sequence['Tensor']

# a 1-rank tensor
Vector: TypeAlias = Sequence[Scalar]

# a distance-like function that collapses scalars and vectors to a +ve real number
Norm  : TypeAlias = Callable[[Scalar | Vector], Real]

# a comparison function that returns the distance between two points
Metric: TypeAlias = Callable[[Scalar, Scalar], Scalar] | Callable[[Vector, Vector], Scalar]

