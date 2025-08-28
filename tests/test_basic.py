from pyquantize import quantize
from math import copysign

def test_defaults():
	assert quantize(-2   ) == -2
	assert quantize(-1.5 ) == -2
	assert quantize(-1   ) == -1
	assert quantize(-0.75) == -1
	assert quantize(-0.5 ) == -0.0
	assert quantize(-0.25) == -0.0
	assert quantize(-0.0 ) == -0.0
	assert quantize( 0   ) ==  0
	assert quantize( 0.25) ==  0
	assert quantize( 0.5 ) ==  0
	assert quantize( 0.75) ==  1
	assert quantize( 1   ) ==  1
	assert quantize( 1.5 ) ==  2
	assert quantize( 2   ) ==  2

def test_signed_zeroes():
	assert copysign(1, quantize( 0.1)) ==  1
	assert copysign(1, quantize(-0.1)) == -1

def test_threshold_mode():
	threshold = 0.7
	mode = 'threshold'
	assert quantize(0.0, threshold=threshold, mode=mode) == 0
	assert quantize(0.1, threshold=threshold, mode=mode) == 0
	assert quantize(0.2, threshold=threshold, mode=mode) == 0
	assert quantize(0.3, threshold=threshold, mode=mode) == 0
	assert quantize(0.4, threshold=threshold, mode=mode) == 0
	assert quantize(0.5, threshold=threshold, mode=mode) == 0
	assert quantize(0.6, threshold=threshold, mode=mode) == 0
	assert quantize(0.7, threshold=threshold, mode=mode) == 1
	assert quantize(0.8, threshold=threshold, mode=mode) == 1
	assert quantize(0.9, threshold=threshold, mode=mode) == 1
	assert quantize(1.0, threshold=threshold, mode=mode) == 1

def test_floor_mode():
	mode = 'floor'
	assert quantize(-1.25, mode=mode) == -1
	assert quantize(-1   , mode=mode) == -1
	assert quantize(-0.75, mode=mode) == -1
	assert quantize(-0.5 , mode=mode) == -1
	assert quantize(-0.25, mode=mode) == -0.0
	assert quantize(-0.0 , mode=mode) == -0.0
	assert quantize( 0.0 , mode=mode) ==  0.0
	assert quantize( 0.25, mode=mode) ==  0.0
	assert quantize( 0.5 , mode=mode) ==  0.0
	assert quantize( 0.75, mode=mode) ==  1
	assert quantize( 1   , mode=mode) ==  1
	assert quantize( 1.25, mode=mode) ==  1

def test_ceil_mode():
	mode = 'ceil'
	assert quantize(-1.25, mode=mode) == -1
	assert quantize(-1   , mode=mode) == -1
	assert quantize(-0.75, mode=mode) == -1
	assert quantize(-0.5 , mode=mode) == -0.0
	assert quantize(-0.25, mode=mode) == -0.0
	assert quantize(-0.0 , mode=mode) == -0.0
	assert quantize( 0.0 , mode=mode) ==  0.0
	assert quantize( 0.25, mode=mode) ==  0.0
	assert quantize( 0.5 , mode=mode) ==  1
	assert quantize( 0.75, mode=mode) ==  1
	assert quantize( 1   , mode=mode) ==  1
	assert quantize( 1.25, mode=mode) ==  1

def test_even_mode():
	mode = 'even'

	assert quantize(-1.5 , mode=mode) == -2
	assert quantize(-1.25, mode=mode) == -1
	assert quantize(-1   , mode=mode) == -1
	assert quantize(-0.75, mode=mode) == -1
	assert quantize(-0.5 , mode=mode) == -0.0
	assert quantize(-0.25, mode=mode) == -0.0
	assert quantize(-0.0 , mode=mode) == -0.0
	assert quantize( 0.0 , mode=mode) ==  0.0
	assert quantize( 0.25, mode=mode) ==  0.0
	assert quantize( 0.5 , mode=mode) ==  0.0
	assert quantize( 0.75, mode=mode) ==  1
	assert quantize( 1   , mode=mode) ==  1
	assert quantize( 1.25, mode=mode) ==  1
	assert quantize( 1.5 , mode=mode) ==  2

def test_odd_mode():
	mode = 'odd'

	assert quantize(-1.5 , mode=mode) == -1
	assert quantize(-1.25, mode=mode) == -1
	assert quantize(-1   , mode=mode) == -1
	assert quantize(-0.75, mode=mode) == -1
	assert quantize(-0.5 , mode=mode) == -1
	assert quantize(-0.25, mode=mode) == -0.0
	assert quantize(-0.0 , mode=mode) == -0.0
	assert quantize( 0.0 , mode=mode) ==  0.0
	assert quantize( 0.25, mode=mode) ==  0.0
	assert quantize( 0.5 , mode=mode) ==  1
	assert quantize( 0.75, mode=mode) ==  1
	assert quantize( 1   , mode=mode) ==  1
	assert quantize( 1.25, mode=mode) ==  1
	assert quantize( 1.5 , mode=mode) ==  1

