# CSF302 — Lab 03: Divide and Conquer Algorithms

**Lab:** Lab 03 — Matrix Multiplication, Large Integer Multiplication, and Searching

## Files

| File | What it does |
|---|---|
| `matrix_mult.py` | Q1 — traditional matrix multiplication (O(n³)) + helper functions (random / manual input) |
| `strassen.py` | Q1 — Strassen's algorithm, comparison with traditional, step-count table + graph (needs `matrix_mult.py`) |
| `karatsuba.py` | Q2 — traditional vs Karatsuba on digit strings, step-count table + graph |
| `search.py` | Q3 — menu-driven Binary vs Ternary search with comparison counts |
| `*.png` | Graphs produced by the programs |


## Objective

Implement and compare three pairs of algorithms — one straightforward approach
and one divide-and-conquer approach — and understand why their complexities differ:

1. Matrix multiplication (Traditional vs. Strassen's Algorithm)
2. Large integer multiplication (Traditional vs. Karatsuba's Algorithm)
3. Searching in a sorted array (Binary Search vs. Ternary Search)

## Q1 — Matrix Multiplication: Traditional vs. Strassen's Algorithm

**Traditional:** every cell is a dot product of a row and a column → n³ multiplications → **O(n³)**.

**Strassen:** split each matrix into four quadrants and compute only **7** products
(M1…M7) instead of 8, using extra additions/subtractions:
`T(n) = 7T(n/2) + O(n²)` → **O(n^log₂7) ≈ O(n^2.81)**.

**Input:** random or typed in manually (power-of-2 sizes 2 … 128). Both result
matrices are displayed and the program verifies that they match.

### Step/frequency count table (random matrices)

| n | Trad mults | Trad adds | Strassen mults | Strassen adds | Trad time (s) | Strassen time (s) | Match |
|---|---|---|---|---|---|---|---|
| 2 | 8 | 8 | 7 | 18 | 0.000005 | 0.000022 | True |
| 4 | 64 | 64 | 49 | 198 | 0.000009 | 0.000088 | True |
| 8 | 512 | 512 | 343 | 1,674 | 0.000055 | 0.000605 | True |
| 16 | 4,096 | 4,096 | 2,401 | 12,870 | 0.000445 | 0.004421 | True |
| 32 | 32,768 | 32,768 | 16,807 | 94,698 | 0.003356 | 0.037481 | True |
| 64 | 262,144 | 262,144 | 117,649 | 681,318 | 0.026942 | 0.242829 | True |
| 128 | 2,097,152 | 2,097,152 | 823,543 | 4,842,954 | 0.286359 | 1.838263 | True |

Graph: `matrix_comparison.png`

### Analysis

Both methods always produced the same matrix. Strassen uses fewer multiplications
(exactly 7^log₂n; at n = 128 that is 823,543 vs 2,097,152) and the gap grows with n.
However, it does many more additions/subtractions and creates many small matrices
and recursive calls, so in pure Python the traditional method is faster in real
time at every size tested. Strassen's advantage in time only appears for much
larger matrices or in a compiled language.

## Q2 — Large Integer Multiplication: Traditional vs. Karatsuba's Algorithm

**Traditional:** every digit of one number times every digit of the other → n² steps → **O(n²)**.

**Karatsuba:** with `x = a·10^m + b` and `y = c·10^m + d`, only 3 multiplications are needed:

```
z2 = a·c
z0 = b·d
z1 = (a+b)(c+d) − z2 − z0
x·y = z2·10^(2m) + z1·10^m + z0
```

`T(n) = 3T(n/2) + O(n)` → **O(n^log₂3) ≈ O(n^1.585)**.

**Implementation notes:** numbers are stored as strings (so 1024-digit numbers work),
with hand-written string addition, subtraction and shifting. Operands are padded to
the same length, and to the next power of 2 before Karatsuba starts. Input can be
typed manually or generated randomly, and Karatsuba's answer is checked against the
traditional answer every time. A "step" is one single-digit multiplication.

### Step/frequency count table (random numbers)

| Digits | Trad steps | Karatsuba steps | Trad time (s) | Karatsuba time (s) | Match |
|---|---|---|---|---|---|
| 8 | 64 | 37 | 0.000032 | 0.000230 | True |
| 16 | 256 | 159 | 0.000068 | 0.001292 | True |
| 32 | 1,024 | 475 | 0.000297 | 0.002690 | True |
| 64 | 4,096 | 1,409 | 0.001030 | 0.008468 | True |
| 128 | 16,384 | 4,243 | 0.005031 | 0.022631 | True |
| 256 | 65,536 | 12,779 | 0.014850 | 0.068296 | True |
| 512 | 262,144 | 38,261 | 0.065336 | 0.208740 | True |
| 1024 | 1,048,576 | 115,051 | 0.259424 | 0.658553 | True |

Graph: `karatsuba_comparison.png`

### Analysis

Karatsuba always matched the traditional result and needs far fewer single-digit
multiplications as n grows (about 9 times fewer at 1024 digits). Because it also
performs many extra string additions/subtractions, it was still slower in real
running time for the sizes tested; it would win in time only for much larger numbers.

## Q3 — Binary Search vs. Ternary Search (menu-driven)

**Menu:** 1 generate n sorted random numbers, 2 display array, 3 binary search,
4 ternary search, 5 best-case count, 6 worst-case count, 7 comparison table, 8 exit.

Step/frequency count = number of comparisons with array elements. Binary search
makes up to 2 per level; ternary search makes up to 4 per level.

### Step/frequency count comparison table

| n | Binary best | Ternary best | Binary worst | Ternary worst | log₂n | log₃n |
|---|---|---|---|---|---|---|
| 10 | 1 | 1 | 8 | 8 | 3.32 | 2.10 |
| 100 | 1 | 1 | 14 | 16 | 6.64 | 4.19 |
| 1,000 | 1 | 1 | 20 | 24 | 9.97 | 6.29 |
| 10,000 | 1 | 1 | 28 | 36 | 13.29 | 8.38 |
| 100,000 | 1 | 1 | 34 | 44 | 16.61 | 10.48 |
| 1,000,000 | 1 | 1 | 40 | 52 | 19.93 | 12.58 |

Graph: `search_comparison.png`

### Analysis (recurrence relations)

- Binary search: `T(n) = T(n/2) + O(1)` → about log₂n levels × up to 2 comparisons ≈ **2·log₂n**.
- Ternary search: `T(n) = T(n/3) + O(1)` → about log₃n levels × up to 4 comparisons ≈ 4·log₂n / 1.585 ≈ **2.52·log₂n**.
- Best case: both find the key on the first probe → 1 comparison, O(1).
- Worst case: ternary has fewer levels but pays more comparisons per level, so it makes
  **more** comparisons than binary search. Both are O(log n); they differ only by a
  constant factor, and binary search is the better choice in practice.
