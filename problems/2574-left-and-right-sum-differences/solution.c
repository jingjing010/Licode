int *leftRightDifference(int *nums, int numsSize, int *returnSize) {
    int right = 0, left = 0, *out = malloc(numsSize * sizeof(int));
    for (int i = 0; i < numsSize; ++i)
        right += nums[i];
    for (int i = 0; i < numsSize; ++i) {
        right -= nums[i];
        out[i] = abs(left - right);
        left += nums[i];
    }
    *returnSize = numsSize;
    return out;
}
