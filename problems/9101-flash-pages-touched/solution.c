uint32_t flashPages(uint32_t address, uint32_t length, int pageSize) {
    if (length == 0)
        return 0;
    return (uint32_t)(((uint64_t)(address % (uint32_t)pageSize) + length + pageSize - 1) /
                      pageSize);
}
