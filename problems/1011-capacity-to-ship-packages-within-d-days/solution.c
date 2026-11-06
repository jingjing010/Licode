static int daysNeeded(int* weights, int weightsSize, int cap) {
    int d = 1, cur = 0;
    for (int i = 0; i < weightsSize; i++) {
        if (cur + weights[i] > cap) {
            d++;
            cur = 0;
        }
        cur += weights[i];
    }
    return d;
}

int shipWithinDays(int* weights, int weightsSize, int days) {
    int lo = 0, hi = 0;
    for (int i = 0; i < weightsSize; i++) {
        if (weights[i] > lo) lo = weights[i];
        hi += weights[i];
    }
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (daysNeeded(weights, weightsSize, mid) <= days) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}
