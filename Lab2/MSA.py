"""
Q2: Merge Sort Analysis (Menu-Driven Program)
-----------------------------------------------
Sorts an array of n integers using Merge Sort, records step/frequency
counts, and compares performance across three input distributions:
random, already ascending-sorted, and descending-sorted data.

Why Merge Sort?
    It repeatedly divides the array in half (Divide), sorts each half
    recursively (Conquer), then merges the two sorted halves back
    together (Combine). Because splitting always happens down to
    single elements regardless of the data's original order, merge
    sort's time complexity stays O(n log n) in the BEST, AVERAGE, and
    WORST cases -- unlike, e.g., bubble/insertion sort which are much
    faster on already-sorted data.

Student Code: 308
"""

import random
import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------
# Merge Sort - Ascending (with step counter)
# ---------------------------------------------------------------------
def merge_sort_asc_308(arr_308, counter_308):
    """Recursively sort arr_308 in ascending order.
    counter_308 is a single-element list used as a mutable step counter."""
    if len(arr_308) <= 1:
        return arr_308

    mid_308 = len(arr_308) // 2
    left_308 = merge_sort_asc_308(arr_308[:mid_308], counter_308)
    right_308 = merge_sort_asc_308(arr_308[mid_308:], counter_308)

    return merge_asc_308(left_308, right_308, counter_308)


def merge_asc_308(left_308, right_308, counter_308):
    """Merge two sorted (ascending) lists into one sorted list."""
    result_308 = []
    i_308 = j_308 = 0

    while i_308 < len(left_308) and j_308 < len(right_308):
        counter_308[0] += 1          # one comparison
        if left_308[i_308] <= right_308[j_308]:
            result_308.append(left_308[i_308])
            i_308 += 1
        else:
            result_308.append(right_308[j_308])
            j_308 += 1

    result_308.extend(left_308[i_308:])
    result_308.extend(right_308[j_308:])
    return result_308


# ---------------------------------------------------------------------
# Merge Sort - Descending (used for menu option 4)
# ---------------------------------------------------------------------
def merge_sort_desc_308(arr_308, counter_308):
    if len(arr_308) <= 1:
        return arr_308

    mid_308 = len(arr_308) // 2
    left_308 = merge_sort_desc_308(arr_308[:mid_308], counter_308)
    right_308 = merge_sort_desc_308(arr_308[mid_308:], counter_308)

    return merge_desc_308(left_308, right_308, counter_308)


def merge_desc_308(left_308, right_308, counter_308):
    result_308 = []
    i_308 = j_308 = 0

    while i_308 < len(left_308) and j_308 < len(right_308):
        counter_308[0] += 1
        if left_308[i_308] >= right_308[j_308]:
            result_308.append(left_308[i_308])
            i_308 += 1
        else:
            result_308.append(right_308[j_308])
            j_308 += 1

    result_308.extend(left_308[i_308:])
    result_308.extend(right_308[j_308:])
    return result_308


# ---------------------------------------------------------------------
# Helpers to build test data of different "shapes"
# ---------------------------------------------------------------------
def generate_random_array_308(n_308, low_308=1, high_308=1000):
    return [random.randint(low_308, high_308) for _ in range(n_308)]


def generate_sorted_array_308(n_308):
    return list(range(1, n_308 + 1))


def generate_reverse_sorted_array_308(n_308):
    return list(range(n_308, 0, -1))


# ---------------------------------------------------------------------
# Time-complexity experiment: runs merge sort for increasing n and
# records step counts + wall-clock time, then plots the results.
# ---------------------------------------------------------------------
def run_complexity_experiment_308(data_type_label_308, array_generator_308,
                                   sizes_308=(100, 500, 1000, 2000, 4000, 8000)):
    step_counts_308 = []
    time_counts_308 = []

    print(f"\n--- Time Complexity: {data_type_label_308} data ---")
    print(f"{'n':>8} | {'Steps (comparisons)':>20} | {'Time (s)':>12}")
    print("-" * 46)

    for n_308 in sizes_308:
        arr_308 = array_generator_308(n_308)
        counter_308 = [0]

        start_308 = time.perf_counter()
        merge_sort_asc_308(arr_308, counter_308)
        elapsed_308 = time.perf_counter() - start_308

        step_counts_308.append(counter_308[0])
        time_counts_308.append(elapsed_308)
        print(f"{n_308:>8} | {counter_308[0]:>20} | {elapsed_308:>12.6f}")

    return list(sizes_308), step_counts_308, time_counts_308


