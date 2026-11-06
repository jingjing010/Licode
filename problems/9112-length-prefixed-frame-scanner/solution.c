int *scanFrames(const uint8_t *data, size_t len, int *returnSize) {
    int *out = malloc((len + 1) * sizeof(int)), k = 0;
    size_t i = 0;
    while (i + 2 < len) {
        if (data[i] == 0xaa && data[i + 1] == 0x55) {
            size_t n = data[i + 2];
            if (n > len - i - 3)
                break;
            out[k++] = (int)n;
            i += 3 + n;
        } else
            ++i;
    }
    *returnSize = k;
    return out;
}
