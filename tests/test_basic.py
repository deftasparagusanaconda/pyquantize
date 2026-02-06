import pyquantize as pq

def test_integer_lattice():
	space = pq.IntegerLattice(1)

	assert space.project(0.25) == 0
	assert space.project(0.75) == 1

def test_transformed_space():
	space = pq.TransformedSpace(pq.IntegerLattice(1), lambda x: x, lambda x: x)
	
	assert space.project(0.25) == 0
	assert space.project(0.75) == 1

def test_affine_lattice():
	space = pq.AffineLattice(1, 0)

	assert space.project(0.25) == 0
	assert space.project(0.75) == 1

def test_finite_points():
	space = pq.FinitePoints({0, 1})
	
	assert space.project(0.25) == 0
	assert space.project(0.75) == 1
