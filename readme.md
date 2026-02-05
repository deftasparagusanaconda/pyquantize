# pyquantize

general-purpose [quantization](https://en.wikipedia.org/wiki/Quantization_(signal_processing)) 

features: 
- [directed rounding](https://en.wikipedia.org/wiki/Rounding#Directed_rounding_to_an_integer)
- [tie-breaking rounding](https://en.wikipedia.org/wiki/Rounding#Rounding_to_the_nearest_integer)
- [randomized rounding](https://en.wikipedia.org/wiki/Rounding#Randomized_rounding_to_an_integer)
- [truncation](https://en.wikipedia.org/wiki/Truncation)
- [rounding to multiples](https://en.wikipedia.org/wiki/Rounding#Rounding_to_a_specified_multiple)

# how to install

install using [pip](https://en.wikipedia.org/wiki/Pip_(package_manager)). run this command in your terminal:
```shell
pip install pyquantize
```

(you may need to [set up a virtual environment](https://docs.python.org/3/library/venv.html#creating-virtual-environments))

<details><summary>alternatives</summary>

1. using python explicitly:
```shell
python -m pip install pyquantize
```

2. directly from the PyPI website: https://pypi.org/project/pyquantize/

3. directly from the latest github version:
```shell
git clone https://github.com/deftasparagusanaconda/pyquantize/
cd pyquantize
pip install .
```
</details>

# how to use



```python
import pyquantize as pq

# quantize to multiples of 0.8
pq.quantize_to_uniform_grid(3.14, 0.8)

# 3.2
```

`import pyquantize as pq`

```python
pq.
```

# tidbits 

to simulate rounding, try: 
```python
import pyquantize as pq

def qround(number, digits=0, *args, **kwargs):
	return pq.quantize(number, quantum=10**-digits, *args, **kwargs)

rounded_num = qround(2.34, 1, directed=True, mode='stochastic')
print(rounded_num)

# 2.3 or 2.4
```
unlike python's `round`, you can even round a number to a non-integer amount of digits!
```
rounded_num = qround(2.34, 1.5)
print(rounded_num)

# 2.2135943621178655
```

to simulate rounded division, try:
```python
def qdivmod(dividend, divisor, *args, **kwargs):
	result = quantize(dividend/divisor, *args, **kwargs)
	return result, dividend-result*divisor

rounded_answer = qdivmod(2.34, 1, directed=True, mode='stochastic')
print(rounded_answer)

# (1, 1.0) or (2, -0.5)
```
stochastic division. neat huh?? or try even-rounded integer division:

```
print(qdivmod(3, 2, mode='even'))
# (2, -1)
print(qdivmod(4, 2, mode='even'))
# (2, 0)
print(qdivmod(5, 2, mode='even'))
# (2, 1)
```

or check that stochastic mode works:

```python
count = 0
for i in range(10**5):
	count += quantize(0.9, directed=True, mode='stochastic')

print(count/10**5)
# ≈0.9
```

these patterns fall naturally out of pyquantize. i will add these functions formally in the future.

# how to uninstall

```shell
pip uninstall pyquantize
```

# the end ~
if you liked this, please please give me a star it really helps
