bool canConstruct(char *s, char *t) {
    int counts[26] = {0};
    /* 先统计来源，再扣除需要的字母。 */
    for (int i = 0; t[i]; ++i)
        ++counts[t[i] - 'a'];
    for (int i = 0; s[i]; ++i)
        if (--counts[s[i] - 'a'] < 0)
            return false;

    return true;
}
