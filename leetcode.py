def merge(nums1: List[int], m: int, nums2: List[int], n: int) -> None:
    for i in range(m - 1, -1, -1):
        nums1[i + n] = nums1[i]
    for i in range(n):
        nums1[i] = nums2[i]




nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3
print(merge(nums1, m, nums2, n))
nums1 = [1], m = 1, nums2 = [], n = 0
print(merge(nums1, m, nums2, n))
nums1 = [0], m = 0, nums2 = [1], n = 1
print(merge(nums1, m, nums2, n))