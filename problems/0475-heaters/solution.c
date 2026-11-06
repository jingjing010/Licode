static int cmpInt(const void* a, const void* b) {
    int x = *(const int*)a, y = *(const int*)b;
    return (x > y) - (x < y);
}

int findRadius(int* houses, int housesSize, int* heaters, int heatersSize) {
    qsort(heaters, heatersSize, sizeof(int), cmpInt);
    int ans = 0;
    for (int i = 0; i < housesSize; i++) {
        int h = houses[i];
        int lo = 0, hi = heatersSize;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (heaters[mid] < h) lo = mid + 1;
            else hi = mid;
        }
        int best = INT_MAX;
        if (lo < heatersSize) best = heaters[lo] - h;
        if (lo > 0 && h - heaters[lo - 1] < best) best = h - heaters[lo - 1];
        if (best > ans) ans = best;
    }
    return ans;
}
