"""
search.py
----------
Menu-driven program: Binary Search vs Ternary Search.

Binary Search:  splits the array into 2 pieces each step
                 recurrence: T(n) = T(n/2) + O(1)  ->  O(log2 n)
                 each step makes up to 2 comparisons

Ternary Search: splits the array into 3 pieces each step
                 recurrence: T(n) = T(n/3) + O(1)  ->  O(log3 n)
                 BUT each step makes up to 4 comparisons, so its real
                 comparison count is close to
                 4 * log3(n) = 4 * log2(n)/log2(3) ~= 2.52 * log2(n)
                 while binary search needs about 2 * log2(n).

So even though log3(n) < log2(n), Ternary Search usually does *more*
comparisons than Binary Search in practice, because it pays for extra
comparisons at every level. This program lets you see that for yourself.

Step/frequency count = number of comparisons of the key with array elements.

Run:  python search.py
"""

import random
import math

# The graph is a bonus: the program still works if matplotlib is missing.
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAVE_PLOT = True
except ImportError:
    HAVE_PLOT = False

current_array = []  # the array we're working with (set via menu option 1)


# ---------- core algorithms (each returns index found AND comparisons made) ----------

def binary_search(arr, key):
    """
    Standard binary search on a sorted array.
    Returns (index_or_-1, comparison_count).
    """
    low, high = 0, len(arr) - 1
    comparisons = 0

    while low <= high:
        mid = (low + high) // 2
        comparisons += 1                 # is arr[mid] == key ?
        if arr[mid] == key:
            return mid, comparisons
        comparisons += 1                 # is arr[mid] < key ?
        if arr[mid] < key:
            low = mid + 1
        else:
            high = mid - 1

    return -1, comparisons


def ternary_search(arr, key):
    """
    Standard ternary search on a sorted array.
    Splits the current range into 3 parts using two "mid" points.
    Returns (index_or_-1, comparison_count).
    """
    low, high = 0, len(arr) - 1
    comparisons = 0

    while low <= high:
        mid1 = low + (high - low) // 3
        mid2 = high - (high - low) // 3

        comparisons += 1                 # is arr[mid1] == key ?
        if arr[mid1] == key:
            return mid1, comparisons

        comparisons += 1                 # is arr[mid2] == key ?
        if arr[mid2] == key:
            return mid2, comparisons

        comparisons += 1                 # is key < arr[mid1] ?
        if key < arr[mid1]:
            high = mid1 - 1
        else:
            comparisons += 1             # is key > arr[mid2] ?
            if key > arr[mid2]:
                low = mid2 + 1
            else:
                low, high = mid1 + 1, mid2 - 1

    return -1, comparisons


# ---------- best / worst case helpers (used by the menu AND the table) ----------

