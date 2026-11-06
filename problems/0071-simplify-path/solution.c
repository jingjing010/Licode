char* simplifyPath(char* path) {
    int n = (int)strlen(path);
    int* starts = (int*)malloc(sizeof(int) * (n + 1));
    int* lens = (int*)malloc(sizeof(int) * (n + 1));
    int top = 0;
    int i = 0;
    while (i < n) {
        while (i < n && path[i] == '/') i++;
        if (i >= n) break;
        int j = i;
        while (j < n && path[j] != '/') j++;
        int len = j - i;
        if (len == 1 && path[i] == '.') {
        } else if (len == 2 && path[i] == '.' && path[i + 1] == '.') {
            if (top > 0) top--;
        } else {
            starts[top] = i;
            lens[top] = len;
            top++;
        }
        i = j;
    }
    char* res = (char*)malloc(n + 2);
    int k = 0;
    for (int t = 0; t < top; t++) {
        res[k++] = '/';
        memcpy(res + k, path + starts[t], lens[t]);
        k += lens[t];
    }
    if (k == 0) res[k++] = '/';
    res[k] = '\0';
    free(starts);
    free(lens);
    return res;
}
