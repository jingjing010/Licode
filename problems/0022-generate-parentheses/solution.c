/* 回溯：左括号不超过 n、右括号不超过左括号，O(4^n / sqrt(n)) */
static void gp_dfs(int n, int open, int close, char* path, char** res, int* cnt) {
    int len = open + close;
    if (len == 2 * n) {
        res[*cnt] = (char*)malloc(2 * n + 1);
        memcpy(res[*cnt], path, 2 * n + 1);
        (*cnt)++;
        return;
    }
    if (open < n) {
        path[len] = '(';
        gp_dfs(n, open + 1, close, path, res, cnt);
    }
    if (close < open) {
        path[len] = ')';
        gp_dfs(n, open, close + 1, path, res, cnt);
    }
}

char** generateParenthesis(int n, int* returnSize) {
    /* 卡特兰数 C(8) = 1430 */
    int cap = 1;
    for (int i = 0; i < n; i++) cap = cap * 2 * (2 * i + 1) / (i + 2);
    char** res = (char**)malloc(sizeof(char*) * (cap + 1));
    char path[17];
    path[2 * n] = '\0';
    *returnSize = 0;
    gp_dfs(n, 0, 0, path, res, returnSize);
    return res;
}
