/* 一维滚动数组 DP，O(mn) 时间，O(n) 空间 */
int minDistance(char* word1, char* word2) {
    int m = (int)strlen(word1), n = (int)strlen(word2);
    int* dp = (int*)malloc(sizeof(int) * (n + 1));
    for (int j = 0; j <= n; j++) dp[j] = j;
    for (int i = 1; i <= m; i++) {
        int leftUp = dp[0]; /* dp[i-1][j-1] */
        dp[0] = i;
        for (int j = 1; j <= n; j++) {
            int up = dp[j];
            if (word1[i - 1] == word2[j - 1]) {
                dp[j] = leftUp;
            } else {
                int best = leftUp;
                if (up < best) best = up;
                if (dp[j - 1] < best) best = dp[j - 1];
                dp[j] = best + 1;
            }
            leftUp = up;
        }
    }
    int ans = dp[n];
    free(dp);
    return ans;
}
