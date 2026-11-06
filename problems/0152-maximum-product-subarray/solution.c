/* 动态规划：同时维护以当前元素结尾的最大 / 最小乘积，O(n) */
int maxProduct(int* nums, int numsSize) {
    long long mx = nums[0], mn = nums[0], ans = nums[0];
    for (int i = 1; i < numsSize; i++) {
        long long x = nums[i];
        long long a = mx * x, b = mn * x;
        long long nmx = x, nmn = x;
        if (a > nmx) nmx = a;
        if (b > nmx) nmx = b;
        if (a < nmn) nmn = a;
        if (b < nmn) nmn = b;
        mx = nmx;
        mn = nmn;
        if (mx > ans) ans = mx;
    }
    return (int)ans;
}
