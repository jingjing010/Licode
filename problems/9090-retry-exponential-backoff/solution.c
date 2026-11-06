int retryDelay(int base, int attempt, int cap) {
    int delay = base < cap ? base : cap;
    for (int i = 0; i < attempt && delay < cap; ++i) {
        if (delay > cap / 2) {
            delay = cap;
            break;
        }
        delay *= 2;
    }
    return delay;
}
