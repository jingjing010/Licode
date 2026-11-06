/* 前缀积存进答案数组 + 一个变量记录后缀积，O(n) 时间 O(1) 额外空间 */
int* productExceptSelf(int* nums, int numsSize, int* returnSize) {
    int* ans = (int*)malloc(sizeof(int) * numsSize);
    *returnSize = numsSize;
    ans[0] = 1;
    for (int i = 1; i < numsSize; i++) ans[i] = ans[i - 1] * nums[i - 1];
    int right = 1;
    for (int i = numsSize - 1; i >= 0; i--) {
        ans[i] *= right;
        right *= nums[i];
    }
    return ans;
}
