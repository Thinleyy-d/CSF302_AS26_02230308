"""
search.py
----------
Menu-driven program: Binary Search vs Ternary Search.

Binary Search:  splits the array into 2 pieces each step
                 recurrence: T(n) = T(n/2) + O(1)  ->  O(log2 n)

Ternary Search: splits the array into 3 pieces each step
                 recurrence: T(n) = T(n/3) + O(1)  ->  O(log3 n)
                 BUT each step does 2 comparisons instead of 1,
                 so its real comparison count is close to
                 2 * log3(n) = 2 * log2(n)/log2(3) ~= 1.26 * log2(n)

So even though log3(n) < log2(n), Ternary Search usually does *more*
comparisons than Binary Search in practice, because it pays for an
extra comparison at every level. This program lets you see that for
yourself.
"""

import random
import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

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
        comparisons += 1
        if arr[mid] == key:
            return mid, comparisons
        comparisons += 1
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

        comparisons += 1
        if arr[mid1] == key:
            return mid1, comparisons

        comparisons += 1
        if arr[mid2] == key:
            return mid2, comparisons

        comparisons += 1
        if key < arr[mid1]:
            high = mid1 - 1
        else:
            comparisons += 1
            if key > arr[mid2]:
                low = mid2 + 1
            else:
                low, high = mid1 + 1, mid2 - 1

    return -1, comparisons


# ---------- menu option implementations ----------

def generate_array():
    global current_array
    try:
        n = int(input("How many numbers should the array contain? "))
        low = int(input("Lowest possible value: "))
        high = int(input("Highest possible value: "))
    except ValueError:
        print("Please enter valid integers.")
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
    key = int(input("Enter the key to search for: "))
    idx, comps = binary_search(current_array, key)
    if idx == -1:
        print(f"{key} not found. Comparisons made: {comps}\n")
    else:
        print(f"{key} found at index {idx}. Comparisons made: {comps}\n")


def search_with_ternary():
    if not current_array:
        print("No array yet. Use option 1 first.\n")
        return
    key = int(input("Enter the key to search for: "))
    idx, comps = ternary_search(current_array, key)
    if idx == -1:
        print(f"{key} not found. Comparisons made: {comps}\n")
    else:
        print(f"{key} found at index {idx}. Comparisons made: {comps}\n")


def best_case_demo():
    """
    Best case for both searches: the key is exactly where the
    algorithm looks first (the very first 'mid' it checks).
    """
    if not current_array:
        print("No array yet. Use option 1 first.\n")
        return
    n = len(current_array)
    # For binary search, the first mid checked is index n//2 (0-indexed via (0+n-1)//2)
    bin_mid = (0 + n - 1) // 2
    key_for_binary = current_array[bin_mid]
    _, bin_comps = binary_search(current_array, key_for_binary)

    # For ternary search, the first mid1 checked is at low + (high-low)//3
    ter_mid1 = 0 + (n - 1) // 3
    key_for_ternary = current_array[ter_mid1]
    _, ter_comps = ternary_search(current_array, key_for_ternary)

    print("Best case (key found on the very first probe):")
    print(f"  Binary Search  -> key={key_for_binary}, comparisons={bin_comps}")
    print(f"  Ternary Search -> key={key_for_ternary}, comparisons={ter_comps}\n")


def worst_case_demo():
    """
    Worst case for both searches: search for a key that does NOT
    exist in the array (forces the algorithm to narrow all the way
    down to an empty range).
    """
    if not current_array:
        print("No array yet. Use option 1 first.\n")
        return
    # Pick a value guaranteed not to be in the array
    missing_key = max(current_array) + 1
    _, bin_comps = binary_search(current_array, missing_key)
    _, ter_comps = ternary_search(current_array, missing_key)

    print("Worst case (key is absent from the array):")
    print(f"  Binary Search  -> comparisons={bin_comps}")
    print(f"  Ternary Search -> comparisons={ter_comps}\n")


def comparison_table():
    """
    Build (and plot) a table of worst-case comparison counts for
    Binary vs Ternary search across increasing array sizes.
    """
    sizes = [10, 100, 1_000, 10_000, 100_000, 1_000_000]
    rows = []

    print(f"{'n':>10} | {'Binary comps':>13} | {'Ternary comps':>14}")
    print("-" * 45)
    for n in sizes:
        arr = list(range(0, 2 * n, 2))  # sorted even numbers, length n
        missing_key = -1  # guaranteed absent -> worst case
        _, bin_comps = binary_search(arr, missing_key)
        _, ter_comps = ternary_search(arr, missing_key)
        rows.append((n, bin_comps, ter_comps))
        print(f"{n:>10} | {bin_comps:>13} | {ter_comps:>14}")

    # Plot it
    ns = [r[0] for r in rows]
    bins_ = [r[1] for r in rows]
    ters = [r[2] for r in rows]

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
    print("\nGraph saved as search_comparison.png")

    print("\nWhy this happens:")
    print("  Binary Search recurrence: T(n) = T(n/2) + O(1) -> ~log2(n) comparisons")
    print("  Ternary Search recurrence: T(n) = T(n/3) + O(1) -> ~log3(n) *levels*,")
    print("  but each level costs 2 comparisons instead of 1, so the real count")
    print("  is close to 2*log3(n) = 1.26*log2(n), which is MORE than log2(n).")
    print("  That's why Ternary Search usually needs more comparisons than Binary")
    print("  Search in practice, even though it 'divides' the array into more pieces.\n")


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