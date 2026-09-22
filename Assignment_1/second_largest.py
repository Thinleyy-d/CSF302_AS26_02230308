"""
second_largest.py
--------------------
Q7: Find the second largest element in an array.

Done with a single pass (no sorting needed) by tracking the largest
and second-largest values seen so far as we scan the array. O(n) time.
"""


def second_largest(arr):
    """
    Return the second largest DISTINCT value in arr.
    Returns None if arr has fewer than 2 distinct values.
    """
    first = second = None

    for value in arr:
        if first is None or value > first:
            # New overall largest found; the old largest becomes 2nd
            second = first
            first = value
        elif value != first and (second is None or value > second):
            # New second-largest found (must be different from 'first')
            second = value

    return second


def main():
    raw = input("Enter numbers separated by spaces: ")
    arr = [int(x) for x in raw.split()]

    result = second_largest(arr)

    if result is None:
        print("The array doesn't have two distinct values.")
    else:
        print(f"Second largest element: {result}")


if __name__ == "__main__":
    main()