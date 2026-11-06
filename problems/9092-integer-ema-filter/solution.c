int *emaFilter(int *samples, int samplesSize, int shift, int *returnSize) {
    int *out = malloc((samplesSize + 1) * sizeof(int)), y = 0, divisor = 1 << shift;
    /* 负差值用整数除法向零截断，不依赖负数右移行为。 */
    for (int i = 0; i < samplesSize; ++i) {
        y += (samples[i] - y) / divisor;
        out[i] = y;
    }
    *returnSize = samplesSize;
    return out;
}
