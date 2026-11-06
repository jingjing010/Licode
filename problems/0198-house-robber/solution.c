/* 滚动变量 DP，O(n) 时间，O(1) 空间 */
int rob(int* nums, int numsSize) {
    int prev2 = 0, prev1 = 0; /* dp[i-2], dp[i-1] */
    for (int i = 0; i < numsSize; i++) {
        int cur = prev1 > prev2 + nums[i] ? prev1 : prev2 + nums[i];
        prev2 = prev1;
        prev1 = cur;
    }
    return prev1;
}
