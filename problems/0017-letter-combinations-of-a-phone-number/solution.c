static const char* LC_MAP[10] = {"", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"};

static void lc_dfs(const char* digits, int n, int i, char* path, char** res, int* cnt) {
    if (i == n) {
        res[*cnt] = (char*)malloc(n + 1);
        memcpy(res[*cnt], path, n + 1);
        (*cnt)++;
        return;
    }
    for (const char* p = LC_MAP[digits[i] - '0']; *p; p++) {
        path[i] = *p;
        lc_dfs(digits, n, i + 1, path, res, cnt);
    }
}

char** letterCombinations(char* digits, int* returnSize) {
    int n = (int)strlen(digits);
    *returnSize = 0;
    if (n == 0) return NULL;
    int total = 1;
    for (int i = 0; i < n; i++) total *= (int)strlen(LC_MAP[digits[i] - '0']);
    char** res = (char**)malloc(sizeof(char*) * total);
    char path[8];
    path[n] = '\0';
    lc_dfs(digits, n, 0, path, res, returnSize);
    return res;
}
