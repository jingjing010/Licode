int findClosestNumber(int *nums, int numsSize) {
    int best = nums[0];
    for (int i = 1; i < numsSize; ++i)
        if (abs(nums[i]) < abs(best) || (abs(nums[i]) == abs(best) && nums[i] > best))
            best = nums[i];
    return best;
}
