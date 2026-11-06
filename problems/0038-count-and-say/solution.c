char* countAndSay(int n) {
    char* cur = (char*)malloc(2);
    strcpy(cur, "1");
    int len = 1;
    for (int step = 2; step <= n; step++) {
        char* next = (char*)malloc(2 * len + 1);
        int k = 0;
        for (int i = 0; i < len;) {
            int j = i;
            while (j < len && cur[j] == cur[i]) j++;
            next[k++] = (char)('0' + (j - i));
            next[k++] = cur[i];
            i = j;
        }
        next[k] = '\0';
        free(cur);
        cur = next;
        len = k;
    }
    return cur;
}
