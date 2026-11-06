int *cobsEncode(const uint8_t *data, size_t len, int *returnSize) {
    int *out = malloc((len + len / 254 + 2) * sizeof(int));
    size_t index = 0, k = 1;
    int code = 1;
    for (size_t i = 0; i < len; ++i) {
        if (data[i] == 0) {
            out[index] = code;
            index = k++;
            code = 1;
        } else {
            out[k++] = data[i];
            if (++code == 255) {
                out[index] = code;
                index = k++;
                code = 1;
            }
        }
    }
    out[index] = code;
    *returnSize = (int)k;
    return out;
}
