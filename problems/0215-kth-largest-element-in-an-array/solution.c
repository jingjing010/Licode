/* 值域只有 [-10^4, 10^4]，计数排序 O(n + 值域) */
#define OFFSET 10000

int findKthLargest(int* nums, int numsSize, int k) {
    static int cnt[2 * OFFSET + 1];
    memset(cnt, 0, sizeof(cnt));
    for (int i = 0; i < numsSize; i++) cnt[nums[i] + OFFSET]++;
    for (int v = 2 * OFFSET; v >= 0; v--) {
        k -= cnt[v];
        if (k <= 0) return v - OFFSET;
    }
    return 0;
}
