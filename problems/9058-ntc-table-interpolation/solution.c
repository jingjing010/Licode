int16_t ntcLookup(const uint16_t* adcTable, const int16_t* tempTable, size_t n, uint16_t adc) {
    if (adc <= adcTable[0]) return tempTable[0];
    if (adc >= adcTable[n - 1]) return tempTable[n - 1];
    /* 二分查找最后一个 adcTable[i] <= adc 的 i */
    size_t lo = 0, hi = n - 1;
    while (hi - lo > 1) {
        size_t mid = lo + (hi - lo) / 2;
        if (adcTable[mid] <= adc) lo = mid;
        else hi = mid;
    }
    int32_t x0 = adcTable[lo], x1 = adcTable[lo + 1];
    int32_t t0 = tempTable[lo], t1 = tempTable[lo + 1];
    int32_t num = (t1 - t0) * (int32_t)(adc - x0);
    int32_t den = x1 - x0;
    int32_t absq = (2 * (num < 0 ? -num : num) + den) / (2 * den);
    return (int16_t)(t0 + (num < 0 ? -absq : absq));
}
