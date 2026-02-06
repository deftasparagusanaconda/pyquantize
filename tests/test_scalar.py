import pyquantize as pq
import math

INF = float('inf')

def test_FinitePoints():
	space = pq.FinitePoints({-2, 0, 1, 3, 4, 5})

	# general
	assert space.project(0) == 0
	
	# with rank
	#assert space.project(1, rank = 2) == 0
	
	# -ve rank
	#assert space.project(4, rank = -1) == -2	# -ve rank gives nth farthest, instead of nth nearest
	#assert space.project(5, rank = -2) == 0
	
	# inf input
	assert space.project(-INF) == -2
	assert space.project(INF) == 5
	#assert space.project(-INF, rank = 2) == 0
	#assert space.project(INF, rank = 2) == 4
	#assert space.project(-INF, rank = -1) == 5
	#assert space.project(INF, rank = -1) == -2
	#assert space.project(-INF, rank = -2) == 4
	#assert space.project(INF, rank = -2) == 0
	
	# tie conditions
	space.project(2)
	space.project(-1)

def test_AffineLattice():
	space = pq.AffineLattice(2, 2.5)	# {…, -1.5, 0.5, 2.5, 4.5, 6.5, …}
	
	# general
	assert space.project(0) == 0.5
	assert space.project(2.5) == 2.5
	assert space.project(2.5) == 2.5
	
	# with rank
	#assert space.project(0.6, rank = 2) == 2.5
	
	# -ve rank
	#assert space.project(0.0, rank = -1) == -INF
	#assert space.project(-0.0, rank = -1) == INF
	#assert space.project(0.0, rank = -2) == INF
	#assert space.project(-0.0, rank = -2) == -INF
	
	# inf input
	assert space.project(-INF) == -INF
	assert space.project(INF) == INF
	#assert space.project(-INF, rank = 2) == -INF
	#assert space.project(INF, rank = 2) == INF
	#assert space.project(-INF, rank = -1) == INF
	#assert space.project(INF, rank = -1) == -INF
	#assert space.project(-INF, rank = -2) == INF
	#assert space.project(INF, rank = -2) == -INF
	
	# tie conditions
	space.project(3.5)
	space.project(-0.5)

def test_IntegerLattice():
	space = pq.IntegerLattice(1)
	
	# general
	assert space.project(0) == 0
	assert space.project(0.75) == 1
	
	# with rank
	#assert space.project(0.1, rank = 2) == 1
	#assert space.project(-0.1, rank = 2) == -1

	# -ve rank
	#assert space.project(0.0, rank = -1) == -INF
	#assert space.project(-0.0, rank = -1) == INF
	#assert space.project(0.0, rank = -2) == INF
	#assert space.project(-0.0, rank = -2) == -INF
	
	# inf input
	assert space.project(-INF) == -INF
	assert space.project(INF) == INF
	#assert space.project(-INF, rank = 2) == -INF
	#assert space.project(INF, rank = 2) == INF
	#assert space.project(-INF, rank = -1) == INF
	#assert space.project(INF, rank = -1) == -INF
	#assert space.project(-INF, rank = -2) == INF
	#assert space.project(INF, rank = -2) == -INF

	# tie conditions
	assert space.project(0.5) == 0
	assert space.project(-0.5) == 0

def test_TransformedSpace():
	space = pq.TransformedSpace(pq.IntegerLattice(1), lambda x: x ** 3, math.cbrt)
	# {…, -9, -1, 0, 1, 9, …}

	# general
	assert space.project(0) == 0
	assert space.project(1) == 1
	assert space.project(7) == 8
	
	# with rank
	#assert space.project(1, rank = 2) == 0
	#assert space.project(-9, rank = 2) == -1

	# -ve rank
	#assert space.project(0.0, rank = -1) == -INF
	#assert space.project(-0.0, rank = -1) == INF
	#assert space.project(0.0, rank = -2) == INF
	#assert space.project(-0.0, rank = -2) == -INF
	
	# inf input
	assert space.project(-INF) == -INF
	assert space.project(INF) == INF
	#assert space.project(-INF, rank = 2) == -INF
	#assert space.project(INF, rank = 2) == INF
	#assert space.project(-INF, rank = -1) == INF
	#assert space.project(INF, rank = -1) == -INF
	#assert space.project(-INF, rank = -2) == INF
	#assert space.project(INF, rank = -2) == -INF

	# tie conditions, i think. probably isnt a tie in the new transformed space lul
	space.project(0.5)
	space.project(-0.5)
