int *slewLimit(int *targets, int targetsSize, int step, int *returnSize) {
    int *out = malloc((targetsSize + 1) * sizeof(int)), y = 0;
    for (int i = 0; i < targetsSize; ++i) {
        int d = targets[i] - y;
        if (d > step)
            d = step;
        if (d < -step)
            d = -step;
        y += d;
        out[i] = y;
    }
    *returnSize = targetsSize;
    return out;
}
