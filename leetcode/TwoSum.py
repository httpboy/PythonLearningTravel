class Solution:
    # 1.暴力解法
    def twoSum(self, nums, target):
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]

    # 2.两遍哈希表法
    def twoSum2(self, nums, target):
        hashdict = {num: index for index, num in enumerate(nums)}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in hashdict and i != hashdict[complement]:
                return [i, hashdict[complement]]


# 给定一个整数数组 nums 和一个目标值 target，
# 请你在该数组中找出和为目标值的那 两个 整数，
# 并返回他们的数组下标。
# 你可以假设每种输入只会对应一个答案。但是，你不能重复利用这个数组中同样的元素。
# 示例:
# 给定 nums = [2, 7, 11, 15], target = 9
# 因为 nums[0] + nums[1] = 2 + 7 = 9
# 所以返回 [0, 1]
if __name__ == "__main__":
    nums = (2, 7, 11, 15)
    target = 9
# toSums = Solution().twoSum(nums, target)
toSums = Solution().twoSum2(nums, target)
print(toSums)

