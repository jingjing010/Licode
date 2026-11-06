int arraySign(int *nums, int numsSize) {
    int sign = 1;
    /* 只跟踪符号，避免计算实际乘积导致溢出。 */
    for (int i = 0; i < numsSize; ++i) {
        if (nums[i] == 0)
            return 0;
        if (nums[i] < 0)
            sign = -sign;
    }
    return sign;
}