def plot_complexity_results_308(all_results_308, filename_308):
    """all_results_308: list of (label, sizes, steps) tuples"""
    plt.figure(figsize=(9, 6))
    markers_308 = ["o", "s", "^"]
    for idx_308, (label_308, sizes_308, steps_308) in enumerate(all_results_308):
        plt.plot(sizes_308, steps_308, marker=markers_308[idx_308 % len(markers_308)], label=label_308)
    plt.xlabel("Input size (n)")
    plt.ylabel("Step / Frequency Count (comparisons)")
    plt.title("Merge Sort: Step Count vs Input Size for Different Data Types (Roll No. 308)")
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
    print(" MERGE SORT ANALYSIS - MENU (Student Code: 308)")
    print("=" * 55)
    print("1. Generate n random numbers -> Array")
    print("2. Display Array")
    print("3. Sort in Ascending Order using Merge Sort")
    print("4. Sort in Descending Order using Merge Sort")
    print("5. Time Complexity for ascending sort on RANDOM data")
    print("6. Time Complexity for ascending sort on SORTED data")
    print("7. Time Complexity for ascending sort on DESCENDING data")
    print("8. Exit")
    print("=" * 55)


def main_308():
    current_array_308 = []
    complexity_history_308 = {}   # stores results from options 5/6/7 for a combined plot

    while True:
        print_menu_308()
        choice_308 = input("Enter your choice (1-8): ").strip()

        if choice_308 == "1":
            n_308 = int(input("Enter number of elements (n): "))
            current_array_308 = generate_random_array_308(n_308)
            print(f"Generated array of {n_308} random numbers.")

        elif choice_308 == "2":
            if not current_array_308:
                print("Array is empty. Please generate it first (option 1).")
            else:
                print("Current Array:")
                print(current_array_308)

        elif choice_308 == "3":
            if not current_array_308:
                print("Array is empty. Please generate it first (option 1).")
            else:
                counter_308 = [0]
                start_308 = time.perf_counter()
                sorted_arr_308 = merge_sort_asc_308(current_array_308[:], counter_308)
                elapsed_308 = time.perf_counter() - start_308
                print(f"Sorted (Ascending): {sorted_arr_308}")
                print(f"Step/Frequency Count: {counter_308[0]}   Time: {elapsed_308:.6f}s")

        elif choice_308 == "4":
            if not current_array_308:
                print("Array is empty. Please generate it first (option 1).")
            else:
                counter_308 = [0]
                start_308 = time.perf_counter()
                sorted_arr_308 = merge_sort_desc_308(current_array_308[:], counter_308)
                elapsed_308 = time.perf_counter() - start_308
                print(f"Sorted (Descending): {sorted_arr_308}")
                print(f"Step/Frequency Count: {counter_308[0]}   Time: {elapsed_308:.6f}s")

        elif choice_308 == "5":
            sizes_308, steps_308, times_308 = run_complexity_experiment_308(
                "Random", generate_random_array_308)
            plot_complexity_results_308(
                [("Random Data", sizes_308, steps_308)],
                "merge_sort_random_308.png")
            complexity_history_308["Random Data"] = (sizes_308, steps_308)

        elif choice_308 == "6":
            sizes_308, steps_308, times_308 = run_complexity_experiment_308(
                "Already Ascending-Sorted", generate_sorted_array_308)
            plot_complexity_results_308(
                [("Already Sorted Data", sizes_308, steps_308)],
                "merge_sort_sorted_308.png")
            complexity_history_308["Already Sorted Data"] = (sizes_308, steps_308)

        elif choice_308 == "7":
            sizes_308, steps_308, times_308 = run_complexity_experiment_308(
                "Descending-Sorted", generate_reverse_sorted_array_308)
            plot_complexity_results_308(
                [("Descending-Sorted Data", sizes_308, steps_308)],
                "merge_sort_descending_308.png")
            complexity_history_308["Descending-Sorted Data"] = (sizes_308, steps_308)

        elif choice_308 == "8":
            if len(complexity_history_308) >= 2:
                combined_308 = [(label_308, s_308, st_308)
                                 for label_308, (s_308, st_308) in complexity_history_308.items()]
                plot_complexity_results_308(combined_308, "merge_sort_combined_comparison_308.png")
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

    # CONCLUSION:
    # 1. Merge Sort's step count (number of comparisons during merge)
    #    is ALWAYS close to n*log2(n), regardless of whether the input
    #    was random, already sorted, or reverse sorted. This confirms
    #    merge sort has O(n log n) complexity in best, average, and
    #    worst cases -- it does not benefit from partially-sorted input
    #    the way insertion sort or bubble sort would.
    # 2. This "data-independence" is merge sort's key strength: it
    #    guarantees predictable performance no matter the input shape,
    #    making it reliable for large datasets or when the data
    #    distribution is unknown.
    # 3. The trade-off is O(n) extra space for the merge step, unlike
    #    in-place sorts like quicksort or heapsort.


if __name__ == "__main__":
    main_308()