# def linear(list,target):
#     for i in range(0,len(list)):
#         if list[i] == target:
#             return target
#     return None
        
# def verify(result):
#     if result is not None:
#         print('Your result is:',result)
#     else:
#         print('Target does not exists')

# nums = [1,2,3,4,5,6,7,8,9,10]
# list = linear(nums,7)
# verify(list)

# def binary(nums,target):
#     first = 0
#     last = len(nums) - 1
#     while first <= last:
#         midpoint = (first + last) // 2
#
#         if nums[midpoint] == target:
#             return midpoint
#         elif nums[midpoint] < target:
#             first = midpoint + 1
#         else:
#             last = midpoint - 1
#     return None
#
#
# def verify(index):
#     if index is not None:
#         print('Target found at index:',index)
#     else:
#         print('Target does not exists')
#
# numbers = [1,2,3,4,5,6,7,8,9,10]
#
# loop = binary(numbers,6)
# verify(loop)
#
# loop = binary(numbers,19)
# verify(loop)


# def recursive_binary(nums,target):
#     if len(nums) == 0:
#         return None
#     else:
#         midpoint = len(nums) // 2
#     if nums[midpoint] == target:
#         return target
#     elif nums[midpoint] < target:
#         return recursive_binary(nums[midpoint + 1:],target)
#     elif nums[midpoint] > target:
#         return recursive_binary(nums[:midpoint],target)
# def verify(result):
#     print('Your result is in index:',result)
# numbers = [1,2,3,4,5,6,7,8,9,10]
# result = recursive_binary(numbers,12)
# verify(result)

# def binary(nums,target):
#     first = 0
#     last = len(nums) - 1
#     while first <= last:
#         midpoint = (first + last) // 2
#         if nums[midpoint] == target:
#             return midpoint
#         elif nums[midpoint] < target:
#             first = midpoint + 1
#         elif nums[midpoint] > target:
#             last = midpoint - 1
#         else:
#             return None
# def verify(result):
#     if result is not None:
#         print('Your result in index',result)
#     else:
#         print('Result does not exists')
# numbers = [1,2,3,4,5,6,7,8,9,10]
# binary = binary(numbers,9)
# verify(binary)


# def merge_sort(list):
#     if len(list) <= 1:
#         return list
#     left_half,right_half = split(list)
#     left = merge_sort(left_half)
#     right = merge_sort(right_half)
#     return merge(left,right)

# def split(list):
#     mid = len(list) // 2
#     left = list[:mid]
#     right = list[mid:]
#     return left,right

# def merge(left,right):
#     l = []
#     j = 0
#     i = 0
#     while i < len(left) and j < len(right):
#         if left[i] < right[j]:
#             l.append(right[j])
#             i = i + 1
#         else:
#             l.append(right[j])
#             j = j + 1
#     while i < len(left):
#         l.append(left[i])
#         i = i + 1
#     while j < len(right):
#         l.append(right[j])
#         j = j + 1
#     return l
# nums = [2,56,89,12,14,16]
# l = merge_sort(nums)
# print(l)