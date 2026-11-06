int getMinDistance(int *nums, int numsSize, int target, int start) {
    int best = numsSize;
    for (int i = 0; i < numsSize; ++i)
        if (nums[i] == target) {
            int d = abs(i - start);
            if (d < best)
                best = d;
        }
    return best;
}
