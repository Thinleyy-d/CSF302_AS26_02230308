"""
Q3: Square Matrix Multiplication
-----------------------------------
Multiplies two n x n matrices (n must be a power of 2: 2, 4, 8, 16, ...)
using the standard (naive) algorithm, counts basic operations
(multiplications + additions), and displays the resultant matrix.

Why count operations?
    For each of the n*n cells in the result matrix, we perform n
    multiplications and n-1 additions (to sum the products). This
    gives Total Operations ~ n^2 * (2n) = O(n^3), which is the
    classical time complexity of matrix multiplication.

Student Code: 308
"""

import random
import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------
# Utility: check power of 2, generate/display matrices
# ---------------------------------------------------------------------
def is_power_of_two_308(n_308):
    return n_308 > 0 and (n_308 & (n_308 - 1)) == 0


def generate_matrix_308(n_308, low_308=1, high_308=10):
    return [[random.randint(low_308, high_308) for _ in range(n_308)] for _ in range(n_308)]


def input_matrix_manually_308(n_308, name_308):
    print(f"\nEnter matrix {name_308} row by row ({n_308} numbers per row, space-separated):")
    matrix_308 = []
    for r_308 in range(n_308):
        while True:
            row_308 = input(f"Row {r_308 + 1}: ").strip().split()
            if len(row_308) != n_308:
                print(f"Please enter exactly {n_308} numbers.")
                continue
            try:
                matrix_308.append([int(x_308) for x_308 in row_308])
                break
            except ValueError:
                print("Please enter valid integers.")
    return matrix_308


def display_matrix_308(matrix_308, name_308="Matrix"):
    print(f"\n{name_308}:")
    for row_308 in matrix_308:
        print(" ".join(f"{val_308:>5}" for val_308 in row_308))


# ---------------------------------------------------------------------
# Standard (naive) O(n^3) matrix multiplication with step counting
# ---------------------------------------------------------------------
def multiply_matrices_308(a_308, b_308):
    n_308 = len(a_308)
    result_308 = [[0] * n_308 for _ in range(n_308)]
    steps_308 = 0   # counts multiplications + additions

    for i_308 in range(n_308):
        for j_308 in range(n_308):
            cell_sum_308 = 0
            for k_308 in range(n_308):
                cell_sum_308 += a_308[i_308][k_308] * b_308[k_308][j_308]
                steps_308 += 2      # 1 multiplication + 1 addition
            result_308[i_308][j_308] = cell_sum_308

    return result_308, steps_308


# ---------------------------------------------------------------------
# Time complexity experiment across increasing power-of-2 sizes
# ---------------------------------------------------------------------
def run_complexity_experiment_308(sizes_308=(2, 4, 8, 16, 32, 64)):
    step_counts_308 = []
    time_counts_308 = []

    print("\n--- Time Complexity: Standard Matrix Multiplication ---")
    print(f"{'n':>6} | {'Steps (mult+add)':>18} | {'Time (s)':>12}")
    print("-" * 42)

    for n_308 in sizes_308:
        a_308 = generate_matrix_308(n_308)
        b_308 = generate_matrix_308(n_308)

        start_308 = time.perf_counter()
        _, steps_308 = multiply_matrices_308(a_308, b_308)
        elapsed_308 = time.perf_counter() - start_308

        step_counts_308.append(steps_308)
        time_counts_308.append(elapsed_308)
        print(f"{n_308:>6} | {steps_308:>18} | {elapsed_308:>12.6f}")

    return list(sizes_308), step_counts_308, time_counts_308


def plot_complexity_308(sizes_308, steps_308, filename_308="matrix_mult_complexity_308.png"):
    plt.figure(figsize=(9, 6))
    plt.plot(sizes_308, steps_308, marker="o", color="darkorange", label="Standard Multiplication O(n^3)")
    plt.xlabel("Matrix size (n x n)")
    plt.ylabel("Step / Frequency Count (mult + add operations)")
    plt.title("Matrix Multiplication: Step Count vs Matrix Size (Roll No. 308)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(filename_308, dpi=150)
    print(f"\nGraph saved as {filename_308}")


# ---------------------------------------------------------------------
# Menu-driven driver
# ---------------------------------------------------------------------
def print_menu_308():
    print("\n" + "=" * 55)
    print(" SQUARE MATRIX MULTIPLICATION (Student Code: 308)")
    print("=" * 55)
    print("1. Generate two n x n matrices randomly (n = power of 2)")
    print("2. Input two n x n matrices manually (n = power of 2)")
    print("3. Display current matrices A and B")
    print("4. Multiply A x B and show result + step count")
    print("5. Time Complexity experiment (n = 2,4,8,16,32,64)")
    print("6. Exit")
    print("=" * 55)


def main_308():
    matrix_a_308 = None
    matrix_b_308 = None

    while True:
        print_menu_308()
        choice_308 = input("Enter your choice (1-6): ").strip()

        if choice_308 == "1":
            n_308 = int(input("Enter matrix size n (must be power of 2, e.g. 2,4,8,16): "))
            if not is_power_of_two_308(n_308):
                print("n must be a power of 2 (2, 4, 8, 16, 32, ...). Try again.")
                continue
            matrix_a_308 = generate_matrix_308(n_308)
            matrix_b_308 = generate_matrix_308(n_308)
            print(f"Generated two random {n_308}x{n_308} matrices.")

        elif choice_308 == "2":
            n_308 = int(input("Enter matrix size n (must be power of 2, e.g. 2,4,8,16): "))
            if not is_power_of_two_308(n_308):
                print("n must be a power of 2 (2, 4, 8, 16, 32, ...). Try again.")
                continue
            matrix_a_308 = input_matrix_manually_308(n_308, "A")
            matrix_b_308 = input_matrix_manually_308(n_308, "B")

        elif choice_308 == "3":
            if matrix_a_308 is None:
                print("No matrices yet. Please generate/input first (option 1 or 2).")
            else:
                display_matrix_308(matrix_a_308, "Matrix A")
                display_matrix_308(matrix_b_308, "Matrix B")

        elif choice_308 == "4":
            if matrix_a_308 is None:
                print("No matrices yet. Please generate/input first (option 1 or 2).")
            else:
                start_308 = time.perf_counter()
                result_308, steps_308 = multiply_matrices_308(matrix_a_308, matrix_b_308)
                elapsed_308 = time.perf_counter() - start_308
                display_matrix_308(result_308, "Result Matrix (A x B)")
                print(f"\nStep/Frequency Count (multiplications + additions): {steps_308}")
                print(f"Time taken: {elapsed_308:.6f}s")

        elif choice_308 == "5":
            sizes_308, steps_308, times_308 = run_complexity_experiment_308()
            plot_complexity_308(sizes_308, steps_308)

        elif choice_308 == "6":
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

    # CONCLUSION:
    # 1. The standard matrix multiplication algorithm performs n
    #    multiplications and n additions per output cell, and there
    #    are n*n output cells, giving Total Steps ~ 2*n^3 -> O(n^3).
    # 2. The experiment confirms this: doubling n (e.g. 8 -> 16)
    #    increases the step count by roughly 2^3 = 8x, and doubling
    #    again (16 -> 32) again multiplies steps by ~8x -- the
    #    hallmark of cubic growth.
    # 3. For large n, more advanced algorithms like Strassen's
    #    (O(n^2.807), see strassen.py) or Coppersmith-Winograd-style
    #    methods reduce the asymptotic complexity, at the cost of
    #    higher constant factors and more complex implementation,
    #    so they only pay off for sufficiently large n.


if __name__ == "__main__":
    main_308()