bool watchdogCanFeed(uint32_t elapsed, uint32_t minimum, uint32_t maximum) {
    return elapsed >= minimum && elapsed <= maximum;
}
