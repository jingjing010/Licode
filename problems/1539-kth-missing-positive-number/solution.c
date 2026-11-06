int findKthPositive(int *arr, int arrSize, int k) {
    int lo = 0, hi = arrSize;
    /* arr[mid]之前缺失的数量为arr[mid]-(mid+1)。 */
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (arr[mid] - mid - 1 >= k)
            hi = mid;
        else
            lo = mid + 1;
    }
    return lo + k;
}
