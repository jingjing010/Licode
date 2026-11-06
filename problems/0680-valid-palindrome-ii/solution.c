static bool rangePalindrome(char *s, int l, int r) {
    while (l < r)
        if (s[l++] != s[r--])
            return false;
    return true;
}
bool validPalindrome(char *s) {
    int l = 0, r = (int)strlen(s) - 1;
    while (l < r) {
        if (s[l] != s[r])
            return rangePalindrome(s, l + 1, r) || rangePalindrome(s, l, r - 1);
        ++l;
        --r;
    }
    return true;
}
