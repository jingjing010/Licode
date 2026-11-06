static bool isVowel(char c) {
    return strchr("aeiouAEIOU", c) != NULL && c != '\0';
}

char* reverseVowels(char* s) {
    int l = 0, r = (int)strlen(s) - 1;
    while (l < r) {
        while (l < r && !isVowel(s[l])) l++;
        while (l < r && !isVowel(s[r])) r--;
        if (l < r) {
            char t = s[l];
            s[l] = s[r];
            s[r] = t;
            l++;
            r--;
        }
    }
    return s;
}
