from pyquantize import quantize
from math import copysign

def is_neg_zero(x):
	return x == 0 and copysign(1, x) == -1

def is_pos_zero(x):
	return x == 0 and copysign(1, x) == 1

test_set = [-1.5, -1.25, -1, -0.75, -0.5, -0.25, -0.0, 0, 0.25, 0.5, 0.75, 1, 1.25, 1.5]
modes = ['threshold', 'floor', 'ceil', 'toward', 'away', 'even', 'odd', 'alternate', 'random', 'stochastic']

def test_defaults():
	expects = [-2, -1, -1, -1, -0.0, -0.0, -0.0, 0, 0, 0, 1, 1, 1, 2]
	results = [quantize(num) for num in test_set]

	for expect, result in zip(expects,results):
		assert result == expect
	
	for result in results[4:7]:
		assert is_neg_zero(result)

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
	assert quantize(0.7, threshold=threshold, mode=mode) in [0,1]
	assert quantize(0.8, threshold=threshold, mode=mode) == 1
	assert quantize(0.9, threshold=threshold, mode=mode) == 1
	assert quantize(1.0, threshold=threshold, mode=mode) == 1

def test_floor_mode():
	mode = 'floor'
	assert quantize(-1.5 , mode=mode) == -2
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
	assert quantize( 1.5 , mode=mode) ==  1

def test_ceil_mode():
	mode = 'ceil'
	assert quantize(-1.5 , mode=mode) == -1
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
	assert quantize( 1.5 , mode=mode) ==  2

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

def test_toward_mode():
	mode = 'toward'

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
"""
def test_alternate_mode():
	mode = 'alternate'
	quantize.alternate_last = False
	
	expects = [-1, -1, -1, -0.0, -0.0, -0.0, -0.0, 0, 0, 0, 0, 1, 1, 1]
	results = [quantize(num, mode=mode) for num in test_set]

	for result, expect in zip(results, expects):
		assert result == expect

def test_random_mode():
def test_stochastic_mode():

def test_directed_threshold_mode():
"""
def test_directed_floor_mode():
	directed = True
	mode = 'floor'
	assert quantize(-1.5 , directed=directed, mode=mode) == -2
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
	assert quantize( 1.5 , directed=directed, mode=mode) ==  1

def test_directed_ceil_mode():
	directed = True
	mode = 'ceil'
	assert quantize(-1.5 , directed=directed, mode=mode) == -1
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
	assert quantize( 1.5 , directed=directed, mode=mode) ==  2

def test_directed_toward_mode():
	directed = True
	mode = 'toward'
	centre = 0
	
	expects = [-1, -1, -1, -0.0, -0.0, -0.0, -0.0, 0, 0, 0, 0, 1, 1, 1]
	results = [quantize(num, centre=centre, directed=directed, mode=mode) for num in test_set]

	for result, expect in zip(results, expects):
		assert result == expect

def test_directed_away_mode():
	directed = True
	mode = 'away'
	centre = 0
	
	expects = [-2, -2, -1, -1, -1, -1, -0.0, 0, 1, 1, 1, 1, 2, 2]
	results = [quantize(num, centre=centre, directed=directed, mode=mode) for num in test_set]

	for result, expect in zip(results, expects):
		assert result == expect
"""
def test_directed_even_mode():
def test_directed_odd_mode():
"""
def test_directed_alternate_mode():
	from statistics import mean
	
	directed = True
	mode = 'alternate'

	things = [quantize(0.8, directed=directed, mode=mode) for i in range(10000)]

	avg = mean(things)

	assert 0 < avg < 1
	assert 0.4 < avg < 0.6
	assert 0.49 < avg < 0.51
	assert avg == 0.5
	assert sum(things[0::2]) == 0
	assert sum(things[1::2]) == 5000

def test_directed_random_mode():
	from statistics import mean

	directed = True
	mode = 'random'

	things = [quantize(0.8, directed=directed, mode=mode) for i in range(10000)]

	avg = mean(things)

	assert 0 < avg < 1
	assert 0.25 < avg < 0.75

def test_directed_stochastic_mode():
	from statistics import mean
	
	directed = True
	mode = 'stochastic'

	things = [quantize(0.8, directed=directed, mode=mode) for i in range(10000)]

	avg = mean(things)

	assert 0 < avg < 1
	assert 0.6 < avg < 1
