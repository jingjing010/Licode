int *dmaChunks(int length, int maximum, int *returnSize) {
    int n = (length + maximum - 1) / maximum, *out = malloc((n + 1) * sizeof(int));
    for (int i = 0; i < n; ++i) {
        out[i] = length > maximum ? maximum : length;
        length -= out[i];
    }
    *returnSize = n;
    return out;
}
