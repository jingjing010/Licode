int maxNumberOfBalloons(char *text) {
    int counts[26] = {0};
    for (int i = 0; text[i]; ++i)
        ++counts[text[i] - 'a'];
    int best = counts['b' - 'a'];
    char *word = "alon";
    for (int i = 0; word[i]; ++i) {
        int v = counts[word[i] - 'a'];
        if (word[i] == 'l' || word[i] == 'o')
            v /= 2;
        if (v < best)
            best = v;
    }
    return best;
}
