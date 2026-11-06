int findPoisonedDuration(int* timeSeries, int timeSeriesSize, int duration) {
    int total = 0;
    for (int i = 0; i + 1 < timeSeriesSize; i++) {
        int gap = timeSeries[i + 1] - timeSeries[i];
        total += gap < duration ? gap : duration;
    }
    return total + duration;
}
