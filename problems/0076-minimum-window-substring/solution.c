/* 滑动窗口 + 缺失计数，O(m + n) */
char* minWindow(char* s, char* t) {
    int need[128] = {0};
    int missing = 0;
    for (int i = 0; t[i]; i++) {
        need[(int)t[i]]++;
        missing++;
    }
    int bestL = 0, bestLen = -1, left = 0;
    for (int r = 0; s[r]; r++) {
        if (need[(int)s[r]]-- > 0) missing--;
        if (missing > 0) continue;
        while (need[(int)s[left]] < 0) need[(int)s[left++]]++;
        if (bestLen < 0 || r - left + 1 < bestLen) {
            bestLen = r - left + 1;
            bestL = left;
        }
        need[(int)s[left++]]++;
        missing++;
    }
    if (bestLen < 0) bestLen = 0;
    char* res = (char*)malloc(bestLen + 1);
    memcpy(res, s + bestL, bestLen);
    res[bestLen] = '\0';
    return res;
}
