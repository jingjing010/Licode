double findMedianSortedArrays(int* nums1, int nums1Size, int* nums2, int nums2Size) {
    if (nums1Size > nums2Size) return findMedianSortedArrays(nums2, nums2Size, nums1, nums1Size);
    int m = nums1Size, n = nums2Size;
    int half = (m + n + 1) / 2;
    int lo = 0, hi = m;
    while (lo <= hi) {
        int i = lo + (hi - lo) / 2;
        int j = half - i;
        int l1 = (i == 0) ? INT_MIN : nums1[i - 1];
        int r1 = (i == m) ? INT_MAX : nums1[i];
        int l2 = (j == 0) ? INT_MIN : nums2[j - 1];
        int r2 = (j == n) ? INT_MAX : nums2[j];
        if (l1 > r2) {
            hi = i - 1;
        } else if (l2 > r1) {
            lo = i + 1;
        } else {
            int left = l1 > l2 ? l1 : l2;
            if ((m + n) % 2 == 1) return left;
            int right = r1 < r2 ? r1 : r2;
            return (left + (double)right) / 2.0;
        }
    }
    return 0.0;
}
