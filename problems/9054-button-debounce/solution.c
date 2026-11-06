int** debounce(const uint8_t* samples, size_t len, uint16_t stableCount,
               int* returnSize, int** returnColumnSizes) {
    int** res = (int**)malloc(sizeof(int*) * (len + 1));
    int* cols = (int*)malloc(sizeof(int) * (len + 1));
    int n = 0;
    uint8_t stable = 0;
    uint16_t cnt = 0;
    for (size_t i = 0; i < len; i++) {
        if (samples[i] == stable) {
            cnt = 0;
            continue;
        }
        if (++cnt >= stableCount) {
            stable = samples[i];
            cnt = 0;
            res[n] = (int*)malloc(sizeof(int) * 2);
            res[n][0] = (int)i;
            res[n][1] = stable;
            cols[n] = 2;
            n++;
        }
    }
    *returnSize = n;
    *returnColumnSizes = cols;
    return res;
}
