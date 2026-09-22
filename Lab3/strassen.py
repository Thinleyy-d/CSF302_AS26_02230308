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
matrices of increasing size (powers of 2), checks that their
results match, times them, and plots the results.
"""

import time
import random
import matplotlib
matplotlib.use("Agg")  # so it works without a display
import matplotlib.pyplot as plt

from matrix_mult import multiply_traditional, generate_matrix


# ---------- helper functions used by Strassen ----------

def add(A, B):
    """Elementwise matrix addition."""
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]


def subtract(A, B):
    """Elementwise matrix subtraction."""
    n = len(A)
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


def multiply_strassen(A, B):
    """
    Multiply two n x n matrices (n must be a power of 2) using
    Strassen's algorithm.
    """
    n = len(A)

    # Base case: 1x1 "matrix" multiplication is just a number product
    if n == 1:
        return [[A[0][0] * B[0][0]]]

    A11, A12, A21, A22 = split_matrix(A)
    B11, B12, B21, B22 = split_matrix(B)

    # The 7 products Strassen discovered (instead of the naive 8)
    M1 = multiply_strassen(add(A11, A22), add(B11, B22))
    M2 = multiply_strassen(add(A21, A22), B11)
    M3 = multiply_strassen(A11, subtract(B12, B22))
    M4 = multiply_strassen(A22, subtract(B21, B11))
    M5 = multiply_strassen(add(A11, A12), B22)
    M6 = multiply_strassen(subtract(A21, A11), add(B11, B12))
    M7 = multiply_strassen(subtract(A12, A22), add(B21, B22))

    C11 = add(subtract(add(M1, M4), M5), M7)
    C12 = add(M3, M5)
    C21 = add(M2, M4)
    C22 = add(subtract(add(M1, M3), M2), M6)

    return combine_quadrants(C11, C12, C21, C22)


# ---------- comparison / experiment code ----------

def matrices_equal(A, B):
    """Check two matrices are identical (used to verify correctness)."""
    return A == B


def run_comparison(sizes):
    """
    For every size n in `sizes` (each a power of 2):
      1. Generate two random n x n matrices
      2. Multiply with both algorithms, timing each
      3. Verify the results match
      4. Record the timings
    Returns a list of dict rows for the report table.
    """
    results = []
    for n in sizes:
        A = generate_matrix(n)
        B = generate_matrix(n)

        t0 = time.perf_counter()
        C_trad = multiply_traditional(A, B)
        t1 = time.perf_counter()
        C_strassen = multiply_strassen(A, B)
        t2 = time.perf_counter()

        trad_time = t1 - t0
        strassen_time = t2 - t1
        match = matrices_equal(C_trad, C_strassen)

        results.append({
            "n": n,
            "traditional_time_sec": trad_time,
            "strassen_time_sec": strassen_time,
            "results_match": match,
        })

        print(f"n={n:4d} | Traditional: {trad_time:10.6f}s | "
              f"Strassen: {strassen_time:10.6f}s | Match: {match}")

    return results


def plot_results(results, filename="matrix_comparison.png"):
    """Plot running time vs matrix size for both algorithms."""
    ns = [r["n"] for r in results]
    trad = [r["traditional_time_sec"] for r in results]
    strassen = [r["strassen_time_sec"] for r in results]

    plt.figure(figsize=(7, 5))
    plt.plot(ns, trad, marker="o", label="Traditional O(n^3)")
    plt.plot(ns, strassen, marker="s", label="Strassen O(n^2.81)")
    plt.xlabel("Matrix size (n)")
    plt.ylabel("Time (seconds)")
    plt.title("Traditional vs Strassen Matrix Multiplication")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    print(f"\nGraph saved as {filename}")


if __name__ == "__main__":
    random.seed(42)  # reproducible results for the report

    # Sizes must be powers of 2. Feel free to extend up to 128 as the
    # lab suggests, but note Strassen's pure-Python recursion gets
    # noticeably slower past 128 because of Python's function-call
    # overhead (a real C/optimized implementation would not show this).
    sizes = [2, 4, 8, 16, 32, 64, 128]

    print("Comparing Traditional vs Strassen's Matrix Multiplication\n")
    results = run_comparison(sizes)
    plot_results(results)

    all_match = all(r["results_match"] for r in results)
    print("\nConclusion:")
    print(f"  All results matched between the two methods: {all_match}")
    print("  Traditional multiplication does O(n^3) multiplications.")
    print("  Strassen's algorithm does about O(n^2.807) multiplications")
    print("  by trading 1 multiplication for a handful of extra additions")
    print("  at every level of recursion. In pure Python, Strassen's real")
    print("  advantage only starts to show for larger n, because Python's")
    print("  per-call overhead and the extra add/subtract steps eat into")
    print("  the theoretical gain for small matrices.")