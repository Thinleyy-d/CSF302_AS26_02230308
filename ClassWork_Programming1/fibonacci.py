"""
fibonacci.py
-------------
Q5: Fibonacci Sequence — each number is the sum of the two before it:
0, 1, 1, 2, 3, 5, 8, 13, 21, ...

Two versions are given:
  - fibonacci_iterative: builds the sequence with a simple loop. O(n) time.
  - fibonacci_recursive: the classic recursive definition. O(2^n) time
    (much slower — included to show the textbook definition, and to
    compare against the efficient iterative version).
"""


def fibonacci_iterative(n):
    """Return a list of the first n Fibonacci numbers, built with a loop."""
    if n <= 0:
        return []
    sequence = [0, 1]
    while len(sequence) < n:
        sequence.append(sequence[-1] + sequence[-2])
    return sequence[:n]


def fibonacci_recursive(k):
    """
    Return the k-th Fibonacci number (0-indexed: fib(0)=0, fib(1)=1)
    using plain recursion, following the textbook definition
    fib(k) = fib(k-1) + fib(k-2).
    """
    if k <= 1:
        return k
    return fibonacci_recursive(k - 1) + fibonacci_recursive(k - 2)


def main():
    n = int(input("How many Fibonacci numbers to generate? "))

    print("\nIterative version:")
    print(fibonacci_iterative(n))

    print("\nRecursive version (same numbers, one at a time):")
    recursive_sequence = [fibonacci_recursive(k) for k in range(n)]
    print(recursive_sequence)


if __name__ == "__main__":
    main()