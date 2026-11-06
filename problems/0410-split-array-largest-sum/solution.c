static int countPieces(int* nums, int numsSize, long long limit) {
    int pieces = 1;
    long long cur = 0;
    for (int i = 0; i < numsSize; i++) {
        if (cur + nums[i] > limit) {
            pieces++;
            cur = 0;
        }
        cur += nums[i];
    }
    return pieces;
}

int splitArray(int* nums, int numsSize, int k) {
    long long lo = 0, hi = 0;
    for (int i = 0; i < numsSize; i++) {
        if (nums[i] > lo) lo = nums[i];
        hi += nums[i];
    }
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2;
        if (countPieces(nums, numsSize, mid) <= k) hi = mid;
        else lo = mid + 1;
    }
    return (int)lo;
}
