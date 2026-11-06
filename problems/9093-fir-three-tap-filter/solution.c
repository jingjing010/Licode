int *firThreeTap(int *samples, int samplesSize, int *returnSize) {
    int *out = malloc((samplesSize + 1) * sizeof(int)), p1 = 0, p2 = 0;
    for (int i = 0; i < samplesSize; ++i) {
        out[i] = (samples[i] + 2 * p1 + p2) / 4;
        p2 = p1;
        p1 = samples[i];
    }
    *returnSize = samplesSize;
    return out;
}
