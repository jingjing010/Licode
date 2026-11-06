int arrangeCoins(int n) {
    long long lo = 1, hi = n;
    while (lo < hi) {
        long long mid = lo + (hi - lo + 1) / 2;
        if (mid * (mid + 1) / 2 <= n) lo = mid;
        else hi = mid - 1;
    }
    return (int)lo;
}
