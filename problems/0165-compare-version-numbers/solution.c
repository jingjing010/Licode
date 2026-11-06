int compareVersion(char* version1, char* version2) {
    int i = 0, j = 0;
    while (version1[i] || version2[j]) {
        long long x = 0, y = 0;
        while (version1[i] && version1[i] != '.') x = x * 10 + (version1[i++] - '0');
        while (version2[j] && version2[j] != '.') y = y * 10 + (version2[j++] - '0');
        if (x != y) return x < y ? -1 : 1;
        if (version1[i] == '.') i++;
        if (version2[j] == '.') j++;
    }
    return 0;
}
