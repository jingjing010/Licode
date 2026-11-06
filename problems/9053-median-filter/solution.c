static int16_t sampleAt(const int16_t* signal, size_t len, long idx) {
    if (idx < 0) idx = 0;
    if (idx > (long)len - 1) idx = (long)len - 1;
    return signal[idx];
}

void medianFilter(const int16_t* signal, size_t len, size_t k, int16_t* out) {
    long h = (long)(k / 2);
    int16_t* win = (int16_t*)malloc(sizeof(int16_t) * k);
    int n = 0;
    /* 第一个窗口：下标 -h .. h，插入排序 */
    for (long j = -h; j <= h; j++) {
        int16_t v = sampleAt(signal, len, j);
        int p = n++;
        while (p > 0 && win[p - 1] > v) {
            win[p] = win[p - 1];
            p--;
        }
        win[p] = v;
    }
    for (size_t i = 0; i < len; i++) {
        out[i] = win[h];
        if (i + 1 == len) break;
        int16_t oldV = sampleAt(signal, len, (long)i - h);
        int16_t newV = sampleAt(signal, len, (long)i + h + 1);
        int p = 0;
        while (win[p] != oldV) p++;
        /* 删除 oldV 的位置后插入 newV，保持有序 */
        while (p > 0 && win[p - 1] > newV) {
            win[p] = win[p - 1];
            p--;
        }
        while (p + 1 < (int)k && win[p + 1] < newV) {
            win[p] = win[p + 1];
            p++;
        }
        win[p] = newV;
    }
    free(win);
}
