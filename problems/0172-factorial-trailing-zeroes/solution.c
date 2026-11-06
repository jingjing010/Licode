/* 统计因子 5 的个数：n/5 + n/25 + ...，O(log n) */
int trailingZeroes(int n) {
    int cnt = 0;
    while (n > 0) {
        n /= 5;
        cnt += n;
    }
    return cnt;
}
