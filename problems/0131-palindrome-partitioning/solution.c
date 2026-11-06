/* 动态规划预处理回文 + 回溯，O(n * 2^n) */
typedef struct {
    const char* s;
    int n;
    bool pal[16][16];
    int cut[17];          /* 当前方案中每段的起点，cut[k] 为第 k 段起点 */
    char*** res;
    int* cols;
    int cnt, cap;
} PpCtx;

static void pp_dfs(PpCtx* c, int start, int k) {
    if (start == c->n) {
        if (c->cnt == c->cap) {
            c->cap *= 2;
            c->res = (char***)realloc(c->res, sizeof(char**) * c->cap);
            c->cols = (int*)realloc(c->cols, sizeof(int) * c->cap);
        }
        char** row = (char**)malloc(sizeof(char*) * (k + 1));
        c->cut[k] = c->n;
        for (int i = 0; i < k; i++) {
            int len = c->cut[i + 1] - c->cut[i];
            row[i] = (char*)malloc(len + 1);
            memcpy(row[i], c->s + c->cut[i], len);
            row[i][len] = '\0';
        }
        c->res[c->cnt] = row;
        c->cols[c->cnt] = k;
        c->cnt++;
        return;
    }
    for (int end = start; end < c->n; end++) {
        if (!c->pal[start][end]) continue;
        c->cut[k] = start;
        pp_dfs(c, end + 1, k + 1);
    }
}

char*** partition(char* s, int* returnSize, int** returnColumnSizes) {
    static PpCtx c;
    c.s = s;
    c.n = (int)strlen(s);
    for (int i = c.n - 1; i >= 0; i--)
        for (int j = i; j < c.n; j++)
            c.pal[i][j] = s[i] == s[j] && (j - i < 2 || c.pal[i + 1][j - 1]);
    c.cap = 64;
    c.cnt = 0;
    c.res = (char***)malloc(sizeof(char**) * c.cap);
    c.cols = (int*)malloc(sizeof(int) * c.cap);
    pp_dfs(&c, 0, 0);
    *returnSize = c.cnt;
    *returnColumnSizes = c.cols;
    return c.res;
}
