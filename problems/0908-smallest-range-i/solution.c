int smallestRangeI(int *nums, int numsSize, int k) {
    int lo = nums[0], hi = nums[0];
    for (int i = 1; i < numsSize; ++i) {
        if (nums[i] < lo)
            lo = nums[i];
        if (nums[i] > hi)
            hi = nums[i];
    }
    int gap = hi - lo - 2 * k;
    return gap > 0 ? gap : 0;
}
