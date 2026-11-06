bool isSubsequence(char* s, char* t) {
    int i = 0;
    for (int j = 0; s[i] != '\0' && t[j] != '\0'; j++) {
        if (s[i] == t[j]) i++;
    }
    return s[i] == '\0';
}
