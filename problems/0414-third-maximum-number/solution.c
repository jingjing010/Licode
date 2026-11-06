int thirdMax(int *nums, int numsSize) {
    long long a = LLONG_MIN, b = LLONG_MIN, c = LLONG_MIN;
    for (int i = 0; i < numsSize; ++i) {
        long long x = nums[i];
        if (x == a || x == b || x == c)
            continue;
        /* 维护三个互不相同的最大值。 */
        if (x > a) {
            c = b;
            b = a;
            a = x;
        } else if (x > b) {
            c = b;
            b = x;
        } else if (x > c)
            c = x;
    }
    return (int)(c == LLONG_MIN ? a : c);
}
