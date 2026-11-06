bool canProgramFlash(const uint8_t *before, size_t beforeSize, const uint8_t *after,
                     size_t afterSize) {
    if (beforeSize != afterSize)
        return false;
    for (size_t i = 0; i < beforeSize; ++i)
        if ((before[i] & after[i]) != after[i])
            return false;
    return true;
}
