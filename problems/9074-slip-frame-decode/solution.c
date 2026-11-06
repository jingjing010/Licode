int *slipDecode(const uint8_t *data, size_t len, int *returnSize) {
    int *out = malloc(len * sizeof(int)), k = 0;
    for (size_t i = 1; i + 1 < len; ++i) {
        int x = data[i];
        if (x == 0xdb) {
            ++i;
            x = data[i] == 0xdc ? 0xc0 : 0xdb;
        }
        out[k++] = x;
    }
    *returnSize = k;
    return out;
}
