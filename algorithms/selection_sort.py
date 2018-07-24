def sort(arr, a, b):
    for i in range(a, b):
        m = i
        for j in range(i + 1, b):
            if arr[j] < arr[m]:
                m = j
        arr.swap(i, m)