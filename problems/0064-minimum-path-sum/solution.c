/* 一维滚动数组 DP，O(mn) 时间，O(n) 空间 */
int minPathSum(int** grid, int gridSize, int* gridColSize) {
    int m = gridSize, n = gridColSize[0];
    int* dp = (int*)malloc(sizeof(int) * n);
    dp[0] = grid[0][0];
    for (int j = 1; j < n; j++) dp[j] = dp[j - 1] + grid[0][j];
    for (int i = 1; i < m; i++) {
        dp[0] += grid[i][0];
        for (int j = 1; j < n; j++) {
            int best = dp[j] < dp[j - 1] ? dp[j] : dp[j - 1];
            dp[j] = best + grid[i][j];
        }
    }
    int ans = dp[n - 1];
    free(dp);
    return ans;
}
