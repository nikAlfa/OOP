# #Сортировка посредством выбора
# def selection_sort(arr):
#     n = len(arr)
#     for i in range(n):
#         min_idx = i
#         for j in range(i + 1, n):
#             if arr[j] < arr[min_idx]:
#                 min_idx = j
#         arr[i], arr[min_idx] = arr[min_idx], arr[i]
#     return arr
#
# if name == "main":
#     print("Введите числа через пробел:")
#     arr = list(map(float, input().split()))
#
#
#     result = selection_sort(arr)
#     print(result)
#
# # №7 Сортировка Шелла
# def shell_sort(arr):
#     n = len(arr)
#     gap = n // 2
#     while gap > 0:
#         for i in range(gap, n):
#             temp = arr[i]
#             j = i
#             while j >= gap and arr[j - gap] > temp:
#                 arr[j] = arr[j - gap]
#                 j -= gap
#             arr[j] = temp
#         gap //= 2
#     return arr
# if name == "main":
#     print("Введите числа через пробел:")
#     arr = list(map(float, input().split()))
#
#
#     result = shell_sort(arr)
#     print(result)
#
# # №8 Поразрядная сортировка
# def radix_sort(arr):
#     if not arr:
#         return arr
#     max_num = max(arr)
#     exp = 1
#     while max_num // exp > 0:
#         buckets = [[] for _ in range(10)]
#         for num in arr:
#             buckets[(num // exp) % 10].append(num)
#         arr = [num for bucket in buckets for num in bucket]
#         exp *= 10
#     return arr
#
# if name == "main":
#     print("Введите числа через пробел:")
#     arr = list(map(float, input().split()))
#
#     result = radix_sort(arr)
#     print(result)
#
# # №9 Пирамидальная сортировка
# def heapify(arr, n, i):
#     largest = i
#     left = 2 * i + 1
#     right = 2 * i + 2
#     if left < n and arr[left] > arr[largest]:
#         largest = left
#     if right < n and arr[right] > arr[largest]:
#         largest = right
#     if largest != i:
#         arr[i], arr[largest] = arr[largest], arr[i]
#         heapify(arr, n, largest)
#
# def heap_sort(arr):
#     n = len(arr)
#     for i in range(n // 2 - 1, -1, -1):
#         heapify(arr, n, i)
#     for i in range(n - 1, 0, -1):
#         arr[0], arr[i] = arr[i], arr[0]
#         heapify(arr, i, 0)
#     return arr
#
# if name == "main":
#     print("Введите числа через пробел:")
#     arr = list(map(float, input().split()))
#
#     result = heap_sort(arr)
#     print(result)
#
# # №10 Сортировка слиянием
# def merge_sort(arr):
#     if len(arr) <= 1:
#         return arr
#     mid = len(arr) // 2
#     left = merge_sort(arr[:mid])
#     right = merge_sort(arr[mid:])
#     return merge(left, right)
#
#
# def merge(left, right):
#     result = []
#     i = j = 0
#     while i < len(left) and j < len(right):
#         if left[i] <= right[j]:
#             result.append(left[i])
#             i += 1
#         else:
#             result.append(right[j])
#             j += 1
#     result.extend(left[i:])
#     result.extend(right[j:])
#     return result
#
# if name == "main":
#     print("Введите числа через пробел:")
#     arr = list(map(float, input().split()))
#
#     result = merge_sort(arr)
#     print(result)
#
# # №11 Быстрая сортировка
# def quick_sort(arr):
#     if len(arr) <= 1:
#         return arr
#     pivot = arr[len(arr) // 2]
#     left = [x for x in arr if x < pivot]
#     middle = [x for x in arr if x == pivot]
#     right = [x for x in arr if x > pivot]
#     return quick_sort(left) + middle + quick_sort(right)
#
# if name == "main":
#     print("Введите числа через пробел:")
#     arr = list(map(float, input().split()))
#
#     result = quick_sort(arr)
#     print(result)
