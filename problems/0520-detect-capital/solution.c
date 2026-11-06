bool detectCapitalUse(char *word) {
    int caps = 0, n = (int)strlen(word);
    for (int i = 0; i < n; ++i)
        if (word[i] >= 'A' && word[i] <= 'Z')
            ++caps;
    return caps == 0 || caps == n || (caps == 1 && word[0] >= 'A' && word[0] <= 'Z');
}
