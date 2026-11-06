/* 逐行回溯 + 列/两条斜线的位掩码，O(n!) */
static void nq_dfs(int n, int r, int cols, int d1, int d2, int* pos, char*** res, int* cnt) {
    if (r == n) {
        char** board = (char**)malloc(sizeof(char*) * n);
        for (int i = 0; i < n; i++) {
            board[i] = (char*)malloc(n + 1);
            memset(board[i], '.', n);
            board[i][pos[i]] = 'Q';
            board[i][n] = '\0';
        }
        res[(*cnt)++] = board;
        return;
    }
    int full = (1 << n) - 1;
    int avail = full & ~(cols | d1 | d2);
    while (avail) {
        int bit = avail & -avail;
        avail ^= bit;
        int c = 0;
        while ((1 << c) != bit) c++;
        pos[r] = c;
        nq_dfs(n, r + 1, cols | bit, ((d1 | bit) << 1) & full, (d2 | bit) >> 1, pos, res, cnt);
    }
}

char*** solveNQueens(int n, int* returnSize, int** returnColumnSizes) {
    /* n <= 9 时解的个数最多 352 */
    char*** res = (char***)malloc(sizeof(char**) * 400);
    int pos[9];
    *returnSize = 0;
    nq_dfs(n, 0, 0, 0, 0, pos, res, returnSize);
    *returnColumnSizes = (int*)malloc(sizeof(int) * 400);
    for (int i = 0; i < *returnSize; i++) (*returnColumnSizes)[i] = n;
    return res;
}
