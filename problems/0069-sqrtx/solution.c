/* 二分查找，O(log x) */
int mySqrt(int x) {
    int lo = 0, hi = x, ans = 0;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if ((long long)mid * mid <= x) {
            ans = mid;
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    return ans;
}
