/* 原地置换：把 x 放到下标 x-1，O(n) 时间 O(1) 额外空间 */
int firstMissingPositive(int* nums, int numsSize) {
    int n = numsSize;
    for (int i = 0; i < n; i++) {
        while (nums[i] >= 1 && nums[i] <= n && nums[nums[i] - 1] != nums[i]) {
            int j = nums[i] - 1;
            int t = nums[j];
            nums[j] = nums[i];
            nums[i] = t;
        }
    }
    for (int i = 0; i < n; i++)
        if (nums[i] != i + 1) return i + 1;
    return n + 1;
}
