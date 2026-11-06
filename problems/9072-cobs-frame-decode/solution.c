int *cobsDecode(const uint8_t *data, size_t len, int *returnSize) {
    int *out = malloc((len + 1) * sizeof(int));
    size_t i = 0;
    int k = 0;
    while (i < len) {
        unsigned code = data[i++];
        for (unsigned j = 1; j < code; ++j)
            out[k++] = data[i++];
        if (code < 255 && i < len)
            out[k++] = 0;
    }
    *returnSize = k;
    return out;
}
