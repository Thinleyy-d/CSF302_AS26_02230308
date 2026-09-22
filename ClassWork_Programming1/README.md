# Arrays, Searching, Shapes, Fibonacci

## Files

| File | Question | What it does |
|---|---|---|
| `min_max.py` | Q1 | Fills an array of n random integers (n from user input) and finds the smallest and largest values. |
| `linear_search.py` | Q2 | Linear Search — checks each element in turn until the key is found. |
| `binary_search.py` | Q3 | Binary Search — sorts the input first, then repeatedly halves the search range. |
| `shapes.py` | Q4 | Menu-driven area/volume calculator: circle, sphere, cone, pyramid, cylinder, rectangle, and a custom regular polygon (any n sides). |
| `fibonacci.py` | Q5 | Generates the first n Fibonacci numbers both iteratively and recursively. |
| `frequency_count.py` | Q6 | Counts how many times each element appears in an array. |
| `second_largest.py` | Q7 | Finds the second largest (distinct) element in an array in a single pass. |


## Notes

- `min_max.py`, `linear_search.py`, `frequency_count.py`, and
  `second_largest.py` all expect numbers typed on one line separated
  by spaces, e.g. `5 2 9 1 7`.
- `binary_search.py` sorts whatever you type in before searching,
  since binary search only works on sorted arrays.
- `shapes.py` option **g** (custom polygon) uses the general regular
  polygon area formula `(n * s²) / (4 * tan(π/n))`, which works for
  any number of sides n ≥ 3 — triangle, pentagon, hexagon, and so on.
- `fibonacci.py` shows two implementations of the same sequence: an
  efficient loop-based one and the classic (slower) recursive
  definition, so you can compare them directly.