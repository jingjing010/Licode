char *defangIPaddr(char *address) {
    int n = (int)strlen(address), k = 0;
    char *out = malloc(n * 3 + 1);
    for (int i = 0; i < n; ++i) {
        if (address[i] == '.') {
            out[k++] = '[';
            out[k++] = '.';
            out[k++] = ']';
        } else
            out[k++] = address[i];
    }
    out[k] = 0;
    return out;
}
