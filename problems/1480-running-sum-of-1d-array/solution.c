int *runningSum(int *nums, int numsSize, int *returnSize) {
    int *out = malloc(numsSize * sizeof(int)), sum = 0;
    for (int i = 0; i < numsSize; ++i) {
        sum += nums[i];
        out[i] = sum;
    }
    *returnSize = numsSize;
    return out;
}
