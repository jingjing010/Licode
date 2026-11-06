/* 快慢双指针解法，O(n) 时间，O(1) 额外空间 */
int removeDuplicates(int* nums, int numsSize) {
    if (numsSize == 0) return 0;
    int k = 1; /* nums[0..k-1] 是已经去重的部分 */
    for (int i = 1; i < numsSize; i++) {
        if (nums[i] != nums[k - 1]) {
            nums[k] = nums[i];
            k++;
        }
    }
    return k;
}
