int *periodicReleases(int *times, int timesSize, int period, int *returnSize) {
    int *out = malloc((timesSize + 1) * sizeof(int)), previous = 0;
    for (int i = 0; i < timesSize; ++i) {
        int total = times[i] / period;
        out[i] = total - previous;
        previous = total;
    }
    *returnSize = timesSize;
    return out;
}
