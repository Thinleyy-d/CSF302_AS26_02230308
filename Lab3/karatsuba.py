"""
karatsuba.py
-------------
Multiplying large integers two ways:

1. Traditional grade-school multiplication -> O(n^2)
2. Karatsuba's divide-and-conquer algorithm -> O(n^1.585)

Numbers are handled as strings of digits so the code works for
integers far larger than a normal 32/64-bit int (Python ints are
already arbitrary precision, but we still implement grade-school
multiplication "by hand" using digit arrays, exactly like the
algorithm is taught, rather than just calling x * y).
"""

import time
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ---------- Traditional grade-school multiplication O(n^2) ----------

def multiply_traditional(x, y):
    """
    Multiply two non-negative integers x and y using the standard
    grade-school algorithm: multiply every digit of x by every digit
    of y and add up the shifted results. O(n^2) where n = number of
    digits.
    """
    x_digits = [int(d) for d in str(x)][::-1]  # reverse: index 0 = ones place
    y_digits = [int(d) for d in str(y)][::-1]

    result = [0] * (len(x_digits) + len(y_digits))

    for i, xd in enumerate(x_digits):
        carry = 0
        for j, yd in enumerate(y_digits):
            product = xd * yd + result[i + j] + carry
            result[i + j] = product % 10
            carry = product // 10
        result[i + len(y_digits)] += carry

    # Strip leading zeros (which are at the end of our reversed list)
    while len(result) > 1 and result[-1] == 0:
        result.pop()

    return int("".join(str(d) for d in result[::-1]))


# ---------- Karatsuba's algorithm O(n^1.585) ----------

def karatsuba(x, y):
    """
    Multiply two non-negative integers using Karatsuba's algorithm.

    Idea: split each number into a "high" and "low" half,
      x = x_high * 10^m + x_low
      y = y_high * 10^m + y_low

    Naively, x*y needs 4 sub-multiplications (high*high, high*low,
    low*high, low*low). Karatsuba shows you only need 3:
      z2 = x_high * y_high
      z0 = x_low  * y_low
      z1 = (x_high + x_low) * (y_high + y_low) - z2 - z0
    and then:
      x*y = z2 * 10^(2m) + z1 * 10^m + z0
    """
    # Base case: small enough to multiply directly
    if x < 10 or y < 10:
        return x * y

    # Number of digits, padded so both operands split evenly
    n = max(len(str(x)), len(str(y)))
    m = n // 2

    high_x, low_x = divmod(x, 10 ** m)
    high_y, low_y = divmod(y, 10 ** m)

    z2 = karatsuba(high_x, high_y)                     # high * high
    z0 = karatsuba(low_x, low_y)                        # low * low
    z1 = karatsuba(high_x + low_x, high_y + low_y) - z2 - z0  # cross term

    return z2 * 10 ** (2 * m) + z1 * 10 ** m + z0


# ---------- comparison / experiment code ----------

def random_number_with_digits(num_digits):
    """Generate a random positive integer with exactly num_digits digits."""
    if num_digits == 1:
        return random.randint(1, 9)
    first_digit = random.randint(1, 9)
    rest = "".join(str(random.randint(0, 9)) for _ in range(num_digits - 1))
    return int(str(first_digit) + rest)


def run_comparison(digit_sizes):
    """
    For each digit-length in digit_sizes:
      1. Generate two random numbers of that many digits
      2. Multiply with both algorithms, timing each
      3. Verify the results match
    Returns the list of result rows for the report table.
    """
    results = []
    for digits in digit_sizes:
        x = random_number_with_digits(digits)
        y = random_number_with_digits(digits)

        t0 = time.perf_counter()
        result_trad = multiply_traditional(x, y)
        t1 = time.perf_counter()
        result_karatsuba = karatsuba(x, y)
        t2 = time.perf_counter()

        trad_time = t1 - t0
        karatsuba_time = t2 - t1
        match = (result_trad == result_karatsuba)

        results.append({
            "digits": digits,
            "traditional_time_sec": trad_time,
            "karatsuba_time_sec": karatsuba_time,
            "results_match": match,
        })

        print(f"digits={digits:5d} | Traditional: {trad_time:10.6f}s | "
              f"Karatsuba: {karatsuba_time:10.6f}s | Match: {match}")

    return results


def plot_results(results, filename="karatsuba_comparison.png"):
    """Plot running time vs number of digits for both algorithms."""
    digits = [r["digits"] for r in results]
    trad = [r["traditional_time_sec"] for r in results]
    kara = [r["karatsuba_time_sec"] for r in results]

    plt.figure(figsize=(7, 5))
    plt.plot(digits, trad, marker="o", label="Traditional O(n^2)")
    plt.plot(digits, kara, marker="s", label="Karatsuba O(n^1.585)")
    plt.xlabel("Number of digits (n)")
    plt.ylabel("Time (seconds)")
    plt.title("Traditional vs Karatsuba Big-Integer Multiplication")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    print(f"\nGraph saved as {filename}")


if __name__ == "__main__":
    random.seed(42)  # reproducible results for the report

    digit_sizes = [8, 16, 32, 64, 128, 256, 512, 1024]

    print("Comparing Traditional vs Karatsuba Big-Integer Multiplication\n")
    results = run_comparison(digit_sizes)
    plot_results(results)

    all_match = all(r["results_match"] for r in results)
    print("\nConclusion:")
    print(f"  All results matched between the two methods: {all_match}")
    print("  Traditional multiplication compares/multiplies every pair of")
    print("  digits, giving O(n^2) work for n-digit numbers.")
    print("  Karatsuba cuts the number of sub-multiplications per split")
    print("  from 4 down to 3, giving the recurrence T(n)=3T(n/2)+O(n),")
    print("  which solves to O(n^log2(3)) = O(n^1.585). The crossover")
    print("  point where Karatsuba starts winning shows up clearly once")
    print("  n gets into the hundreds of digits in the graph/table above.")