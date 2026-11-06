int longestFreeRun(uint32_t bitmap, int width) {
    int run = 0, best = 0;
    for (int i = 0; i < width; ++i) {
        run = ((bitmap >> i) & 1u) ? 0 : run + 1;
        if (run > best)
            best = run;
    }
    return best;
}
