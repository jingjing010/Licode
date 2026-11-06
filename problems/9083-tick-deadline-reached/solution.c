bool deadlineReached(uint32_t now, uint32_t deadline) {
    /* 不把无符号差值强转有符号，直接检查半周期范围。 */
    return now - deadline < 0x80000000u;
}
