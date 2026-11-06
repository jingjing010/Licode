char* my_strcat(char* dst, const char* src) {
    char* d = dst;
    while (*d) d++;
    while ((*d++ = *src++) != '\0')
        ;
    return dst;
}
