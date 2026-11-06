int peakToPeak(int *samples, int samplesSize) {
    int lo = samples[0], hi = samples[0];
    for (int i = 1; i < samplesSize; ++i) {
        if (samples[i] < lo)
            lo = samples[i];
        if (samples[i] > hi)
            hi = samples[i];
    }
    return hi - lo;
}
