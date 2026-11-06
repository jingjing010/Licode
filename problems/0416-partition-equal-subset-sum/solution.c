/* 0-1 背包（一维 bool 数组，倒序遍历），O(n * sum) */
bool canPartition(int* nums, int numsSize) {
    int sum = 0;
    for (int i = 0; i < numsSize; i++) sum += nums[i];
    if (sum % 2 != 0) return false;
    int target = sum / 2;
    bool* dp = (bool*)calloc(target + 1, sizeof(bool));
    dp[0] = true;
    for (int i = 0; i < numsSize; i++)
        for (int j = target; j >= nums[i]; j--)
            if (dp[j - nums[i]]) dp[j] = true;
    bool ans = dp[target];
    free(dp);
    return ans;
}
