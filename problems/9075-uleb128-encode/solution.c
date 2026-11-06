int *uleb128Encode(uint32_t value, int *returnSize) {
    int *out = malloc(5 * sizeof(int)), k = 0;
    do {
        uint8_t byte = (uint8_t)(value & 0x7fu);
        value >>= 7;
        if (value)
            byte |= 0x80;
        out[k++] = byte;
    } while (value);
    *returnSize = k;
    return out;
}
