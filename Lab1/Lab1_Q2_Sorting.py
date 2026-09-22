import random
import time
import copy


def BubbleSort_308(arr):
    n_308 = len(arr)
    for i in range(n_308):
        for j in range(0, n_308 - i - 1):
            if arr[j] > arr[j + 1]:
                # swap
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def Merge_308(left_308, right_308):
    result_308 = []
    i_308 = 0
    j_308 = 0

    while i_308 < len(left_308) and j_308 < len(right_308):
        if left_308[i_308] <= right_308[j_308]:
            result_308.append(left_308[i_308])
            i_308 += 1
        else:
            result_308.append(right_308[j_308])
            j_308 += 1

    # add any leftover elements
    result_308.extend(left_308[i_308:])
    result_308.extend(right_308[j_308:])
    return result_308


def MergeSort_308(arr):
    if len(arr) <= 1:
        return arr

    mid_308 = len(arr) // 2
    left_half_308 = MergeSort_308(arr[:mid_308])
    right_half_308 = MergeSort_308(arr[mid_308:])

    return Merge_308(left_half_308, right_half_308)


def GenerateArray_308(n):
    arr_308 = []
    for i in range(n):
        arr_308.append(random.randint(1, n * 10))
    return arr_308


def Main_308():
    sizes_308 = [100, 500, 1000, 2000, 4000, 8000]
    trials_308 = 3  # bubble sort is slow, so fewer trials

    print(f"{'Size':<10}{'Bubble Sort (s)':<20}{'Merge Sort (s)':<20}")
    print("-" * 50)

    for size_308 in sizes_308:
        total_bubble_308 = 0
        total_merge_308 = 0

        for t in range(trials_308):
            base_array_308 = GenerateArray_308(size_308)

            # ---- Bubble Sort timing ----
            bubble_array_308 = copy.deepcopy(base_array_308)
            start_308 = time.time()
            BubbleSort_308(bubble_array_308)
            end_308 = time.time()
            total_bubble_308 += (end_308 - start_308)

            # ---- Merge Sort timing ----
            merge_array_308 = copy.deepcopy(base_array_308)
            start_308 = time.time()
            MergeSort_308(merge_array_308)
            end_308 = time.time()
            total_merge_308 += (end_308 - start_308)

        avg_bubble_308 = total_bubble_308 / trials_308
        avg_merge_308 = total_merge_308 / trials_308

        print(f"{size_308:<10}{avg_bubble_308:<20.8f}{avg_merge_308:<20.8f}")


if __name__ == "__main__":
    Main_308()