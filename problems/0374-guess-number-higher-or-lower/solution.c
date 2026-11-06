int guessNumber(int n) {
    int lo = 1, hi = n;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        int r = guess(mid);
        if (r == 0) return mid;
        if (r < 0) hi = mid - 1;
        else lo = mid + 1;
    }
    return -1;
}
