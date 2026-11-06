static long long hoursNeeded(int* piles, int pilesSize, int k) {
    long long total = 0;
    for (int i = 0; i < pilesSize; i++) total += (piles[i] - 1) / k + 1;
    return total;
}

int minEatingSpeed(int* piles, int pilesSize, int h) {
    int lo = 1, hi = 1;
    for (int i = 0; i < pilesSize; i++)
        if (piles[i] > hi) hi = piles[i];
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (hoursNeeded(piles, pilesSize, mid) <= h) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}
