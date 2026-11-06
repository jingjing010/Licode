/* 动态规划：dp[i] 表示前 i 个字符能否拆分，O(n * m * L) */
bool wordBreak(char* s, char** wordDict, int wordDictSize) {
    int n = (int)strlen(s);
    int* lens = (int*)malloc(sizeof(int) * (wordDictSize > 0 ? wordDictSize : 1));
    for (int k = 0; k < wordDictSize; k++) lens[k] = (int)strlen(wordDict[k]);
    bool* dp = (bool*)calloc(n + 1, sizeof(bool));
    dp[0] = true;
    for (int i = 1; i <= n; i++) {
        for (int k = 0; k < wordDictSize && !dp[i]; k++) {
            int L = lens[k];
            if (L <= i && dp[i - L] && strncmp(s + i - L, wordDict[k], L) == 0) dp[i] = true;
        }
    }
    bool ans = dp[n];
    free(dp);
    free(lens);
    return ans;
}
