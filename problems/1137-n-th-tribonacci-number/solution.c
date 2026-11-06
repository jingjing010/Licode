int tribonacci(int n) {
    int a = 0, b = 1, c = 1;
    if (n == 0)
        return 0;
    if (n < 3)
        return 1;
    /* 滚动保存前三项，不必保存完整数组。 */
    for (int i = 3; i <= n; ++i) {
        int d = a + b + c;
        a = b;
        b = c;
        c = d;
    }
    return c;
}
