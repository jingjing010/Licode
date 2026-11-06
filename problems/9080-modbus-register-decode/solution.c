int *decodeRegisters(const uint8_t *data, size_t len, int *returnSize) {
    int *out = malloc((len / 2 + 1) * sizeof(int));
    for (size_t i = 0; i < len / 2; ++i)
        out[i] = ((unsigned)data[2 * i] << 8) | data[2 * i + 1];
    *returnSize = (int)(len / 2);
    return out;
}
