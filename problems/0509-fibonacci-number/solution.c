/* 滚动变量迭代，O(n) 时间，O(1) 空间 */
int fib(int n) {
    int a = 0, b = 1;
    for (int i = 0; i < n; i++) {
        int c = a + b;
        a = b;
        b = c;
    }
    return a;
}
