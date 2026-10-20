"""
strassen.py
------------
Strassen's divide-and-conquer matrix multiplication algorithm.

Instead of the 8 recursive multiplications you'd expect from naively
splitting an n x n matrix into four (n/2) x (n/2) quadrants,
Strassen found a way to do it with only 7 multiplications (at the
cost of some extra additions/subtractions). That changes the
recurrence from:

    T(n) = 8T(n/2) + O(n^2)   ->  O(n^3)   (same as traditional)
to:
    T(n) = 7T(n/2) + O(n^2)   ->  O(n^log2(7)) ~= O(n^2.807)

This file also contains the code that runs both algorithms on
matrices (random or typed in manually), checks that their results
match, counts the steps (multiplications / additions), times them,
and prints the step/frequency count table + a graph.

Needs matrix_mult.py in the same folder.
Run:  python strassen.py
"""

import time
import random

# The graph is a bonus: the program still works if matplotlib is missing.
try:
    import matplotlib
    matplotlib.use("Agg")  # so it works without a display
    import matplotlib.pyplot as plt
    HAVE_PLOT = True
except ImportError:
    HAVE_PLOT = False

from matrix_mult import (multiply_traditional, generate_matrix,
                         get_matrices, print_matrix, new_counter)


# ---------- helper functions used by Strassen ----------

def add(A, B, counter):
    """Elementwise matrix addition (counts n*n additions)."""
    n = len(A)
    counter["add"] += n * n
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]


def subtract(A, B, counter):
    """Elementwise matrix subtraction (counted as n*n additions)."""
    n = len(A)
    counter["add"] += n * n
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]


def split_matrix(M):
    """Split matrix M into four equal quadrants: top-left, top-right,
    bottom-left, bottom-right."""
    n = len(M)
    mid = n // 2
    top_left = [row[:mid] for row in M[:mid]]
    top_right = [row[mid:] for row in M[:mid]]
    bottom_left = [row[:mid] for row in M[mid:]]
    bottom_right = [row[mid:] for row in M[mid:]]
    return top_left, top_right, bottom_left, bottom_right


def combine_quadrants(C11, C12, C21, C22):
    """Glue four quadrants back into one matrix."""
    top = [c11_row + c12_row for c11_row, c12_row in zip(C11, C12)]
    bottom = [c21_row + c22_row for c21_row, c22_row in zip(C21, C22)]
    return top + bottom


def multiply_strassen(A, B, counter=None):
    """
    Multiply two n x n matrices (n must be a power of 2) using
    Strassen's algorithm.

    counter (optional) is a dictionary {"mult": .., "add": ..} that is
    updated with the number of steps (step/frequency count).
    """
    if counter is None:
        counter = new_counter()

    n = len(A)

    # Base case: 1x1 "matrix" multiplication is just a number product
    if n == 1:
        counter["mult"] += 1
        return [[A[0][0] * B[0][0]]]

    A11, A12, A21, A22 = split_matrix(A)
    B11, B12, B21, B22 = split_matrix(B)

    # The 7 products Strassen discovered (instead of the naive 8)
    M1 = multiply_strassen(add(A11, A22, counter), add(B11, B22, counter), counter)
    M2 = multiply_strassen(add(A21, A22, counter), B11, counter)
    M3 = multiply_strassen(A11, subtract(B12, B22, counter), counter)
    M4 = multiply_strassen(A22, subtract(B21, B11, counter), counter)
    M5 = multiply_strassen(add(A11, A12, counter), B22, counter)
    M6 = multiply_strassen(subtract(A21, A11, counter), add(B11, B12, counter), counter)
    M7 = multiply_strassen(subtract(A12, A22, counter), add(B21, B22, counter), counter)

    C11 = add(subtract(add(M1, M4, counter), M5, counter), M7, counter)
    C12 = add(M3, M5, counter)
    C21 = add(M2, M4, counter)
    C22 = add(subtract(add(M1, M3, counter), M2, counter), M6, counter)

    return combine_quadrants(C11, C12, C21, C22)


# ---------- comparison / experiment code ----------

def matrices_equal(A, B):
    """Check two matrices are identical (used to verify correctness)."""
    return A == B


def compare_one_pair():
    """Menu option 1: multiply one pair of matrices (random or manual) with both methods."""
    A, B = get_matrices()
    print_matrix(A, "Matrix A")
    print_matrix(B, "Matrix B")

    trad_counter = new_counter()
    t0 = time.perf_counter()
    C_trad = multiply_traditional(A, B, trad_counter)
    t1 = time.perf_counter()

    str_counter = new_counter()
    C_strassen = multiply_strassen(A, B, str_counter)
    t2 = time.perf_counter()

    print_matrix(C_trad, "Result (Traditional)")
    print_matrix(C_strassen, "Result (Strassen)")

    if matrices_equal(C_trad, C_strassen):
        print("VERIFIED: both methods give the SAME result matrix.\n")
    else:
        print("ERROR: the two results are different!\n")

    print("Step/frequency count:")
    print(f"  Traditional -> mults: {trad_counter['mult']}, adds: {trad_counter['add']}, "
          f"time: {t1 - t0:.6f}s")
    print(f"  Strassen    -> mults: {str_counter['mult']}, adds: {str_counter['add']}, "
          f"time: {t2 - t1:.6f}s\n")


