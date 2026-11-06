int findLengthOfLCIS(int* nums, int numsSize) {
    int run = 0, best = 0;
    for (int i = 0; i < numsSize; ++i) {
        /* 相等也会中断严格递增区间。 */
        run = i > 0 && nums[i] > nums[i - 1] ? run + 1 : 1;
        if (run > best) best = run;
    }
    return best;
}
