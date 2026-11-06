int bulbSwitch(int n) {
    /* 只有完全平方数有奇数个约数。 */
    int lo = 0, hi = 46340;
    while (lo < hi) {
        int m = lo + (hi - lo + 1) / 2;
        if ((long long)m * m <= n)
            lo = m;
        else
            hi = m - 1;
    }
    return lo;
}
