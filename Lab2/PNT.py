"""
Q1: Prime Number Testing
-------------------------
Compares two primality-testing algorithms by counting their basic
operations (step/frequency count) and plots the comparison.

Algorithm 1 - Naive Method:
    Checks divisibility of n by every integer from 2 to n-1.
    Time Complexity: O(n)

Algorithm 2 - Optimized Method:
    Checks divisibility of n only up to sqrt(n), because if n has a
    factor larger than sqrt(n), it must also have a corresponding
    factor smaller than sqrt(n). So checking beyond sqrt(n) is redundant.
    Time Complexity: O(sqrt(n))

Optional - Sieve of Eratosthenes:
    Generates ALL primes up to a limit in one pass by "crossing out"
    multiples of each prime found. Efficient when many primes are needed.
    Time Complexity: O(n log log n)

Student Code: 308
"""

import math
import time
import matplotlib
matplotlib.use("Agg")  # save plots to file instead of opening a window
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------
# Algorithm 1: Naive primality test
# ---------------------------------------------------------------------
def naive_is_prime_308(n_308):
    """Check primality by testing every divisor from 2 to n-1.
    Returns (is_prime, step_count)."""
    steps_308 = 0

    if n_308 < 2:
        return False, steps_308

    for i_308 in range(2, n_308):
        steps_308 += 1               # count each divisibility check
        if n_308 % i_308 == 0:
            return False, steps_308

    return True, steps_308


# ---------------------------------------------------------------------
# Algorithm 2: Optimized primality test (check up to sqrt(n))
# ---------------------------------------------------------------------
def optimized_is_prime_308(n_308):
    """Check primality by testing divisors only up to sqrt(n).
    Returns (is_prime, step_count)."""
    steps_308 = 0

    if n_308 < 2:
        return False, steps_308

    limit_308 = int(math.isqrt(n_308))
    for i_308 in range(2, limit_308 + 1):
        steps_308 += 1               # count each divisibility check
        if n_308 % i_308 == 0:
            return False, steps_308

    return True, steps_308


# ---------------------------------------------------------------------
# Optional: Sieve of Eratosthenes
# ---------------------------------------------------------------------
def sieve_of_eratosthenes_308(limit_308):
    """Return list of all primes up to (and including) limit_308,
    plus the number of "crossing out" operations performed."""
    steps_308 = 0
    is_prime_arr_308 = [True] * (limit_308 + 1)
    is_prime_arr_308[0:2] = [False, False]   # 0 and 1 are not prime

    for p_308 in range(2, int(math.isqrt(limit_308)) + 1):
        steps_308 += 1
        if is_prime_arr_308[p_308]:
            for multiple_308 in range(p_308 * p_308, limit_308 + 1, p_308):
                steps_308 += 1        # count every multiple crossed out
                is_prime_arr_308[multiple_308] = False

    primes_308 = [i_308 for i_308, flag_308 in enumerate(is_prime_arr_308) if flag_308]
    return primes_308, steps_308


# ---------------------------------------------------------------------
# Input: at least 10 numbers from the user
# ---------------------------------------------------------------------
def get_numbers_from_user_308():
    """Prompts the user for at least 10 numbers (comma separated)."""
    while True:
        raw_308 = input(
            "Enter at least 10 numbers separated by commas "
            "(e.g. 7,15,29,100,997,...): "
        ).strip()
        try:
            numbers_308 = [int(x_308.strip()) for x_308 in raw_308.split(",") if x_308.strip() != ""]
        except ValueError:
            print("Please enter valid integers separated by commas.")
            continue

        if len(numbers_308) < 10:
            print(f"You entered {len(numbers_308)} numbers. Please enter at least 10.")
            continue

        return numbers_308


