int *unpackAdc12(const uint8_t *data, size_t len, int *returnSize) {
    int *out = malloc((len / 3 * 2 + 1) * sizeof(int)), k = 0;
    for (size_t i = 0; i < len; i += 3) {
        out[k++] = ((unsigned)data[i] << 4) | (data[i + 1] >> 4);
        out[k++] = ((unsigned)(data[i + 1] & 15) << 8) | data[i + 2];
    }
    *returnSize = k;
    return out;
}
