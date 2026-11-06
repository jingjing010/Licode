/* 单调递减双端队列（存下标），O(n) */
int* maxSlidingWindow(int* nums, int numsSize, int k, int* returnSize) {
    int* dq = (int*)malloc(sizeof(int) * numsSize);
    int* ans = (int*)malloc(sizeof(int) * (numsSize - k + 1));
    int head = 0, tail = 0, cnt = 0;
    for (int i = 0; i < numsSize; i++) {
        while (tail > head && nums[dq[tail - 1]] <= nums[i]) tail--;
        dq[tail++] = i;
        if (dq[head] <= i - k) head++;
        if (i >= k - 1) ans[cnt++] = nums[dq[head]];
    }
    free(dq);
    *returnSize = cnt;
    return ans;
}
