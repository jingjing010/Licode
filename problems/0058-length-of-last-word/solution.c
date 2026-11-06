int lengthOfLastWord(char *s) {
    int i = (int)strlen(s) - 1, count = 0;
    while (i >= 0 && s[i] == ' ')
        --i;
    while (i >= 0 && s[i] != ' ') {
        ++count;
        --i;
    }
    return count;
}
