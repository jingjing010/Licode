/* 中心扩展法，O(n^2) 时间，O(1) 额外空间 */
static int expandAround(const char* s, int n, int l, int r) {
    while (l >= 0 && r < n && s[l] == s[r]) {
        l--;
        r++;
    }
    return r - l - 1;
}

char* longestPalindrome(char* s) {
    int n = (int)strlen(s);
    int start = 0, best = 0;
    for (int i = 0; i < n; i++) {
        int len1 = expandAround(s, n, i, i);
        int len2 = expandAround(s, n, i, i + 1);
        int len = len1 > len2 ? len1 : len2;
        if (len > best) {
            best = len;
            start = i - (len - 1) / 2;
        }
    }
    char* res = (char*)malloc(best + 1);
    memcpy(res, s + start, best);
    res[best] = '\0';
    return res;
}
