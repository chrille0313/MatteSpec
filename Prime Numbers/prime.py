from Timing.timing import timing


@timing
def primes(n):
	isPrime = [True] * (n + 1)
	isPrime[0] = False
	isPrime[1] = False

	i = 2
	while i * i <= n:
		if isPrime[i]:
			for j in range(i * i, n + 1, i):
				isPrime[j] = False

		i += 1

	return isPrime


@timing
def is_prime(n):
	if n == 2:
		return True
	elif n & 1 == 0 or n < 2:
		return False

	d = 3
	while d * d <= n:
		if n % d == 0:
			return False
		d += 2

	return True


# primes(3314192745)
# print(is_prime(30313))
