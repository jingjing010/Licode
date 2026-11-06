bool is_power_of_two(uint32_t x) {
    return x != 0 && (x & (x - 1u)) == 0;
}
