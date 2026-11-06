/* 摩尔投票，O(n) 时间 O(1) 空间 */
int majorityElement(int* nums, int numsSize) {
    int cand = 0, cnt = 0;
    for (int i = 0; i < numsSize; i++) {
        if (cnt == 0) cand = nums[i];
        cnt += (nums[i] == cand) ? 1 : -1;
    }
    return cand;
}
