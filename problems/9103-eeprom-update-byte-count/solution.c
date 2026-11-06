int eepromChangedBytes(const uint8_t *before, size_t beforeSize, const uint8_t *after,
                       size_t afterSize) {
    if (beforeSize != afterSize)
        return -1;
    int count = 0;
    for (size_t i = 0; i < beforeSize; ++i)
        if (before[i] != after[i])
            ++count;
    return count;
}
