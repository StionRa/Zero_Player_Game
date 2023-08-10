list_x = [5, 64, 88, 787, 91, 121, 44, 67, 43, 89, 22, 121, 78, 121, 43, 85, 98, 100, 5, 7, 11, 53, 11, 2]


def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


bubble_sort(list_x)
print(list_x)

result = []
unique_list = []
for i in range(len(unique_list)):
    for j in range(i + 1, len(unique_list)):
        for k in range(j + 1, len(unique_list)):
            if unique_list[i] + unique_list[j] + unique_list[k] < 50:
                 result.append([unique_list[i], unique_list[j], unique_list[k]])
for lst in result:
    print(lst)
