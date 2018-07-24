def sort(arr, a, b):
    for i in range(a + 1, b):
        j = i
        while j > a and arr[j] < arr[j-1]:
            arr.swap(j, j-1)
            j -= 1