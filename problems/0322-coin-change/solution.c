/* 完全背包 DP，O(amount * coinsSize) */
int coinChange(int* coins, int coinsSize, int amount) {
    int INF = amount + 1;
    int* dp = (int*)malloc(sizeof(int) * (amount + 1));
    dp[0] = 0;
    for (int i = 1; i <= amount; i++) {
        dp[i] = INF;
        for (int k = 0; k < coinsSize; k++) {
            if (coins[k] <= i && dp[i - coins[k]] + 1 < dp[i]) dp[i] = dp[i - coins[k]] + 1;
        }
    }
    int ans = dp[amount] >= INF ? -1 : dp[amount];
    free(dp);
    return ans;
}
