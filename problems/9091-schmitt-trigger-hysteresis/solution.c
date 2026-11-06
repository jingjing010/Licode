int *schmittTrigger(int *samples, int samplesSize, int low, int high, int *returnSize) {
    int *out = malloc((samplesSize + 1) * sizeof(int)), state = 0;
    for (int i = 0; i < samplesSize; ++i) {
        if (samples[i] >= high)
            state = 1;
        else if (samples[i] <= low)
            state = 0;
        out[i] = state;
    }
    *returnSize = samplesSize;
    return out;
}
