static int cmp(const void *a, const void *b) {
    int x = *(const int *)a, y = *(const int *)b;
    return (x > y) - (x < y);
}
int findLHS(int *nums, int numsSize) {
    qsort(nums, numsSize, sizeof(int), cmp);
    int left = 0, best = 0;
    for (int right = 0; right < numsSize; ++right) {
        while ((long long)nums[right] - nums[left] > 1)
            ++left;
        if ((long long)nums[right] - nums[left] == 1 && right - left + 1 > best)
            best = right - left + 1;
    }
    return best;
}
