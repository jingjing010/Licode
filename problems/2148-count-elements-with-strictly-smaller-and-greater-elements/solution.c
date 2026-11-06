int countElements(int *nums, int numsSize) {
    int lo = nums[0], hi = nums[0], count = 0;
    for (int i = 0; i < numsSize; ++i) {
        if (nums[i] < lo)
            lo = nums[i];
        if (nums[i] > hi)
            hi = nums[i];
    }
    for (int i = 0; i < numsSize; ++i)
        if (nums[i] > lo && nums[i] < hi)
            ++count;
    return count;
}
