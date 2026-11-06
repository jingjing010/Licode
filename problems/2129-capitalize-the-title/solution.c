char *capitalizeTitle(char *title) {
    int n = (int)strlen(title);
    char *out = malloc(n + 1);
    memcpy(out, title, n + 1);
    for (int i = 0; i < n;) {
        int j = i;
        while (j < n && out[j] != ' ') {
            out[j] = (char)tolower((unsigned char)out[j]);
            ++j;
        }
        if (j - i > 2)
            out[i] = (char)toupper((unsigned char)out[i]);
        i = j + 1;
    }
    return out;
}
