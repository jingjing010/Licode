int *sortedSquares(int *nums, int numsSize, int *returnSize) {
    int *out = malloc(numsSize * sizeof(int)), l = 0, r = numsSize - 1;
    /* 最大绝对值位于两端，从结果末尾向前填。 */
    for (int i = numsSize - 1; i >= 0; --i) {
        int a = nums[l] * nums[l], b = nums[r] * nums[r];
        if (a > b) {
            out[i] = a;
            ++l;
        } else {
            out[i] = b;
            --r;
        }
    }
    *returnSize = numsSize;
    return out;
}
