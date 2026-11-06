int *runLengthDecode(const uint8_t *data, size_t len, int *returnSize) {
    int count = 0;
    for (size_t i = 0; i < len; i += 2)
        count += data[i];
    int *out = malloc((count + 1) * sizeof(int)), k = 0;
    for (size_t i = 0; i < len; i += 2)
        for (unsigned j = 0; j < data[i]; ++j)
            out[k++] = data[i + 1];
    *returnSize = k;
    return out;
}
