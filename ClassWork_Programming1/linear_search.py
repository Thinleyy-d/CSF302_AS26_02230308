"""
linear_search.py
------------------
Q2: Linear Search — check every element one by one until the key is
found (or the array ends). Works on both sorted and unsorted arrays.
Time complexity: O(n).
"""


def linear_search(arr, key):
    """
    Search for `key` in `arr` by checking each element in order.
    Returns the index of the first match, or -1 if not found.
    """
    for index, value in enumerate(arr):
        if value == key:
            return index
    return -1


def main():
    raw = input("Enter numbers separated by spaces: ")
    arr = [int(x) for x in raw.split()]
    key = int(input("Enter the number to search for: "))

    result = linear_search(arr, key)

    if result == -1:
        print(f"{key} was not found in the array.")
    else:
        print(f"{key} found at index {result}.")


if __name__ == "__main__":
    main()