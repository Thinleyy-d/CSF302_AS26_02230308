import time
import math


def NaiveTrialDivision_308(n):
    # Checks every number from 2 to n-1
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


def OptimizedTrialDivision_308(n):
    # Only checks up to the square root of n
    if n < 2:
        return False
    limit_308 = int(math.sqrt(n)) + 1
    for i in range(2, limit_308):
        if n % i == 0:
            return False
    return True


def SieveOfEratosthenes_308(n):
    is_prime_308 = [True] * (n + 1)
    is_prime_308[0] = False
    if n >= 1:
        is_prime_308[1] = False

    for i in range(2, int(math.sqrt(n)) + 1):
        if is_prime_308[i]:
            for j in range(i * i, n + 1, i):
                is_prime_308[j] = False

    primes_308 = [i for i, val in enumerate(is_prime_308) if val]
    return primes_308


def Main_308():
    sizes_308 = [10000, 50000, 100000, 500000, 1000000]

    # Naive method is O(n^2) overall, so it becomes too slow for
    # very large N. We skip it above this limit and note it in the table.
    naive_limit_308 = 100000

    print(f"{'N':<10}{'Naive (s)':<18}{'Optimized (s)':<18}{'Sieve (s)':<18}")
    print("-" * 64)

    for n_308 in sizes_308:
        # ---- Naive Trial Division ----
        if n_308 <= naive_limit_308:
            start_308 = time.time()
            naive_primes_308 = [x for x in range(2, n_308 + 1) if NaiveTrialDivision_308(x)]
            end_308 = time.time()
            naive_time_308 = f"{end_308 - start_308:.6f}"
        else:
            naive_time_308 = "skipped (too slow)"

        # ---- Optimized Trial Division ----
        start_308 = time.time()
        optimized_primes_308 = [x for x in range(2, n_308 + 1) if OptimizedTrialDivision_308(x)]
        end_308 = time.time()
        optimized_time_308 = f"{end_308 - start_308:.6f}"

        # ---- Sieve of Eratosthenes ----
        start_308 = time.time()
        sieve_primes_308 = SieveOfEratosthenes_308(n_308)
        end_308 = time.time()
        sieve_time_308 = f"{end_308 - start_308:.6f}"

        print(f"{n_308:<10}{naive_time_308:<18}{optimized_time_308:<18}{sieve_time_308:<18}")


if __name__ == "__main__":
    Main_308()