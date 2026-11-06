int balancedStringSplit(char *s) {
    int balance = 0, count = 0;
    for (int i = 0; s[i]; ++i) {
        balance += s[i] == 'L' ? 1 : -1;
        if (balance == 0)
            ++count;
    }
    return count;
}
