/* Floyd 判圈：把 i -> nums[i] 看成链表，重复数是环的入口。O(n) 时间 O(1) 空间，不修改数组 */
int findDuplicate(int* nums, int numsSize) {
    int slow = 0, fast = 0;
    do {
        slow = nums[slow];
        fast = nums[nums[fast]];
    } while (slow != fast);
    slow = 0;
    while (slow != fast) {
        slow = nums[slow];
        fast = nums[fast];
    }
    return slow;
}
