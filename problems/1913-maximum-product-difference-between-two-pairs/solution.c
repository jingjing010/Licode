int maxProductDifference(int *nums, int numsSize) {
    int a = 0, b = 0, x = INT_MAX, y = INT_MAX;
    for (int i = 0; i < numsSize; ++i) {
        int v = nums[i];
        if (v >= a) {
            b = a;
            a = v;
        } else if (v > b)
            b = v;
        if (v <= x) {
            y = x;
            x = v;
        } else if (v < y)
            y = v;
    }
    return a * b - x * y;
}
