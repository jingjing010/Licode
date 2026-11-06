int timerReload(int clockHz, int prescaler, int frequency) {
    int64_t divisor = (int64_t)(prescaler + 1) * frequency;
    return (int)(((int64_t)clockHz + divisor / 2) / divisor) - 1;
}
