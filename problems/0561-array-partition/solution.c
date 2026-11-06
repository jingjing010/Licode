static int compare(const void *a, const void *b) {
    int x = *(const int *)a, y = *(const int *)b;
    return (x > y) - (x < y);
}
int arrayPairSum(int *nums, int numsSize) {
    qsort(nums, numsSize, sizeof(int), compare);
    int sum = 0;
    /* 相邻配对可以减少较大元素被浪费的数值。 */
    for (int i = 0; i < numsSize; i += 2)
        sum += nums[i];
    return sum;
}
