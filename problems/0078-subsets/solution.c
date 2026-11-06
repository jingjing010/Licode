int** subsets(int* nums, int numsSize, int* returnSize, int** returnColumnSizes) {
    int total = 1 << numsSize;
    int** res = (int**)malloc(sizeof(int*) * total);
    *returnColumnSizes = (int*)malloc(sizeof(int) * total);
    for (int mask = 0; mask < total; mask++) {
        res[mask] = (int*)malloc(sizeof(int) * (numsSize + 1));
        int k = 0;
        for (int j = 0; j < numsSize; j++)
            if (mask >> j & 1) res[mask][k++] = nums[j];
        (*returnColumnSizes)[mask] = k;
    }
    *returnSize = total;
    return res;
}
