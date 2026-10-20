"""
matrix_mult.py
---------------
Traditional (grade-school) matrix multiplication using the classic
triple nested loop.  Time complexity: O(n^3).

This file is imported by strassen.py so both algorithms can be
compared on the same input matrices.  It also holds the small helper
functions (random matrix, manual input, printing) used by both files.

Run it directly to multiply two matrices with the traditional method:
    python matrix_mult.py
"""

import random


def new_counter():
    """A tiny 'scoreboard' used to count steps (multiplications and additions)."""
    return {"mult": 0, "add": 0}


def generate_matrix(n, low=0, high=9):
    """Generate an n x n matrix filled with random integers."""
    return [[random.randint(low, high) for _ in range(n)] for _ in range(n)]


def input_matrix(n, name):
    """Ask the user to type an n x n matrix, one row at a time."""
    print(f"Enter matrix {name} ({n} rows, {n} numbers per row, separated by spaces):")
    matrix = []
    for i in range(n):
        while True:
            try:
                row = list(map(int, input(f"  Row {i + 1}: ").split()))
            except ValueError:
                print("  Please type whole numbers only.")
                continue
            if len(row) == n:
                break
            print(f"  Need exactly {n} numbers. Try again.")
        matrix.append(row)
    return matrix


def is_power_of_two(n):
    """True for 1, 2, 4, 8, 16, ..."""
    return n > 0 and (n & (n - 1)) == 0


def get_matrices():
    """Ask for the size n, then read or generate matrices A and B."""
    while True:
        try:
            n = int(input("Enter matrix size n (power of 2: 2, 4, 8, ... 128): "))
        except ValueError:
            print("Please type a whole number.")
            continue
        if is_power_of_two(n):
            break
        print("n must be a power of 2.")

    choice = input("1 = generate random matrices, 2 = type them manually: ").strip()
    if choice == "2":
        A = input_matrix(n, "A")
        B = input_matrix(n, "B")
    else:
        A = generate_matrix(n)
        B = generate_matrix(n)
    return A, B


def multiply_traditional(A, B, counter=None):
    """
    Multiply two n x n matrices A and B using the standard
    triple nested loop method.

    For every cell C[i][j] we compute the dot product of row i of A
    and column j of B -> n multiplications per cell, n^2 cells
    => O(n^3) multiplications overall.

    counter (optional) is a dictionary {"mult": .., "add": ..} that is
    updated with the number of steps (step/frequency count).
    """
    if counter is None:
        counter = new_counter()

    n = len(A)
    # Start with a result matrix full of zeros
    C = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):          # pick a row of A
        for j in range(n):      # pick a column of B
            total = 0
            for k in range(n):  # walk along the row/column and sum products
                total += A[i][k] * B[k][j]
                counter["mult"] += 1   # one multiplication
                counter["add"] += 1    # one addition (into total)
            C[i][j] = total

    return C


def print_matrix(M, name="Matrix"):
    """Pretty-print a matrix. Big matrices show only the top-left 8 x 8 corner."""
    print(f"{name}:")
    limit = min(len(M), 8)
    for i in range(limit):
        print("  ", M[i][:limit], "..." if len(M) > 8 else "")
    if len(M) > 8:
        print(f"   (showing only the top-left 8 x 8 of {len(M)} x {len(M)})")
    print()


if __name__ == "__main__":
    A, B = get_matrices()
    print_matrix(A, "A")
    print_matrix(B, "B")

    counter = new_counter()
    C = multiply_traditional(A, B, counter)
    print_matrix(C, "A x B (Traditional)")
    print(f"Step count -> multiplications: {counter['mult']}, additions: {counter['add']}")

# ---------------------------------------------------------------------
# ANALYSIS / CONCLUSION (Traditional matrix multiplication)
# The innermost line runs n * n * n times, so the method always does
# n^3 multiplications and about n^3 additions -> time complexity O(n^3).
# Doubling n makes the work 8 times bigger (e.g. n=64 -> 262,144
# multiplications, n=128 -> 2,097,152 multiplications).
# ---------------------------------------------------------------------
