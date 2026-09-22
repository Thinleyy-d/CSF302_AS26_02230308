# CSF302 — Lab 03: Divide and Conquer Algorithms

**Lab:** Lab 03 — Matrix Multiplication, Large Integer Multiplication, and Searching

## Objective

The purpose of this lab was to implement and compare three pairs of
algorithms — one straightforward approach and one divide-and-conquer
approach — for each of the following problems, and to understand why
their theoretical time complexities differ:

1. Matrix multiplication (Traditional vs. Strassen's Algorithm)
2. Large integer multiplication (Traditional vs. Karatsuba's Algorithm)
3. Searching in a sorted array (Binary Search vs. Ternary Search)

## Q1 — Matrix Multiplication: Traditional vs. Strassen's Algorithm

### Understanding

The traditional method computes each entry of the product matrix as
a dot product of a row and a column, requiring n multiplications per
entry and n² entries, giving **O(n³)** multiplications overall.

Strassen's algorithm splits each n×n matrix into four (n/2)×(n/2)
quadrants. A naive divide-and-conquer approach would still need 8
recursive multiplications (one per quadrant pair), which does not
improve on O(n³). Strassen showed that the product can instead be
computed using only **7** recursive multiplications, by combining the
quadrants into specific sums and differences before multiplying. This
changes the recurrence from

```
T(n) = 8T(n/2) + O(n²)   (naive divide-and-conquer, still O(n³))
```

to

```
T(n) = 7T(n/2) + O(n²)   (Strassen's algorithm)
```

which solves to **O(n^log2(7)) ≈ O(n^2.807)** by the Master Theorem —
an asymptotic improvement over O(n³), paid for by extra matrix
additions/subtractions at every level of recursion.

### Implementation

- `matrix_mult.py` implements the traditional triple-nested-loop
  multiplication and a random matrix generator.
- `strassen.py` implements Strassen's algorithm recursively (base
  case: 1×1 matrices), using helper functions to split a matrix into
  quadrants, add/subtract matrices, and recombine quadrants into the
  final result.
- Both algorithms were run on randomly generated matrices of sizes
  2, 4, 8, 16, 32, 64, and 128 (all powers of 2, as required), and
  their outputs were compared element-by-element to confirm
  correctness.

### Results

| n | Traditional (s) | Strassen (s) | Match |
|---|---|---|---|
| 2 | 0.000005 | 0.000023 | True |
| 4 | 0.000007 | 0.000151 | True |
| 8 | 0.000028 | 0.000687 | True |
| 16 | 0.000250 | 0.004676 | True |
| 32 | 0.001377 | 0.035023 | True |
| 64 | 0.010774 | 0.245406 | True |
| 128 | 0.087559 | 1.733820 | True |

Graph: `matrix_comparison.png`

### Analysis

All outputs matched between the two methods, confirming Strassen's
algorithm was implemented correctly. However, in this pure Python
implementation, the traditional method was consistently **faster**
than Strassen's at every tested size. This is expected: Strassen's
theoretical advantage (O(n^2.807) vs. O(n³)) only becomes visible once
n is large enough that the reduction in multiplications outweighs the
extra addition/subtraction operations and, in Python specifically, the
overhead of many recursive function calls. A lower-level/compiled
implementation, or much larger matrices, would be needed to observe
Strassen's crossover point in practice.

## Q2 — Large Integer Multiplication: Traditional vs. Karatsuba's Algorithm

### Understanding

The traditional grade-school method multiplies every digit of one
number by every digit of the other and sums the shifted partial
products, giving **O(n²)** work for n-digit numbers.

Karatsuba's algorithm splits each number into a high half and a low
half (`x = x_high·10^m + x_low`). A naive split needs 4
sub-multiplications, but Karatsuba computes the product using only
**3**:

```
z2 = x_high · y_high
z0 = x_low  · y_low
z1 = (x_high + x_low)(y_high + y_low) − z2 − z0
result = z2·10^(2m) + z1·10^m + z0
```

This gives the recurrence

```
T(n) = 3T(n/2) + O(n)
```

which solves to **O(n^log2(3)) ≈ O(n^1.585)** — asymptotically faster
than the traditional O(n²) method.

### Implementation

- `karatsuba.py` implements the traditional method by hand using
  digit arrays (not just Python's built-in `*` operator), and
  Karatsuba's algorithm recursively, with a base case for
  single-digit-scale numbers.
- Both methods were tested on randomly generated numbers with 8, 16,
  32, 64, 128, 256, 512, and 1024 digits, and their outputs were
  compared to confirm correctness.

### Results

| Digits | Traditional (s) | Karatsuba (s) | Match |
|---|---|---|---|
| 8 | 0.000039 | 0.000023 | True |
| 16 | 0.000053 | 0.000055 | True |
| 32 | 0.000098 | 0.000142 | True |
| 64 | 0.000335 | 0.000385 | True |
| 128 | 0.001184 | 0.001212 | True |
| 256 | 0.005075 | 0.003484 | True |
| 512 | 0.022654 | 0.010535 | True |
| 1024 | 0.092373 | 0.031971 | True |

Graph: `karatsuba_comparison.png`

### Analysis

All outputs matched. For small numbers of digits, the traditional
method was actually slightly faster, since Karatsuba's recursive
overhead outweighs its algorithmic savings when n is small. The
crossover point appears between roughly 128 and 256 digits, after
which Karatsuba pulls ahead — at 1024 digits it is roughly 3× faster
than the traditional method. This matches the expected difference
between O(n²) and O(n^1.585) growth.

## Q3 — Searching: Binary Search vs. Ternary Search

### Understanding

Binary Search discards half the remaining search space at each step,
giving the recurrence

```
T(n) = T(n/2) + O(1)   →   O(log2 n)
```

Ternary Search discards two-thirds of the remaining search space at
each step by checking two midpoints, giving the recurrence

```
T(n) = T(n/3) + O(1)   →   O(log3 n) levels
```

However, each level of Ternary Search costs **2** comparisons
(checking both midpoints) rather than 1. So its true comparison count
is closer to `2·log3(n)`, which — because `log3(n) = log2(n)/log2(3)`
— works out to approximately `1.26·log2(n)`. This is **more** than
Binary Search's `log2(n)`, even though Ternary Search divides the
array into more pieces per step. This was the central hypothesis
tested in this section.

### Implementation

`search.py` is a menu-driven program with the following options:

1. Generate n sorted random numbers into an array
2. Display the array
3. Search for a key with Binary Search
4. Search for a key with Ternary Search
5. Show best-case comparison counts (key found on the first probe)
6. Show worst-case comparison counts (key absent from the array)
7. Show a comparison table of worst-case comparisons across
   increasing n, with a corresponding graph

### Results

Worst-case comparisons (key absent), across increasing array size:

| n | Binary comparisons | Ternary comparisons |
|---|---|---|
| 10 | 6 | 6 |
| 100 | 12 | 12 |
| 1,000 | 18 | 18 |
| 10,000 | 26 | 27 |
| 100,000 | 32 | 33 |
| 1,000,000 | 38 | 39 |

Graph: `search_comparison.png`

### Analysis

Binary Search used fewer or an equal number of comparisons compared
to Ternary Search at every tested array size, confirming the
hypothesis above. Although Ternary Search has a smaller number of
*levels* of recursion (log3 n < log2 n), the extra comparison it
performs at each level more than cancels out that advantage. This
result illustrates an important lesson: a smaller number of
recursive levels does not automatically mean fewer total
comparisons — the cost per level matters just as much as the number
of levels.

## Overall Conclusion

Across all three experiments, the divide-and-conquer algorithm was
implemented correctly (verified by exact output matches against the
traditional method in every test case), and each showed the expected
theoretical behaviour once analysed carefully:

- **Strassen's algorithm** has a better asymptotic complexity than
  traditional matrix multiplication, but its constant-factor overhead
  means the crossover point is not reached at the matrix sizes tested
  here in a pure Python implementation.
- **Karatsuba's algorithm** clearly outperforms traditional
  multiplication once integers reach a few hundred digits, matching
  its O(n^1.585) vs. O(n²) advantage.
- **Ternary Search**, despite intuitively "dividing more," performs
  *more* comparisons than Binary Search in practice, because of the
  extra comparison required at each level — a good reminder that
  algorithmic complexity depends on the total work done, not just the
  number of recursive levels.
