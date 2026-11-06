static bool ws_dfs(char** b, int m, int n, int r, int c, const char* w, int k) {
    if (w[k] == '\0') return true;
    if (r < 0 || r >= m || c < 0 || c >= n || b[r][c] != w[k]) return false;
    char t = b[r][c];
    b[r][c] = '#';
    bool ok = ws_dfs(b, m, n, r + 1, c, w, k + 1) || ws_dfs(b, m, n, r - 1, c, w, k + 1) ||
              ws_dfs(b, m, n, r, c + 1, w, k + 1) || ws_dfs(b, m, n, r, c - 1, w, k + 1);
    b[r][c] = t;
    return ok;
}

bool exist(char** board, int boardSize, int* boardColSize, char* word) {
    int m = boardSize, n = boardColSize[0];
    int len = (int)strlen(word);
    if (len > m * n) return false;
    int cb[128] = {0}, cw[128] = {0};
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++) cb[(unsigned char)board[i][j]]++;
    for (int i = 0; i < len; i++)
        if (++cw[(unsigned char)word[i]] > cb[(unsigned char)word[i]]) return false;
    char w[32];
    strcpy(w, word);
    if (cb[(unsigned char)w[0]] > cb[(unsigned char)w[len - 1]])
        for (int i = 0, j = len - 1; i < j; i++, j--) { char t = w[i]; w[i] = w[j]; w[j] = t; }
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            if (ws_dfs(board, m, n, i, j, w, 0)) return true;
    return false;
}