def run_comparison(sizes):
    """
    For every size n in `sizes` (each a power of 2):
      1. Generate two random n x n matrices
      2. Multiply with both algorithms, counting steps and timing each
      3. Verify the results match
      4. Record everything
    Prints the step/frequency count table and returns the rows.
    """
    results = []

    print("-" * 100)
    print(f"{'n':>4} | {'Trad mults':>11} {'Trad adds':>11} | "
          f"{'Str mults':>10} {'Str adds':>10} | "
          f"{'Trad time(s)':>12} {'Str time(s)':>12} | Match")
    print("-" * 100)

    for n in sizes:
        A = generate_matrix(n)
        B = generate_matrix(n)

        trad_counter = new_counter()
        t0 = time.perf_counter()
        C_trad = multiply_traditional(A, B, trad_counter)
        t1 = time.perf_counter()

        str_counter = new_counter()
        C_strassen = multiply_strassen(A, B, str_counter)
        t2 = time.perf_counter()

        match = matrices_equal(C_trad, C_strassen)

        results.append({
            "n": n,
            "trad_mult": trad_counter["mult"],
            "trad_add": trad_counter["add"],
            "str_mult": str_counter["mult"],
            "str_add": str_counter["add"],
            "traditional_time_sec": t1 - t0,
            "strassen_time_sec": t2 - t1,
            "results_match": match,
        })

        print(f"{n:>4} | {trad_counter['mult']:>11} {trad_counter['add']:>11} | "
              f"{str_counter['mult']:>10} {str_counter['add']:>10} | "
              f"{t1 - t0:>12.6f} {t2 - t1:>12.6f} | {match}")

    print("-" * 100)
    return results


def plot_results(results, filename="matrix_comparison.png"):
    """Plot multiplications (left) and running time (right) vs matrix size."""
    if not HAVE_PLOT:
        print("matplotlib is not installed, so the graph was skipped.")
        return

    ns = [r["n"] for r in results]

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(ns, [r["trad_mult"] for r in results], marker="o", label="Traditional O(n^3)")
    plt.plot(ns, [r["str_mult"] for r in results], marker="s", label="Strassen O(n^2.81)")
    plt.xlabel("Matrix size (n)")
    plt.ylabel("Number of multiplications (step count)")
    plt.title("Step count: multiplications")
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.subplot(1, 2, 2)
    plt.plot(ns, [r["traditional_time_sec"] for r in results], marker="o", label="Traditional")
    plt.plot(ns, [r["strassen_time_sec"] for r in results], marker="s", label="Strassen")
    plt.xlabel("Matrix size (n)")
    plt.ylabel("Time (seconds)")
    plt.title("Running time")
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    print(f"Graph saved as {filename}")


def run_table():
    """Menu option 2: step-count table + graph for n = 2, 4, ..., 128."""
    random.seed(42)  # reproducible results for the report
    sizes = [2, 4, 8, 16, 32, 64, 128]
    print("\nComparing Traditional vs Strassen's Matrix Multiplication\n")
    results = run_comparison(sizes)
    plot_results(results)
    all_match = all(r["results_match"] for r in results)
    print(f"\nAll results matched between the two methods: {all_match}\n")


def main():
    while True:
        print("=" * 50)
        print(" Traditional vs Strassen - Matrix Multiplication")
        print("=" * 50)
        print("1. Multiply two matrices (random or manual) and compare")
        print("2. Step/frequency count table for n = 2 to 128")
        print("3. Exit")
        choice = input("Choose an option (1-3): ").strip()
        if choice == "1":
            compare_one_pair()
        elif choice == "2":
            run_table()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.\n")


if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------
# ANALYSIS / CONCLUSION (Strassen vs Traditional)
# * Traditional: n^3 multiplications -> O(n^3).
# * Strassen: T(n) = 7T(n/2) + O(n^2) -> O(n^log2(7)) = O(n^2.807).
#   Number of multiplications is exactly 7^(log2 n)
#   (n=128 -> 7^7 = 823,543 versus 128^3 = 2,097,152).
# * The step-count table shows Strassen always needs FEWER multiplications
#   and the gap grows as n grows (n=128: about 2.5 times fewer).
# * BUT Strassen does many more additions/subtractions (n=128: about
#   4.8 million versus 2.1 million) and makes lots of small matrices and
#   recursive calls. In pure Python this overhead is bigger than the
#   saving, so the traditional method is FASTER in real running time for
#   every size tested (n = 2 to 128). Strassen only wins in time for
#   much larger matrices, or in a compiled language.
# * For every test the two methods gave the same result matrix (verified).
# ---------------------------------------------------------------------
