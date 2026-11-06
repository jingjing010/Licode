int firstUniqChar(char *s) {
    int counts[26] = {0};
    for (int i = 0; s[i]; ++i)
        ++counts[s[i] - 'a'];
    for (int i = 0; s[i]; ++i)
        if (counts[s[i] - 'a'] == 1)
            return i;
    return -1;
}
