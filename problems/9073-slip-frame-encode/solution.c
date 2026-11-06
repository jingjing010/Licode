int *slipEncode(const uint8_t *data, size_t len, int *returnSize) {
    int *out = malloc((2 * len + 2) * sizeof(int)), k = 0;
    out[k++] = 0xc0;
    for (size_t i = 0; i < len; ++i) {
        if (data[i] == 0xc0) {
            out[k++] = 0xdb;
            out[k++] = 0xdc;
        } else if (data[i] == 0xdb) {
            out[k++] = 0xdb;
            out[k++] = 0xdd;
        } else
            out[k++] = data[i];
    }
    out[k++] = 0xc0;
    *returnSize = k;
    return out;
}
