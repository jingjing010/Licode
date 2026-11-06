int findMaxConsecutiveOnes(int* nums, int numsSize) {
    int ans = 0, cnt = 0;
    for (int i = 0; i < numsSize; i++) {
        cnt = nums[i] == 1 ? cnt + 1 : 0;
        if (cnt > ans) ans = cnt;
    }
    return ans;
}
