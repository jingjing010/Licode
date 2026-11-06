int *runLengthEncode(const uint8_t *data, size_t len, int *returnSize) {
    int *out = malloc((2 * len + 1) * sizeof(int)), k = 0;
    size_t i = 0;
    while (i < len) {
        size_t count = 1;
        while (i + count < len && data[i + count] == data[i] && count < 255)
            ++count;
        out[k++] = (int)count;
        out[k++] = data[i];
        i += count;
    }
    *returnSize = k;
    return out;
}
