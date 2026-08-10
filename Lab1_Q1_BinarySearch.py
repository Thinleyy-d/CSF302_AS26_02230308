import random
import time


def LinearSearch_308(arr, target):
    # Go through every element one by one
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1


def BinarySearch_308(arr, target):
    # Array must be sorted before calling this function
    low_308 = 0
    high_308 = len(arr) - 1

    while low_308 <= high_308:
        mid_308 = (low_308 + high_308) // 2

        if arr[mid_308] == target:
            return mid_308
        elif arr[mid_308] < target:
            low_308 = mid_308 + 1
        else:
            high_308 = mid_308 - 1

    return -1


def GenerateData_308(n):
    # Create a list of n random numbers
    data_308 = []
    for i in range(n):
        data_308.append(random.randint(1, n * 10))
    return data_308


def Main_308():
    sizes_308 = [1000, 5000, 10000, 50000, 100000, 500000, 1000000]
    trials_308 = 5  # run a few times and take the average

    print(f"{'Size':<12}{'Linear Search (s)':<22}{'Binary Search (s)':<22}")
    print("-" * 56)

    for size_308 in sizes_308:
        data_308 = GenerateData_308(size_308)
        target_308 = data_308[random.randint(0, size_308 - 1)]

        # ---- Linear Search timing (on unsorted data) ----
        total_linear_308 = 0
        for t in range(trials_308):
            start_308 = time.time()
            LinearSearch_308(data_308, target_308)
            end_308 = time.time()
            total_linear_308 += (end_308 - start_308)
        avg_linear_308 = total_linear_308 / trials_308

        # ---- Sort the dataset before Binary Search ----
        sorted_data_308 = sorted(data_308)

        # ---- Binary Search timing (on sorted data) ----
        total_binary_308 = 0
        for t in range(trials_308):
            start_308 = time.time()
            BinarySearch_308(sorted_data_308, target_308)
            end_308 = time.time()
            total_binary_308 += (end_308 - start_308)
        avg_binary_308 = total_binary_308 / trials_308

        print(f"{size_308:<12}{avg_linear_308:<22.8f}{avg_binary_308:<22.8f}")


if __name__ == "__main__":
    Main_308()