def best_case_counts(arr):
    """
    Best case for both searches: the key is exactly where the algorithm
    looks first. Returns (key_for_binary, bin_comps, key_for_ternary, ter_comps).
    """
    n = len(arr)
    key_for_binary = arr[(n - 1) // 2]     # first mid that binary search checks
    key_for_ternary = arr[(n - 1) // 3]    # first mid1 that ternary search checks
    _, bin_comps = binary_search(arr, key_for_binary)
    _, ter_comps = ternary_search(arr, key_for_ternary)
    return key_for_binary, bin_comps, key_for_ternary, ter_comps


def worst_case_counts(arr):
    """
    Worst case for both searches: a key that is NOT in the array and is
    bigger than every element (the search always goes to the right and
    narrows all the way down to an empty range).
    Returns (missing_key, bin_comps, ter_comps).
    """
    missing_key = arr[-1] + 1
    _, bin_comps = binary_search(arr, missing_key)
    _, ter_comps = ternary_search(arr, missing_key)
    return missing_key, bin_comps, ter_comps


# ---------- menu option implementations ----------

def generate_array():
    global current_array
    try:
        n = int(input("How many numbers should the array contain? "))
        low = int(input("Lowest possible value: "))
        high = int(input("Highest possible value: "))
    except ValueError:
        print("Please enter valid integers.\n")
        return
    if n < 1 or low > high:
        print("Need n >= 1 and lowest <= highest.\n")
        return
    current_array = sorted(random.randint(low, high) for _ in range(n))
    print(f"Generated a sorted array of {n} numbers.\n")


def display_array():
    if not current_array:
        print("No array yet. Use option 1 first.\n")
        return
    print("Array:", current_array, "\n")


def search_with_binary():
    if not current_array:
        print("No array yet. Use option 1 first.\n")
        return
    try:
        key = int(input("Enter the key to search for: "))
    except ValueError:
        print("Please enter a whole number.\n")
        return
    idx, comps = binary_search(current_array, key)
    if idx == -1:
        print(f"{key} not found. Comparisons made: {comps}\n")
    else:
        print(f"{key} found at index {idx}. Comparisons made: {comps}\n")


def search_with_ternary():
    if not current_array:
        print("No array yet. Use option 1 first.\n")
        return
    try:
        key = int(input("Enter the key to search for: "))
    except ValueError:
        print("Please enter a whole number.\n")
        return
    idx, comps = ternary_search(current_array, key)
    if idx == -1:
        print(f"{key} not found. Comparisons made: {comps}\n")
    else:
        print(f"{key} found at index {idx}. Comparisons made: {comps}\n")


def best_case_demo():
    """Step/frequency count for the best case (key found on the very first probe)."""
    if not current_array:
        print("No array yet. Use option 1 first.\n")
        return
    key_b, bin_comps, key_t, ter_comps = best_case_counts(current_array)
    print(f"Best case (key present, found on the very first probe), n = {len(current_array)}:")
    print(f"  Binary Search  -> key={key_b}, comparisons={bin_comps}")
    print(f"  Ternary Search -> key={key_t}, comparisons={ter_comps}\n")


def worst_case_demo():
    """Step/frequency count for the worst case (key absent from the array)."""
    if not current_array:
        print("No array yet. Use option 1 first.\n")
        return
    key, bin_comps, ter_comps = worst_case_counts(current_array)
    print(f"Worst case (key {key} is absent from the array), n = {len(current_array)}:")
    print(f"  Binary Search  -> comparisons={bin_comps}")
    print(f"  Ternary Search -> comparisons={ter_comps}\n")


def comparison_table():
    """
    Build (and plot) a table of best-case and worst-case comparison counts
    for Binary vs Ternary search across increasing array sizes.
    """
    sizes = [10, 100, 1_000, 10_000, 100_000, 1_000_000]
    rows = []

    print("-" * 82)
    print(f"{'n':>9} | {'Bin best':>8} {'Ter best':>8} | {'Bin worst':>9} {'Ter worst':>9} | "
          f"{'log2(n)':>8} {'log3(n)':>8}")
    print("-" * 82)
    for n in sizes:
        arr = list(range(0, 2 * n, 2))  # sorted even numbers, length n
        _, bin_best, _, ter_best = best_case_counts(arr)
        _, bin_worst, ter_worst = worst_case_counts(arr)
        rows.append((n, bin_best, ter_best, bin_worst, ter_worst))
        print(f"{n:>9} | {bin_best:>8} {ter_best:>8} | {bin_worst:>9} {ter_worst:>9} | "
              f"{math.log2(n):>8.2f} {math.log(n, 3):>8.2f}")
    print("-" * 82)

    # Plot it
    if HAVE_PLOT:
        ns = [r[0] for r in rows]
        bins_ = [r[3] for r in rows]
        ters = [r[4] for r in rows]

        plt.figure(figsize=(7, 5))
        plt.plot(ns, bins_, marker="o", label="Binary Search")
        plt.plot(ns, ters, marker="s", label="Ternary Search")
        plt.xscale("log")
        plt.xlabel("Array size n (log scale)")
        plt.ylabel("Worst-case comparisons")
        plt.title("Binary vs Ternary Search: Comparison Counts")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig("search_comparison.png", dpi=150)
        print("Graph saved as search_comparison.png")

    print("\nWhy this happens:")
    print("  Binary Search recurrence: T(n) = T(n/2) + O(1) -> ~log2(n) levels,")
    print("  each level costs up to 2 comparisons -> about 2*log2(n).")
    print("  Ternary Search recurrence: T(n) = T(n/3) + O(1) -> ~log3(n) levels,")
    print("  but each level costs up to 4 comparisons -> about 4*log3(n) = 2.52*log2(n).")
    print("  So Ternary Search needs MORE comparisons than Binary Search in the")
    print("  worst case, even though it has fewer levels. In the best case both")
    print("  need only 1 comparison.\n")


def print_menu():
    print("=" * 55)
    print(" Binary Search vs Ternary Search - Menu")
    print("=" * 55)
    print("1. Generate n sorted random numbers -> Array")
    print("2. Display Array")
    print("3. Search for a key using Binary Search")
    print("4. Search for a key using Ternary Search")
    print("5. Step/frequency count - BEST case")
    print("6. Step/frequency count - WORST case")
    print("7. Step/frequency count comparison table across increasing n")
    print("8. Exit")


def main():
    actions = {
        "1": generate_array,
        "2": display_array,
        "3": search_with_binary,
        "4": search_with_ternary,
        "5": best_case_demo,
        "6": worst_case_demo,
        "7": comparison_table,
    }

    while True:
        print_menu()
        choice = input("Choose an option (1-8): ").strip()
        if choice == "8":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice, try again.\n")


if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------
# ANALYSIS / CONCLUSION (Binary vs Ternary Search)
# * Binary search:  T(n) = T(n/2) + O(1) -> O(log2 n) levels.
#   Each level makes up to 2 comparisons  -> about 2 * log2(n) in total.
# * Ternary search: T(n) = T(n/3) + O(1) -> O(log3 n) levels.
#   Each level makes up to 4 comparisons  -> about 4 * log3(n)
#   = 4 * log2(n) / 1.585 = 2.52 * log2(n) in total.
# * Best case: the key is the first element checked, so both need just
#   1 comparison -> O(1).
# * Worst case (key absent): ternary search has fewer levels but pays more
#   comparisons per level, so it makes MORE comparisons than binary search
#   (n = 1,000,000: binary 40 versus ternary 52; see the table, option 7).
# * Both algorithms are O(log n); they differ only by a constant factor.
#   Binary search is the better choice in practice.
# ---------------------------------------------------------------------
