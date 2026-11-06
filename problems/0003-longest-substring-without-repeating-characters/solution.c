/* 滑动窗口 + 记录每个字符最近出现的位置，O(n) */
int lengthOfLongestSubstring(char* s) {
    int last[256];
    for (int c = 0; c < 256; c++) last[c] = -1;
    int left = 0, best = 0;
    for (int i = 0; s[i]; i++) {
        int c = (unsigned char)s[i];
        if (last[c] >= left) left = last[c] + 1;
        last[c] = i;
        if (i - left + 1 > best) best = i - left + 1;
    }
    return best;
}
