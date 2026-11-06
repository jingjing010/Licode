int integerRms(int *samples, int samplesSize) {
    uint64_t sum = 0;
    for (int i = 0; i < samplesSize; ++i)
        sum += (int64_t)samples[i] * samples[i];
    uint64_t mean = sum / (unsigned)samplesSize;
    uint32_t lo = 0, hi = 32768;
    while (lo < hi) {
        uint32_t mid = lo + (hi - lo + 1) / 2;
        if ((uint64_t)mid * mid <= mean)
            lo = mid;
        else
            hi = mid - 1;
    }
    return (int)lo;
}
