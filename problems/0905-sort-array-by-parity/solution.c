int* sortArrayByParity(int* nums, int numsSize, int* returnSize) {
    int *out = malloc(numsSize * sizeof(int));
    int k = 0;
    for (int parity = 0; parity <= 1; ++parity) {
        for (int i = 0; i < numsSize; ++i) {
            if (nums[i] % 2 == parity) out[k++] = nums[i];
        }
    }
    *returnSize = numsSize;
    return out;
}
