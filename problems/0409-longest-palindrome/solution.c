int longestPalindrome(char* s) {
    int cnt[128] = {0};
    for (int i = 0; s[i]; i++) cnt[(unsigned char)s[i]]++;
    int ans = 0, odd = 0;
    for (int c = 0; c < 128; c++) {
        ans += cnt[c] / 2 * 2;
        if (cnt[c] % 2) odd = 1;
    }
    return ans + odd;
}
