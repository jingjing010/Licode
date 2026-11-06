/* 异或：成对的数相互抵消，O(n) 时间 O(1) 空间 */
int singleNumber(int* nums, int numsSize) {
    int x = 0;
    for (int i = 0; i < numsSize; i++) x ^= nums[i];
    return x;
}
