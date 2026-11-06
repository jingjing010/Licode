/* 一维滚动数组 DP，O(mn) 时间，O(n) 空间 */
int longestCommonSubsequence(char* text1, char* text2) {
    int m = (int)strlen(text1), n = (int)strlen(text2);
    int* dp = (int*)calloc(n + 1, sizeof(int));
    for (int i = 1; i <= m; i++) {
        int leftUp = 0; /* dp[i-1][j-1] */
        for (int j = 1; j <= n; j++) {
            int up = dp[j];
            if (text1[i - 1] == text2[j - 1]) dp[j] = leftUp + 1;
            else if (dp[j - 1] > dp[j]) dp[j] = dp[j - 1];
            leftUp = up;
        }
    }
    int ans = dp[n];
    free(dp);
    return ans;
}
