cache = {}

def calc_pow(base: int, exp: int) -> int:
    key = f"pow:{base}^{exp}"
    if key in cache:
        return cache[key]
    result = base ** exp
    cache[key] = result
    return result

def calc_fibonacci(n: int) -> int:
    key = f"fibonacci:{n}"
    if key in cache:
        return cache[key]
    if n <= 1:
        cache[key] = n
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    cache[key] = b
    return b

def calc_factorial(n: int) -> int:
    key = f"factorial:{n}"
    if key in cache:
        return cache[key]
    result = 1
    for i in range(1, n + 1):
        result *= i
    cache[key] = result
    return result