def test_towards_mode():
	mode = 'towards'

	assert quantize(-1.5 , mode=mode) == -1
	assert quantize(-1.25, mode=mode) == -1
	assert quantize(-1   , mode=mode) == -1
	assert quantize(-0.75, mode=mode) == -1
	assert quantize(-0.5 , mode=mode) == -0.0
	assert quantize(-0.25, mode=mode) == -0.0
	assert quantize(-0.0 , mode=mode) == -0.0
	assert quantize( 0.0 , mode=mode) ==  0.0
	assert quantize( 0.25, mode=mode) ==  0.0
	assert quantize( 0.5 , mode=mode) ==  0.0
	assert quantize( 0.75, mode=mode) ==  1
	assert quantize( 1   , mode=mode) ==  1
	assert quantize( 1.25, mode=mode) ==  1
	assert quantize( 1.5 , mode=mode) ==  1

def test_away_mode():
	mode = 'away'
	
	assert quantize(-1.5 , mode=mode) == -2
	assert quantize(-1.25, mode=mode) == -1
	assert quantize(-1   , mode=mode) == -1
	assert quantize(-0.75, mode=mode) == -1
	assert quantize(-0.5 , mode=mode) == -1
	assert quantize(-0.25, mode=mode) == -0.0
	assert quantize(-0.0 , mode=mode) == -0.0
	assert quantize( 0.0 , mode=mode) ==  0.0
	assert quantize( 0.25, mode=mode) ==  0.0
	assert quantize( 0.5 , mode=mode) ==  1
	assert quantize( 0.75, mode=mode) ==  1
	assert quantize( 1   , mode=mode) ==  1
	assert quantize( 1.25, mode=mode) ==  1
	assert quantize( 1.5 , mode=mode) ==  2

def test_directed_floor_mode():
	directed = True
	mode = 'floor'
	assert quantize(-1.25, directed=directed, mode=mode) == -2
	assert quantize(-1   , directed=directed, mode=mode) == -1
	assert quantize(-0.75, directed=directed, mode=mode) == -1
	assert quantize(-0.5 , directed=directed, mode=mode) == -1
	assert quantize(-0.25, directed=directed, mode=mode) == -1
	assert quantize(-0.0 , directed=directed, mode=mode) == -0.0
	assert quantize( 0.0 , directed=directed, mode=mode) ==  0.0
	assert quantize( 0.25, directed=directed, mode=mode) ==  0
	assert quantize( 0.5 , directed=directed, mode=mode) ==  0
	assert quantize( 0.75, directed=directed, mode=mode) ==  0
	assert quantize( 1   , directed=directed, mode=mode) ==  1
	assert quantize( 1.25, directed=directed, mode=mode) ==  1

def test_directed_ceil_mode():
	directed = True
	mode = 'ceil'
	assert quantize(-1.25, directed=directed, mode=mode) == -1
	assert quantize(-1   , directed=directed, mode=mode) == -1
	assert quantize(-0.75, directed=directed, mode=mode) == -0.0
	assert quantize(-0.5 , directed=directed, mode=mode) == -0.0
	assert quantize(-0.25, directed=directed, mode=mode) == -0.0
	assert quantize(-0.0 , directed=directed, mode=mode) == -0.0
	assert quantize( 0.0 , directed=directed, mode=mode) ==  0.0
	assert quantize( 0.25, directed=directed, mode=mode) ==  1
	assert quantize( 0.5 , directed=directed, mode=mode) ==  1
	assert quantize( 0.75, directed=directed, mode=mode) ==  1
	assert quantize( 1   , directed=directed, mode=mode) ==  1
	assert quantize( 1.25, directed=directed, mode=mode) ==  2

def test_directed_alternate_mode():
	from statistics import mean
	
	directed = True
	mode = 'alternate'

	things = [quantize(0.8, directed=directed, mode=mode) for i in range(10000)]

	avg = mean(things)

	assert avg > 0
	assert avg < 1
	assert avg > 0.4
	assert avg < 0.6
	assert avg > 0.49
	assert avg < 0.51
	assert avg == 0.5
	assert sum(things[0::2]) == 0
	assert sum(things[1::2]) == 5000

def test_directed_random_mode():
	from statistics import mean

	directed = True
	mode = 'random'

	things = [quantize(0.8, directed=directed, mode=mode) for i in range(10000)]

	avg = mean(things)

	assert avg > 0
	assert avg < 1
	assert avg > 0.25
	assert avg < 0.75

def test_directed_stochastic_mode():
	from statistics import mean
	
	directed = True
	mode = 'stochastic'

	things = [quantize(0.8, directed=directed, mode=mode) for i in range(10000)]

	avg = mean(things)
	print(avg)

	assert avg > 0
	assert avg < 1
	assert avg > 0.6
	assert avg > 0.7
	assert avg < 0.9

