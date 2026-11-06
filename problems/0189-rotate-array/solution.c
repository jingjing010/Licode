/* 三次翻转，O(n) 时间 O(1) 空间 */
static void reverseRange(int* a, int l, int r) {
    while (l < r) {
        int t = a[l];
        a[l++] = a[r];
        a[r--] = t;
    }
}

void rotate(int* nums, int numsSize, int k) {
    k %= numsSize;
    reverseRange(nums, 0, numsSize - 1);
    reverseRange(nums, 0, k - 1);
    reverseRange(nums, k, numsSize - 1);
}
