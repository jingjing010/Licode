static int vowel(char c) {
    return strchr("aeiouAEIOU", c) != NULL;
}
bool halvesAreAlike(char *s) {
    int n = (int)strlen(s), balance = 0;
    for (int i = 0; i < n / 2; ++i)
        balance += vowel(s[i]) - vowel(s[i + n / 2]);
    return balance == 0;
}
