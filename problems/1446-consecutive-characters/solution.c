int maxPower(char *s) {
    int best = 0, run = 0;
    for (int i = 0; s[i]; ++i) {
        run = (i > 0 && s[i] == s[i - 1]) ? run + 1 : 1;
        if (run > best)
            best = run;
    }
    return best;
}
