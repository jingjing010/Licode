char *largestGoodInteger(char *num) {
    char best = 0;
    for (int i = 2; num[i]; ++i)
        if (num[i] == num[i - 1] && num[i] == num[i - 2] && num[i] > best)
            best = num[i];
    char *out = malloc(4);
    int n = best ? 3 : 0;
    for (int i = 0; i < n; ++i)
        out[i] = best;
    out[n] = 0;
    return out;
}
