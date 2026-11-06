void reverseString(char* s, int sSize) {
    for (int l = 0, r = sSize - 1; l < r; l++, r--) {
        char t = s[l];
        s[l] = s[r];
        s[r] = t;
    }
}
