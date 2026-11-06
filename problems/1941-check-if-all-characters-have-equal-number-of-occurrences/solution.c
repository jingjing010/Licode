bool areOccurrencesEqual(char *s) {
    int counts[26] = {0}, expected = 0;
    for (int i = 0; s[i]; ++i)
        ++counts[s[i] - 'a'];
    for (int i = 0; i < 26; ++i)
        if (counts[i]) {
            if (expected && expected != counts[i])
                return false;
            expected = counts[i];
        }
    return true;
}
