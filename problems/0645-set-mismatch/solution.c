int *findErrorNums(int *nums, int numsSize, int *returnSize) {
    int *counts = calloc(numsSize + 1, sizeof(int)), *out = malloc(2 * sizeof(int));
    for (int i = 0; i < numsSize; ++i)
        ++counts[nums[i]];
    for (int x = 1; x <= numsSize; ++x) {
        if (counts[x] == 2)
            out[0] = x;
        if (counts[x] == 0)
            out[1] = x;
    }
    free(counts);
    *returnSize = 2;
    return out;
}
