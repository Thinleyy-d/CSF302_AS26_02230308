"""
matrix_mult.py
---------------
Traditional (grade-school) matrix multiplication using the classic
triple nested loop.  Time complexity: O(n^3).

This file is imported by strassen.py so both algorithms can be
compared on the same input matrices.
"""

import random


def generate_matrix(n, low=0, high=9):
    """Generate an n x n matrix filled with random integers."""
    return [[random.randint(low, high) for _ in range(n)] for _ in range(n)]


def multiply_traditional(A, B):
    """
    Multiply two n x n matrices A and B using the standard
    triple nested loop method.

    For every cell C[i][j] we compute the dot product of row i of A
    and column j of B -> n multiplications per cell, n^2 cells
    => O(n^3) multiplications overall.
    """
    n = len(A)
    # Start with a result matrix full of zeros
    C = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):          # pick a row of A
        for j in range(n):      # pick a column of B
            total = 0
            for k in range(n):  # walk along the row/column and sum products
                total += A[i][k] * B[k][j]
            C[i][j] = total

    return C


def print_matrix(M, name="Matrix"):
    """Pretty-print a matrix (only sensible for small n)."""
    print(f"{name}:")
    for row in M:
        print(row)
    print()


if __name__ == "__main__":
    # Small demo when this file is run directly
    n = 4
    A = generate_matrix(n)
    B = generate_matrix(n)
    print_matrix(A, "A")
    print_matrix(B, "B")
    C = multiply_traditional(A, B)
    print_matrix(C, "A x B (Traditional)")