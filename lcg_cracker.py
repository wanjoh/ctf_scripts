# https://tailcall.net/posts/cracking-rngs-lcgs/

from math import gcd
from functools import reduce

INVALID = -1

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

def modinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n

def get_increment() -> int:
	if len(states) < 2:
		return INVALID 
	return (states[-1] - states[-2] * multiplier) % modulus

def get_modulus() -> int:
	if len(states) < 6:
		return INVALID
	diffs = [s1 - s0 for s0, s1 in zip(states, states[1:])]
	zeroes = [t2*t0 - t1*t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
	return abs(reduce(gcd, zeroes))
 
def get_multiplier() -> int:
	if len(states) < 3:
		return INVALID
	return ((states[2] - states[1]) * modinv(states[1] - states[0], modulus)) % modulus

def get_next_state(counter: int) -> None:
	states.append((states[counter-1]*multiplier + increment)%modulus)
	print(states[counter])

# has to be in increasing order
# todo: allow it to be in arbitrary order
states:list[int] = [4447428463934812555147781473004611200698863953626984879363850046291723672941678027862386495166363618, 7043182960087956946369805110677184291199189006882624131905910985158749673619307810731137015160192386, 920869164375953580306792098951831118027312431868974521395273443837576727900366714264645513128926254]
modulus: int | None = 8471050156910645297199092184997948739352218102032175415195952882946019032523893352683847323674258073
increment : int | None = None
multiplier : int | None = None

if __name__ == "__main__":
	err = 0
	if modulus is None:
		modulus = get_modulus()
		err |= (modulus == INVALID)
	if multiplier is None:
		multiplier = get_multiplier()
		err |= (multiplier == INVALID)
	if increment is None:
		increment = get_increment()
		err |= (increment == INVALID)

	if err:
		print("one of the values is invalid")
		exit()
	counter = len(states)
	while input() != "q":
		get_next_state(counter)
		counter += 1

print(states, multiplier, increment)