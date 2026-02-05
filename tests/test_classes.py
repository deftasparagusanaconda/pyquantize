import pyquantize as pq

def test_lattice():
	lattice = pq.Lattice()

	assert lattice.project(0.25) == 0
	assert lattice.project(0.75) == 1

def test_transformed_lattice():
	l = pq.TransformedLattice()
	
	assert l.project(0.25) == 0
	assert l.project(0.75) == 1

def test_finite_points():
	p = pq.FinitePoints({0, 1})
	
	assert p.project(0.25) == 0
	assert p.project(0.75) == 1
