/* 动态规划（滚动变量），O(n) */
int climbStairs(int n) {
    int a = 1, b = 1; /* f(0), f(1) */
    for (int i = 2; i <= n; i++) {
        int c = a + b;
        a = b;
        b = c;
    }
    return b;
}
