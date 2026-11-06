static int compare(const void *a, const void *b) {
    int x = *(const int *)a, y = *(const int *)b;
    return (x > y) - (x < y);
}
bool containsDuplicate(int *nums, int numsSize) {
    /* 排序后重复元素一定相邻。 */
    qsort(nums, numsSize, sizeof(int), compare);
    for (int i = 1; i < numsSize; ++i)
        if (nums[i] == nums[i - 1])
            return true;
    return false;
}
