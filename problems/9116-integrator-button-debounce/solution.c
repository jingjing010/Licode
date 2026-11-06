int *integratorDebounce(int *samples, int samplesSize, int limit, int *returnSize) {
    int *out = malloc((samplesSize + 1) * sizeof(int)), count = 0, state = 0;
    for (int i = 0; i < samplesSize; ++i) {
        if (samples[i]) {
            if (count < limit)
                ++count;
        } else if (count > 0)
            --count;
        if (count == 0)
            state = 0;
        else if (count == limit)
            state = 1;
        out[i] = state;
    }
    *returnSize = samplesSize;
    return out;
}
