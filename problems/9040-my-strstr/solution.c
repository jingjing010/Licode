char* my_strstr(const char* haystack, const char* needle) {
    if (*needle == '\0') return (char*)haystack;
    for (const char* start = haystack; *start; start++) {
        const char* h = start;
        const char* n = needle;
        while (*n && *h == *n) {
            h++;
            n++;
        }
        if (*n == '\0') return (char*)start;
    }
    return NULL;
}
