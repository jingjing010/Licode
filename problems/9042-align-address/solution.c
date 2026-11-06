uintptr_t align_up(uintptr_t addr, size_t align) {
    uintptr_t mask = (uintptr_t)align - 1;
    return (addr + mask) & ~mask;
}

uintptr_t align_down(uintptr_t addr, size_t align) {
    return addr & ~((uintptr_t)align - 1);
}
