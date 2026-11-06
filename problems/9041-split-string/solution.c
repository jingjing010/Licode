int split_string(char* str, char delim, char* tokens[], int maxTokens) {
    int count = 0;
    char* p = str;
    while (count < maxTokens) {
        while (*p == delim) p++;
        if (*p == '\0') break;
        tokens[count++] = p;
        while (*p != '\0' && *p != delim) p++;
        if (*p == '\0') break;
        *p++ = '\0';
    }
    return count;
}
