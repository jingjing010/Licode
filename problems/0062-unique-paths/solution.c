/* 一维滚动数组 DP，O(mn) 时间，O(n) 空间 */
int uniquePaths(int m, int n) {
    int* dp = (int*)malloc(sizeof(int) * n);
    for (int j = 0; j < n; j++) dp[j] = 1;
    for (int i = 1; i < m; i++)
        for (int j = 1; j < n; j++)
            dp[j] += dp[j - 1];
    int ans = dp[n - 1];
    free(dp);
    return ans;
}
