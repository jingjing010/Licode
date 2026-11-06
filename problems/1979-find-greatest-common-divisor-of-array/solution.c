int findGCD(int *nums, int numsSize) {
    int lo = nums[0], hi = nums[0];
    for (int i = 1; i < numsSize; ++i) {
        if (nums[i] < lo)
            lo = nums[i];
        if (nums[i] > hi)
            hi = nums[i];
    }
    /* 欧几里得算法每轮把大数换成除法余数。 */
    while (lo) {
        int r = hi % lo;
        hi = lo;
        lo = r;
    }
    return hi;
}
