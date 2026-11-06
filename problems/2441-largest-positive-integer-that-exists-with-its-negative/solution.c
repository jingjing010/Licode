int findMaxK(int *nums, int numsSize) {
    bool seen[2001] = {false};
    for (int i = 0; i < numsSize; ++i)
        seen[nums[i] + 1000] = true;
    for (int k = 1000; k > 0; --k)
        if (seen[1000 + k] && seen[1000 - k])
            return k;
    return -1;
}
