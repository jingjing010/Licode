int maximumProduct(int *nums, int numsSize) {
    int a = INT_MIN, b = INT_MIN, c = INT_MIN, x = INT_MAX, y = INT_MAX;
    for (int i = 0; i < numsSize; ++i) {
        int v = nums[i];
        if (v > a) {
            c = b;
            b = a;
            a = v;
        } else if (v > b) {
            c = b;
            b = v;
        } else if (v > c)
            c = v;
        if (v < x) {
            y = x;
            x = v;
        } else if (v < y)
            y = v;
    }
    /* 两个很小的负数相乘也可能产生最大结果。 */
    int p = a * b * c, q = a * x * y;
    return p > q ? p : q;
}
