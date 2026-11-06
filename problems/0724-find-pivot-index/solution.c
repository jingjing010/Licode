int pivotIndex(int *nums, int numsSize) {
    int total = 0, left = 0;
    for (int i = 0; i < numsSize; ++i)
        total += nums[i];
    for (int i = 0; i < numsSize; ++i) {
        /* 右边总和等于总和减左边再减当前元素。 */
        if (left == total - left - nums[i])
            return i;
        left += nums[i];
    }
    return -1;
}
