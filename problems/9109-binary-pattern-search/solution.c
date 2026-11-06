int findBinaryPattern(const uint8_t *data, size_t len, const uint8_t *pattern, size_t patternSize) {
    if (patternSize == 0)
        return 0;
    if (patternSize > len)
        return -1;
    for (size_t i = 0; i <= len - patternSize; ++i) {
        size_t j = 0;
        while (j < patternSize && data[i + j] == pattern[j])
            ++j;
        if (j == patternSize)
            return (int)i;
    }
    return -1;
}