# ---------------------------------------------------------------------
# Main driver
# ---------------------------------------------------------------------
def main_308():
    numbers_308 = get_numbers_from_user_308()

    results_308 = []   # will hold dicts of results for table + plotting

    print("\n" + "=" * 90)
    print(f"{'n':>10} | {'Naive?':>8} | {'Naive Steps':>12} | {'Naive Time(s)':>14} | "
          f"{'Opt?':>6} | {'Opt Steps':>10} | {'Opt Time(s)':>12}")
    print("=" * 90)

    for n_308 in numbers_308:
        start_308 = time.perf_counter()
        naive_result_308, naive_steps_308 = naive_is_prime_308(n_308)
        naive_time_308 = time.perf_counter() - start_308

        start_308 = time.perf_counter()
        opt_result_308, opt_steps_308 = optimized_is_prime_308(n_308)
        opt_time_308 = time.perf_counter() - start_308

        results_308.append({
            "n": n_308,
            "naive_prime": naive_result_308,
            "naive_steps": naive_steps_308,
            "naive_time": naive_time_308,
            "opt_prime": opt_result_308,
            "opt_steps": opt_steps_308,
            "opt_time": opt_time_308,
        })

        print(f"{n_308:>10} | {str(naive_result_308):>8} | {naive_steps_308:>12} | "
              f"{naive_time_308:>14.8f} | {str(opt_result_308):>6} | {opt_steps_308:>10} | "
              f"{opt_time_308:>12.8f}")

    print("=" * 90)

    # -------------------------------------------------------------
    # Optional: Sieve of Eratosthenes up to the largest number given
    # -------------------------------------------------------------
    max_n_308 = max(numbers_308)
    primes_308, sieve_steps_308 = sieve_of_eratosthenes_308(max_n_308)
    print(f"\n[Sieve of Eratosthenes] Primes up to {max_n_308} "
          f"(found in {sieve_steps_308} steps):")
    print(primes_308)

    # -------------------------------------------------------------
    # Graph: steps taken by naive vs optimized method per input
    # -------------------------------------------------------------
    sorted_results_308 = sorted(results_308, key=lambda r_308: r_308["n"])
    x_vals_308 = [r_308["n"] for r_308 in sorted_results_308]
    naive_steps_list_308 = [r_308["naive_steps"] for r_308 in sorted_results_308]
    opt_steps_list_308 = [r_308["opt_steps"] for r_308 in sorted_results_308]

    plt.figure(figsize=(9, 6))
    plt.plot(x_vals_308, naive_steps_list_308, marker="o", label="Naive Method O(n)")
    plt.plot(x_vals_308, opt_steps_list_308, marker="s", label="Optimized Method O(sqrt(n))")
    plt.xlabel("Input number (n)")
    plt.ylabel("Step / Frequency Count")
    plt.title("Prime Testing: Naive vs Optimized - Step Count Comparison (Roll No. 308)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig("prime_step_comparison_308.png", dpi=150)
    print("\nGraph saved as prime_step_comparison_308.png")

    # -------------------------------------------------------------
    # Analysis / Conclusion
    # -------------------------------------------------------------
    # CONCLUSION:
    # 1. The Naive Method's step count grows linearly with n (O(n)).
    #    As n increases, the number of divisibility checks increases
    #    proportionally, making it slow for large numbers.
    # 2. The Optimized Method's step count grows proportional to sqrt(n)
    #    (O(sqrt(n))), which is dramatically fewer steps for large n.
    #    E.g. for n = 1,000,000: naive ~ 999,998 checks vs optimized ~ 1000 checks.
    # 3. The Sieve of Eratosthenes is best when MANY primes are needed at
    #    once (e.g. all primes up to N), since it computes them all in a
    #    single O(n log log n) pass rather than testing each number
    #    individually.
    # 4. Conclusion: For a single primality check, the Optimized (sqrt n)
    #    method is faster. For generating a range/list of primes, the
    #    Sieve of Eratosthenes is the most efficient choice.


if __name__ == "__main__":
    main_308()