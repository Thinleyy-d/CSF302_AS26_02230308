"""
frequency_count.py
--------------------
Q6: Given an array, count how many times each element appears.
"""


def frequency_count(arr):
    """
    Count occurrences of every element in arr.
    Returns a dict {element: count}, built with a single pass, O(n).
    """
    counts = {}
    for value in arr:
        counts[value] = counts.get(value, 0) + 1
    return counts


def main():
    raw = input("Enter numbers separated by spaces: ")
    arr = [int(x) for x in raw.split()]

    counts = frequency_count(arr)

    print("\nFrequency of each element:")
    for value, count in sorted(counts.items()):
        print(f"  {value} -> {count} time(s)")


if __name__ == "__main__":
    main()