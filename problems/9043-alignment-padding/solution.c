bool is_aligned(uintptr_t addr, size_t align) {
    return (addr & ((uintptr_t)align - 1)) == 0;
}

size_t align_padding(uintptr_t addr, size_t align) {
    return (size_t)((0 - addr) & ((uintptr_t)align - 1));
}
