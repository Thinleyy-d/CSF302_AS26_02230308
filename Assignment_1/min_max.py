"""
min_max.py
-----------
Q1: Store n random integers in an array and find the smallest and
largest values in it. n is entered by the user.
"""

import random


def generate_random_array(n, low=0, high=100):
    """Return a list of n random integers between low and high (inclusive)."""
    return [random.randint(low, high) for _ in range(n)]


def find_min_max(arr):
    """
    Scan the array once, keeping track of the smallest and largest
    values seen so far. O(n) time, O(1) extra space.
    """
    if not arr:
        return None, None

    smallest = arr[0]
    largest = arr[0]

    for value in arr[1:]:
        if value < smallest:
            smallest = value
        if value > largest:
            largest = value

    return smallest, largest


def main():
    n = int(input("Enter the number of elements (n): "))
    low = int(input("Enter the lowest possible random value: "))
    high = int(input("Enter the highest possible random value: "))

    arr = generate_random_array(n, low, high)
    print("\nGenerated array:", arr)

    smallest, largest = find_min_max(arr)
    print(f"Smallest number: {smallest}")
    print(f"Largest number:  {largest}")


if __name__ == "__main__":
    main()