static int lowerBound(int* nums, int n, long long x) {
    int lo = 0, hi = n;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] < x) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}

int* searchRange(int* nums, int numsSize, int target, int* returnSize) {
    int* res = (int*)malloc(sizeof(int) * 2);
    *returnSize = 2;
    int l = lowerBound(nums, numsSize, target);
    if (l == numsSize || nums[l] != target) {
        res[0] = res[1] = -1;
        return res;
    }
    res[0] = l;
    res[1] = lowerBound(nums, numsSize, (long long)target + 1) - 1;
    return res;
}
