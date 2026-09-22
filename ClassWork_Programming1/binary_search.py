"""
binary_search.py
------------------
Q3: Binary Search — repeatedly narrows the search range in half.
REQUIRES the array to be sorted first. Time complexity: O(log n).
"""


def binary_search(arr, key):
    """
    Search for `key` in a sorted array `arr` using binary search.
    Returns the index of the match, or -1 if not found.
    """
    low, high = 0, len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == key:
            return mid
        elif arr[mid] < key:
            low = mid + 1          # key must be in the right half
        else:
            high = mid - 1         # key must be in the left half

    return -1


def main():
    raw = input("Enter numbers separated by spaces: ")
    arr = sorted(int(x) for x in raw.split())  # binary search needs sorted input
    print("Sorted array used for the search:", arr)

    key = int(input("Enter the number to search for: "))

    result = binary_search(arr, key)

    if result == -1:
        print(f"{key} was not found in the array.")
    else:
        print(f"{key} found at index {result}.")


if __name__ == "__main__":
    main()